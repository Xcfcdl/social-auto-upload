import os
import time
import uuid
import threading
import queue
import json
import requests
import sqlite3
from datetime import datetime
from pathlib import Path
from conf import BASE_DIR

# 配置信息（实际使用时应该从配置文件读取）
API_BASE_URL = "https://api.apimart.ai"
API_KEY = "sk-5vdtIM5RNun4CT9LDmBHkXvjowmpYKslhPqfURRbn7RL62fy"  # 需要替换为实际的API密钥

# 任务状态常量
TASK_STATUS = {
    'PENDING': 'pending',
    'PROCESSING': 'processing',
    'COMPLETED': 'completed',
    'FAILED': 'failed',
    'CANCELLED': 'cancelled'
}

# 自动保存视频到素材库
def save_video_to_material(video_url, title, description):
    """
    下载Sora2生成的视频并保存到素材库
    :param video_url: 视频URL（可能是字符串或列表）
    :param title: 视频标题
    :param description: 视频描述
    :return: 保存的文件路径或None
    """
    try:
        # 处理URL（可能是列表格式）
        if isinstance(video_url, list):
            if len(video_url) == 0:
                print("❌ 视频URL列表为空")
                return None
            video_url = video_url[0]  # 取第一个URL

        # 下载视频
        print(f"📥 开始下载视频: {video_url}")
        response = requests.get(video_url, timeout=60, stream=True)
        response.raise_for_status()

        # 生成文件名
        uuid_v1 = uuid.uuid1()
        filename = f"{title}.mp4"
        final_filename = f"{uuid_v1}_{filename}"
        filepath = Path(BASE_DIR / "videoFile" / final_filename)

        # 确保目录存在
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # 保存视频文件
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # 获取文件大小（MB）
        filesize = round(float(os.path.getsize(filepath)) / (1024 * 1024), 2)

        # 记录到数据库
        with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO file_records (filename, filesize, file_path)
                VALUES (?, ?, ?)
            ''', (filename, filesize, final_filename))
            conn.commit()

        print(f"✅ 视频已保存到素材库: {filename} ({filesize}MB)")
        return final_filename

    except Exception as e:
        print(f"❌ 保存视频到素材库失败: {e}")
        return None

# 任务管理
class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.task_lock = threading.Lock()
        self.task_queues = {}
    
    def create_task(self, task_data):
        task_id = str(uuid.uuid4())
        now = int(time.time() * 1000)
        task = {
            'taskId': task_id,
            'theme': task_data.get('theme', ''),
            'count': task_data.get('count', 1),
            'duration': task_data.get('duration', '10'),
            'aspectRatio': task_data.get('aspectRatio', '16:9'),
            'scripts': task_data.get('scripts', []),
            'status': TASK_STATUS['PENDING'],
            'progress': 0,
            'createdAt': now,
            'updatedAt': now,
            'completedAt': None,
            'videos': [],
            'error': None,
            'logs': [
                {'time': datetime.now().isoformat(), 'level': 'INFO', 'message': f'任务创建成功，任务ID: {task_id}'}
            ]
        }
        
        with self.task_lock:
            self.tasks[task_id] = task
            self.task_queues[task_id] = queue.Queue()
        
        return task
    
    def get_task(self, task_id):
        with self.task_lock:
            return self.tasks.get(task_id)
    
    def update_task(self, task_id, updates):
        with self.task_lock:
            if task_id in self.tasks:
                self.tasks[task_id].update(updates)
                self.tasks[task_id]['updatedAt'] = int(time.time() * 1000)
                # 通知等待的线程
                if task_id in self.task_queues:
                    self.task_queues[task_id].put(1)
                return True
            return False
    
    def add_log(self, task_id, level, message):
        with self.task_lock:
            if task_id in self.tasks:
                log_entry = {
                    'time': datetime.now().isoformat(),
                    'level': level,
                    'message': message
                }
                self.tasks[task_id]['logs'].append(log_entry)
                return True
            return False
    
    def get_tasks(self):
        with self.task_lock:
            return list(self.tasks.values())
    
    def wait_for_update(self, task_id, timeout=30):
        if task_id in self.task_queues:
            try:
                self.task_queues[task_id].get(timeout=timeout)
                return True
            except queue.Empty:
                return False
        return False
    
    def remove_task(self, task_id):
        with self.task_lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
            if task_id in self.task_queues:
                del self.task_queues[task_id]

# 全局任务管理器
task_manager = TaskManager()

# API客户端类
class Sora2APIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or API_KEY
        self.base_url = API_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def generate_script(self, theme, count):
        """调用Chat API生成视频脚本"""
        endpoint = f"{self.base_url}/v1/chat/completions"
        
        # 构建系统提示词
        system_prompt = f"""
        你是一个专业的视频内容策划师。请根据用户提供的主题，生成{count}个完整的视频生产方案，每个方案包含：
        1. 详细的视频提示词（必须非常具体，包含以下元素）：
           - 视觉元素：场景、角色外观、动作、表情、镜头运动
           - 风格：画风、色调、光影效果
           - 音频元素：背景音乐风格、音效描述
           - 节奏：视频的整体节奏和氛围
           注意：如果是讲解类内容，请描述角色的讲解动作和表情，营造知识分享的氛围
        2. 吸引人的视频标题（简洁有力，10-20字）
        3. 专业的视频简介（50-100字，概括视频内容和亮点）

        请确保每个方案都是独特的，避免重复。返回格式必须是JSON数组，每个元素包含prompt、title和description字段。
        """
        
        payload = {
            "model": "claude-sonnet-4-5-20250929",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"视频主题：{theme}"}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # 解析生成的内容
            content = result['choices'][0]['message']['content']
            
            # 尝试提取JSON
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                scripts = json.loads(json_match.group())
                # 确保返回的数据格式正确
                for i in range(len(scripts)):
                    if i >= count:
                        break
                    if 'prompt' not in scripts[i]:
                        scripts[i]['prompt'] = scripts[i].get('提示词', '')
                    if 'title' not in scripts[i]:
                        scripts[i]['title'] = scripts[i].get('标题', f'视频{i+1}')
                    if 'description' not in scripts[i]:
                        scripts[i]['description'] = scripts[i].get('简介', '')
                return scripts[:count]
            
            # 如果没有找到JSON，返回默认数据
            default_scripts = []
            for i in range(count):
                default_scripts.append({
                    'prompt': f"{theme} - 场景{i+1}：详细展示相关内容，高清画质，专业构图",
                    'title': f"{theme} - 精彩内容{i+1}",
                    'description': f"这是关于{theme}的精彩视频内容，展示了丰富的相关信息和视觉效果。"
                })
            return default_scripts
            
        except Exception as e:
            print(f"生成脚本失败: {e}")
            # 返回默认数据
            default_scripts = []
            for i in range(count):
                default_scripts.append({
                    'prompt': f"{theme} - 场景{i+1}：详细展示相关内容，高清画质，专业构图",
                    'title': f"{theme} - 精彩内容{i+1}",
                    'description': f"这是关于{theme}的精彩视频内容，展示了丰富的相关信息和视觉效果。"
                })
            return default_scripts
    
    def create_video_task(self, prompt, duration=10, aspect_ratio="16:9", watermark=False):
        """创建视频生成任务"""
        endpoint = f"{self.base_url}/v1/videos/generations"
        
        payload = {
            "model": "sora-2",
            "prompt": prompt,
            "duration": int(duration),
            "aspect_ratio": aspect_ratio,
            "watermark": watermark
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get('data', [])[0] if result.get('data') else None
        except Exception as e:
            print(f"创建视频任务失败: {e}")
            raise
    
    def get_task_status(self, task_id):
        """获取任务状态"""
        endpoint = f"{self.base_url}/v1/tasks/{task_id}"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取任务状态失败: {e}")
            raise

# 视频生成工作器
class VideoGenerationWorker:
    def __init__(self):
        self.client = Sora2APIClient()
        self.workers = []
        self.stop_event = threading.Event()
    
    def start_worker(self, task_id, task_data):
        worker_thread = threading.Thread(target=self._process_task, args=(task_id, task_data))
        worker_thread.daemon = True
        worker_thread.start()
        self.workers.append(worker_thread)
        return worker_thread
    
    def _process_task(self, task_id, task_data):
        """处理单个视频生成任务"""
        try:
            # 更新任务状态为处理中
            task_manager.update_task(task_id, {'status': TASK_STATUS['PROCESSING']})
            task_manager.add_log(task_id, 'INFO', '开始处理视频生成任务')
            
            scripts = task_data.get('scripts', [])
            duration = task_data.get('duration', '10')
            aspect_ratio = task_data.get('aspectRatio', '16:9')
            
            generated_videos = []
            total = len(scripts)
            has_errors = False  # 新增标志变量，跟踪是否有错误发生
            
            for i, script in enumerate(scripts):
                if self.stop_event.is_set():
                    task_manager.update_task(task_id, {'status': TASK_STATUS['CANCELLED']})
                    task_manager.add_log(task_id, 'INFO', '任务已取消')
                    return
                
                try:
                    # 创建单个视频任务
                    task_manager.add_log(task_id, 'INFO', f'正在生成第{i+1}/{total}个视频：{script.get("title", "未命名")}')
                    
                    # 调用Sora2 API创建视频任务
                    video_task = self.client.create_video_task(
                        prompt=script.get('prompt', ''),
                        duration=duration,
                        aspect_ratio=aspect_ratio
                    )
                    
                    if video_task and 'task_id' in video_task:
                        # 轮询任务状态
                        while True:
                            if self.stop_event.is_set():
                                task_manager.update_task(task_id, {'status': TASK_STATUS['CANCELLED']})
                                task_manager.add_log(task_id, 'INFO', '任务已取消')
                                return

                            status_response = self.client.get_task_status(video_task['task_id'])
                            # 从响应中提取data字段
                            status_info = status_response.get('data', {})

                            if status_info.get('status') == 'completed':
                                # 获取生成的视频
                                videos = status_info.get('result', {}).get('videos', [])
                                if videos:
                                    video_url = videos[0].get('url', '')

                                    # 自动保存到素材库
                                    task_manager.add_log(task_id, 'INFO', f'正在将第{i+1}个视频保存到素材库...')
                                    material_path = save_video_to_material(
                                        video_url=video_url,
                                        title=script.get('title', f'视频{i+1}'),
                                        description=script.get('description', '')
                                    )

                                    if material_path:
                                        task_manager.add_log(task_id, 'INFO', f'第{i+1}个视频已保存到素材库: {material_path}')
                                    else:
                                        task_manager.add_log(task_id, 'WARNING', f'第{i+1}个视频保存到素材库失败，但视频URL仍可用')

                                    generated_videos.append({
                                        'title': script.get('title', f'视频{i+1}'),
                                        'description': script.get('description', ''),
                                        'url': video_url,
                                        'thumbnail': videos[0].get('thumbnail', ''),
                                        'material_path': material_path  # 添加素材库路径
                                    })
                                break
                            elif status_info.get('status') == 'failed':
                                error_msg = status_info.get('error', {}).get('message', '视频生成失败')
                                task_manager.add_log(task_id, 'ERROR', f'第{i+1}个视频生成失败: {error_msg}')
                                has_errors = True  # 标记有错误发生
                                break
                            
                            # 更新进度
                            current_progress = int(((i + 0.5) / total) * 100)
                            task_manager.update_task(task_id, {'progress': current_progress})
                            
                            # 等待一段时间后继续查询
                            time.sleep(5)
                    else:
                        has_errors = True  # 如果没有获取到有效的video_task，标记有错误
                        task_manager.add_log(task_id, 'ERROR', f'无法为第{i+1}个视频创建任务')
                    
                    # 更新总体进度
                    progress = int(((i + 1) / total) * 100)
                    task_manager.update_task(task_id, {'progress': progress})
                    task_manager.add_log(task_id, 'INFO', f'第{i+1}/{total}个视频处理完成')
                    
                except Exception as e:
                    error_msg = str(e)
                    task_manager.add_log(task_id, 'ERROR', f'处理第{i+1}个视频时出错: {error_msg}')
                    has_errors = True  # 标记有错误发生
            
            # 根据是否有错误决定最终状态
            completed_at = int(time.time() * 1000)
            if has_errors:
                # 如果有错误发生，设置适当的状态
                if len(generated_videos) == 0:
                    # 如果没有生成任何视频，则任务整体失败
                    task_manager.update_task(task_id, {
                        'status': TASK_STATUS['FAILED'],
                        'progress': 100,
                        'completedAt': completed_at,
                        'videos': generated_videos,
                        'error': '所有视频生成失败'
                    })
                    task_manager.add_log(task_id, 'ERROR', '视频生成任务失败，无法生成任何视频')
                else:
                    # 如果部分视频生成成功，则任务为部分成功
                    task_manager.update_task(task_id, {
                        'status': 'partial_success',  # 使用自定义状态表示部分成功
                        'progress': 100,
                        'completedAt': completed_at,
                        'videos': generated_videos,
                        'error': '部分视频生成失败'
                    })
                    task_manager.add_log(task_id, 'SUCCESS', f'视频生成任务部分完成，成功生成{len(generated_videos)}个视频')
            else:
                # 所有视频都成功生成
                task_manager.update_task(task_id, {
                    'status': TASK_STATUS['COMPLETED'],
                    'progress': 100,
                    'completedAt': completed_at,
                    'videos': generated_videos
                })
                task_manager.add_log(task_id, 'SUCCESS', f'视频生成任务完成，成功生成{len(generated_videos)}个视频')
            
        except Exception as e:
            error_msg = str(e)
            task_manager.update_task(task_id, {
                'status': TASK_STATUS['FAILED'],
                'error': error_msg
            })
            task_manager.add_log(task_id, 'ERROR', f'任务执行失败: {error_msg}')
    
    def stop(self):
        self.stop_event.set()
        for worker in self.workers:
            if worker.is_alive():
                worker.join(timeout=5)

# 全局工作器
video_worker = VideoGenerationWorker()

# 主要功能函数
def generate_video_scripts(theme, count):
    """生成视频脚本"""
    client = Sora2APIClient()
    scripts = client.generate_script(theme, count)
    return scripts

def create_video_task(task_data):
    """创建视频生成任务"""
    # 创建任务记录
    task = task_manager.create_task(task_data)
    
    # 启动工作线程
    video_worker.start_worker(task['taskId'], task_data)
    
    return task

def get_task_info(task_id):
    """获取任务信息"""
    return task_manager.get_task(task_id)

def get_all_tasks():
    """获取所有任务"""
    return task_manager.get_tasks()

def cancel_task(task_id):
    """取消任务"""
    task = task_manager.get_task(task_id)
    if task and task['status'] in [TASK_STATUS['PENDING'], TASK_STATUS['PROCESSING']]:
        task_manager.update_task(task_id, {'status': TASK_STATUS['CANCELLED']})
        task_manager.add_log(task_id, 'INFO', '任务已取消')
        return True
    return False

def get_task_logs(task_id):
    """获取任务日志"""
    task = task_manager.get_task(task_id)
    if task:
        return task.get('logs', [])
    return []