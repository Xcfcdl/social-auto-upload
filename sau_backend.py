import asyncio
import os
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from queue import Queue
from flask_cors import CORS
from myUtils.auth import check_cookie
from flask import Flask, request, jsonify, Response, render_template, send_from_directory, stream_with_context
from conf import BASE_DIR
from myUtils.login import get_tencent_cookie, douyin_cookie_gen, get_ks_cookie, xiaohongshu_cookie_gen
from myUtils.postVideo import post_video_tencent, post_video_DouYin, post_video_ks, post_video_xhs
from myUtils.sora2_generator import (
    generate_video_scripts, create_video_task, get_task_info,
    get_all_tasks, cancel_task, get_task_logs, task_manager
)

active_queues = {}
app = Flask(__name__)

#允许所有来源跨域访问
CORS(app)

# 限制上传文件大小为160MB
app.config['MAX_CONTENT_LENGTH'] = 160 * 1024 * 1024

# 获取当前目录（假设 index.html 和 assets 在这里）
current_dir = os.path.dirname(os.path.abspath(__file__))

# 处理所有静态资源请求（未来打包用）
@app.route('/assets/<filename>')
def custom_static(filename):
    return send_from_directory(os.path.join(current_dir, 'assets'), filename)

# 处理 favicon.ico 静态资源（未来打包用）
@app.route('/favicon.ico')
def favicon(filename):
    return send_from_directory(os.path.join(current_dir, 'assets'), 'favicon.ico')

# （未来打包用）
@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({
            "code": 200,
            "data": None,
            "msg": "No file part in the request"
        }), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "code": 200,
            "data": None,
            "msg": "No selected file"
        }), 400
    try:
        # 保存文件到指定位置
        uuid_v1 = uuid.uuid1()
        print(f"UUID v1: {uuid_v1}")
        filepath = Path(BASE_DIR / "videoFile" / f"{uuid_v1}_{file.filename}")
        file.save(filepath)
        return jsonify({"code":200,"msg": "File uploaded successfully", "data": f"{uuid_v1}_{file.filename}"}), 200
    except Exception as e:
        return jsonify({"code":200,"msg": str(e),"data":None}), 500

@app.route('/getFile', methods=['GET'])
def get_file():
    # 获取 filename 参数
    filename = request.args.get('filename')

    if not filename:
        return {"error": "filename is required"}, 400

    # 防止路径穿越攻击
    if '..' in filename or filename.startswith('/'):
        return {"error": "Invalid filename"}, 400

    # 拼接完整路径
    file_path = str(Path(BASE_DIR / "videoFile"))

    # 返回文件
    return send_from_directory(file_path,filename)


@app.route('/uploadSave', methods=['POST'])
def upload_save():
    if 'file' not in request.files:
        return jsonify({
            "code": 400,
            "data": None,
            "msg": "No file part in the request"
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "code": 400,
            "data": None,
            "msg": "No selected file"
        }), 400

    # 获取表单中的自定义文件名（可选）
    custom_filename = request.form.get('filename', None)
    if custom_filename:
        filename = custom_filename + "." + file.filename.split('.')[-1]
    else:
        filename = file.filename

    # 获取元数据（可选）
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    tags = request.form.get('tags', '')

    try:
        # 生成 UUID v1
        uuid_v1 = uuid.uuid1()
        print(f"UUID v1: {uuid_v1}")

        # 构造文件名和路径
        final_filename = f"{uuid_v1}_{filename}"
        filepath = Path(BASE_DIR / "videoFile" / f"{uuid_v1}_{filename}")

        # 保存文件
        file.save(filepath)

        with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO file_records (filename, filesize, file_path, title, description, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                filename,
                round(float(os.path.getsize(filepath)) / (1024 * 1024), 2),
                final_filename,
                title,
                description,
                tags
            ))
            conn.commit()
            print("Upload file recorded")

        return jsonify({
            "code": 200,
            "msg": "File uploaded and saved successfully",
            "data": {
                "filename": filename,
                "filepath": final_filename
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": str("upload failed!"),
            "data": None
        }), 500

@app.route('/getFiles', methods=['GET'])
def get_all_files():
    try:
        # 使用 with 自动管理数据库连接
        with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
            conn.row_factory = sqlite3.Row  # 允许通过列名访问结果
            cursor = conn.cursor()

            # 查询所有记录
            cursor.execute("SELECT * FROM file_records")
            rows = cursor.fetchall()

            # 将结果转为字典列表
            data = [dict(row) for row in rows]

        return jsonify({
            "code": 200,
            "msg": "success",
            "data": data
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": str("get file failed!"),
            "data": None
        }), 500


@app.route("/getValidAccounts",methods=['GET'])
async def getValidAccounts():
    with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM user_info''')
        rows = cursor.fetchall()
        rows_list = [list(row) for row in rows]
        print("\n📋 当前数据表内容：")
        for row in rows:
            print(row)
        for row in rows_list:
            flag = await check_cookie(row[1],row[2])
            if not flag:
                row[4] = 0
                cursor.execute('''
                UPDATE user_info 
                SET status = ? 
                WHERE id = ?
                ''', (0,row[0]))
                conn.commit()
                print("✅ 用户状态已更新")
        for row in rows:
            print(row)
        return jsonify(
                        {
                            "code": 200,
                            "msg": None,
                            "data": rows_list
                        }),200

@app.route('/deleteFile', methods=['GET'])
def delete_file():
    file_id = request.args.get('id')

    if not file_id or not file_id.isdigit():
        return jsonify({
            "code": 400,
            "msg": "Invalid or missing file ID",
            "data": None
        }), 400

    try:
        # 获取数据库连接
        with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 查询要删除的记录
            cursor.execute("SELECT * FROM file_records WHERE id = ?", (file_id,))
            record = cursor.fetchone()

            if not record:
                return jsonify({
                    "code": 404,
                    "msg": "File not found",
                    "data": None
                }), 404

            record = dict(record)

            # 删除数据库记录
            cursor.execute("DELETE FROM file_records WHERE id = ?", (file_id,))
            conn.commit()

        return jsonify({
            "code": 200,
            "msg": "File deleted successfully",
            "data": {
                "id": record['id'],
                "filename": record['filename']
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": str("delete failed!"),
            "data": None
        }), 500

@app.route('/deleteAccount', methods=['GET'])
def delete_account():
    account_id = int(request.args.get('id'))

    try:
        # 获取数据库连接
        with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 查询要删除的记录
            cursor.execute("SELECT * FROM user_info WHERE id = ?", (account_id,))
            record = cursor.fetchone()

            if not record:
                return jsonify({
                    "code": 404,
                    "msg": "account not found",
                    "data": None
                }), 404

            record = dict(record)

            # 删除数据库记录
            cursor.execute("DELETE FROM user_info WHERE id = ?", (account_id,))
            conn.commit()

        return jsonify({
            "code": 200,
            "msg": "account deleted successfully",
            "data": None
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": str("delete failed!"),
            "data": None
        }), 500


# SSE 登录接口
@app.route('/login')
def login():
    # 1 小红书 2 视频号 3 抖音 4 快手
    type = request.args.get('type')
    # 账号名
    id = request.args.get('id')

    # 模拟一个用于异步通信的队列
    status_queue = Queue()
    active_queues[id] = status_queue

    def on_close():
        print(f"清理队列: {id}")
        del active_queues[id]
    # 启动异步任务线程
    thread = threading.Thread(target=run_async_function, args=(type,id,status_queue), daemon=True)
    thread.start()
    response = Response(sse_stream(status_queue,), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'  # 关键：禁用 Nginx 缓冲
    response.headers['Content-Type'] = 'text/event-stream'
    response.headers['Connection'] = 'keep-alive'
    return response

@app.route('/postVideo', methods=['POST'])
def postVideo():
    # 获取JSON数据
    data = request.get_json()

    # 从JSON数据中提取fileList和accountList
    file_list = data.get('fileList', [])
    account_list = data.get('accountList', [])
    type = data.get('type')
    title = data.get('title')
    tags = data.get('tags')
    category = data.get('category')
    enableTimer = data.get('enableTimer')
    if category == 0:
        category = None
    productLink = data.get('productLink', '')
    productTitle = data.get('productTitle', '')
    thumbnail_path = data.get('thumbnail', '')

    videos_per_day = data.get('videosPerDay')
    daily_times = data.get('dailyTimes')
    start_days = data.get('startDays')
    # 打印获取到的数据（仅作为示例）
    print("File List:", file_list)
    print("Account List:", account_list)
    match type:
        case 1:
            post_video_xhs(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times,
                               start_days)
        case 2:
            post_video_tencent(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times,
                               start_days)
        case 3:
            post_video_DouYin(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times,
                      start_days, thumbnail_path, productLink, productTitle)
        case 4:
            post_video_ks(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times,
                      start_days)
    # 返回响应给客户端
    return jsonify(
        {
            "code": 200,
            "msg": None,
            "data": None
        }), 200


@app.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """获取Dashboard统计数据"""
    try:
        with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 账号统计
            cursor.execute('SELECT COUNT(*) as total FROM user_info')
            account_total = cursor.fetchone()['total']

            cursor.execute('SELECT COUNT(*) as normal FROM user_info WHERE status = 1')
            account_normal = cursor.fetchone()['normal']

            account_abnormal = account_total - account_normal

            # 平台统计
            cursor.execute('SELECT type, COUNT(*) as count FROM user_info GROUP BY type')
            platform_rows = cursor.fetchall()
            platform_stats = {
                'kuaishou': 0,
                'douyin': 0,
                'channels': 0,
                'xiaohongshu': 0
            }

            for row in platform_rows:
                type_val = row['type']
                count = row['count']
                if type_val == 1:
                    platform_stats['xiaohongshu'] = count
                elif type_val == 2:
                    platform_stats['channels'] = count
                elif type_val == 3:
                    platform_stats['douyin'] = count
                elif type_val == 4:
                    platform_stats['kuaishou'] = count

            platform_total = sum(platform_stats.values())

            # 任务统计
            cursor.execute('SELECT COUNT(*) as total FROM task_records')
            task_total = cursor.fetchone()['total']

            cursor.execute('SELECT COUNT(*) as completed FROM task_records WHERE status = "已完成"')
            task_completed = cursor.fetchone()['completed']

            cursor.execute('SELECT COUNT(*) as in_progress FROM task_records WHERE status = "进行中"')
            task_in_progress = cursor.fetchone()['in_progress']

            cursor.execute('SELECT COUNT(*) as failed FROM task_records WHERE status = "已失败"')
            task_failed = cursor.fetchone()['failed']

            # 内容统计（假设所有上传的文件都是已发布的内容，暂时没有草稿状态）
            cursor.execute('SELECT COUNT(*) as total FROM file_records')
            content_total = cursor.fetchone()['total']

            # 最近任务列表（最近5条）
            cursor.execute('''
                SELECT
                    id,
                    title,
                    platform,
                    account_name,
                    status,
                    create_time
                FROM task_records
                ORDER BY create_time DESC
                LIMIT 5
            ''')
            recent_tasks_rows = cursor.fetchall()

            platform_map = {
                1: '小红书',
                2: '视频号',
                3: '抖音',
                4: '快手'
            }

            recent_tasks = []
            for row in recent_tasks_rows:
                recent_tasks.append({
                    'id': row['id'],
                    'title': row['title'],
                    'platform': platform_map.get(row['platform'], '未知'),
                    'account': row['account_name'] or '未指定',
                    'createTime': row['create_time'],
                    'status': row['status']
                })

            return jsonify({
                'code': 200,
                'msg': 'success',
                'data': {
                    'accountStats': {
                        'total': account_total,
                        'normal': account_normal,
                        'abnormal': account_abnormal
                    },
                    'platformStats': {
                        'total': platform_total,
                        **platform_stats
                    },
                    'taskStats': {
                        'total': task_total,
                        'completed': task_completed,
                        'inProgress': task_in_progress,
                        'failed': task_failed
                    },
                    'contentStats': {
                        'total': content_total,
                        'published': content_total,  # 暂时假设所有都是已发布
                        'draft': 0  # 暂时没有草稿功能
                    },
                    'recentTasks': recent_tasks
                }
            }), 200

    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取统计数据失败: {str(e)}',
            'data': None
        }), 500


@app.route('/updateUserinfo', methods=['POST'])
def updateUserinfo():
    # 获取JSON数据
    data = request.get_json()

    # 从JSON数据中提取 type 和 userName
    user_id = data.get('id')
    type = data.get('type')
    userName = data.get('userName')
    try:
        # 获取数据库连接
        with sqlite3.connect(Path(BASE_DIR / "db" / "database.db")) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 更新数据库记录
            cursor.execute('''
                           UPDATE user_info
                           SET type     = ?,
                               userName = ?
                           WHERE id = ?;
                           ''', (type, userName, user_id))
            conn.commit()

        return jsonify({
            "code": 200,
            "msg": "account update successfully",
            "data": None
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": str("update failed!"),
            "data": None
        }), 500

@app.route('/postVideoBatch', methods=['POST'])
def postVideoBatch():
    data_list = request.get_json()

    if not isinstance(data_list, list):
        return jsonify({"error": "Expected a JSON array"}), 400
    for data in data_list:
        # 从JSON数据中提取fileList和accountList
        file_list = data.get('fileList', [])
        account_list = data.get('accountList', [])
        type = data.get('type')
        title = data.get('title')
        tags = data.get('tags')
        category = data.get('category')
        enableTimer = data.get('enableTimer')
        if category == 0:
            category = None
        productLink = data.get('productLink', '')
        productTitle = data.get('productTitle', '')

        videos_per_day = data.get('videosPerDay')
        daily_times = data.get('dailyTimes')
        start_days = data.get('startDays')
        # 打印获取到的数据（仅作为示例）
        print("File List:", file_list)
        print("Account List:", account_list)
        match type:
            case 1:
                return
            case 2:
                post_video_tencent(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times,
                                   start_days)
            case 3:
                post_video_DouYin(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times,
                          start_days, productLink, productTitle)
            case 4:
                post_video_ks(title, file_list, tags, account_list, category, enableTimer, videos_per_day, daily_times,
                          start_days)
    # 返回响应给客户端
    return jsonify(
        {
            "code": 200,
            "msg": None,
            "data": None
        }), 200

# 包装函数：在线程中运行异步函数
def run_async_function(type,id,status_queue):
    match type:
        case '1':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(xiaohongshu_cookie_gen(id, status_queue))
            loop.close()
        case '2':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(get_tencent_cookie(id,status_queue))
            loop.close()
        case '3':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(douyin_cookie_gen(id,status_queue))
            loop.close()
        case '4':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(get_ks_cookie(id,status_queue))
            loop.close()

# SSE 流生成器函数
def sse_stream(status_queue):
    while True:
        if not status_queue.empty():
            msg = status_queue.get()
            yield f"data: {msg}\n\n"
        else:
            # 避免 CPU 占满
            time.sleep(0.1)

# Sora2 视频生成相关接口

@app.route('/sora2/generate-script', methods=['POST'])
def generate_script():
    try:
        data = request.get_json()
        theme = data.get('theme', '')
        count = data.get('count', 1)
        
        if not theme:
            return jsonify({
                'code': 400,
                'msg': '主题不能为空',
                'data': None
            })
        
        if count < 1 or count > 20:
            return jsonify({
                'code': 400,
                'msg': '生成数量必须在1-20之间',
                'data': None
            })
        
        # 生成视频脚本
        scripts = generate_video_scripts(theme, count)
        
        return jsonify({
            'code': 200,
            'msg': '脚本生成成功',
            'data': {
                'scripts': scripts,
                'count': len(scripts)
            }
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'生成脚本失败: {str(e)}',
            'data': None
        })

@app.route('/sora2/create-task', methods=['POST'])
def create_sora2_task():
    try:
        data = request.get_json()
        
        # 验证必要参数
        if not data.get('theme'):
            return jsonify({
                'code': 400,
                'msg': '主题不能为空',
                'data': None
            })
        
        if not data.get('scripts'):
            return jsonify({
                'code': 400,
                'msg': '脚本数据不能为空',
                'data': None
            })
        
        # 创建视频任务
        task = create_video_task(data)
        
        return jsonify({
            'code': 200,
            'msg': '任务创建成功',
            'data': task
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'创建任务失败: {str(e)}',
            'data': None
        })

@app.route('/sora2/task-status/<task_id>', methods=['GET'])
def get_sora2_task_status(task_id):
    try:
        task = get_task_info(task_id)
        
        if not task:
            return jsonify({
                'code': 404,
                'msg': '任务不存在',
                'data': None
            })
        
        # 构造符合API规范的响应格式
        api_response = {
            'id': task.get('taskId', task_id),
            'status': task.get('status'),
            'progress': task.get('progress', 0),
            'actual_time': task.get('actual_time', 0),
            'completed': task.get('completed', 0),
            'created': task.get('created', 0),
            'estimated_time': task.get('estimated_time', 0)
        }
        
        # 仅当状态为completed时返回result
        if task.get('status') == 'completed':
            api_response['result'] = {
                'videos': task.get('videos', [])
            }
        
        return jsonify({
            'code': 200,
            'msg': '获取任务状态成功',
            'data': api_response
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取任务状态失败: {str(e)}',
            'data': None
        })

@app.route('/sora2/task-list', methods=['GET'])
def get_sora2_task_list():
    try:
        tasks = get_all_tasks()
        
        # 按创建时间倒序排序
        tasks.sort(key=lambda x: x['createdAt'], reverse=True)
        
        return jsonify({
            'code': 200,
            'msg': '获取任务列表成功',
            'data': tasks
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取任务列表失败: {str(e)}',
            'data': None
        })

@app.route('/sora2/cancel-task/<task_id>', methods=['POST'])
def cancel_sora2_task(task_id):
    try:
        success = cancel_task(task_id)
        
        if success:
            return jsonify({
                'code': 200,
                'msg': '任务取消成功',
                'data': None
            })
        else:
            task = get_task_info(task_id)
            if not task:
                return jsonify({
                    'code': 404,
                    'msg': '任务不存在',
                    'data': None
                })
            else:
                return jsonify({
                    'code': 400,
                    'msg': '任务已完成或已取消，无法取消',
                    'data': None
                })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'取消任务失败: {str(e)}',
            'data': None
        })

@app.route('/sora2/task-logs/<task_id>', methods=['GET'])
def get_sora2_task_logs(task_id):
    try:
        logs = get_task_logs(task_id)
        
        return jsonify({
            'code': 200,
            'msg': '获取任务日志成功',
            'data': logs
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'获取任务日志失败: {str(e)}',
            'data': None
        })

@app.route('/sora2/download/<task_id>', methods=['GET'])
def download_sora2_video(task_id):
    try:
        task = get_task_info(task_id)
        
        if not task:
            return jsonify({
                'code': 404,
                'msg': '任务不存在',
                'data': None
            })
        
        if task['status'] != 'completed':
            return jsonify({
                'code': 400,
                'msg': '任务未完成，无法下载',
                'data': None
            })
        
        # 这里应该实现视频文件的下载逻辑
        # 由于实际的视频文件可能存储在外部服务，这里返回第一个视频的URL
        if task['videos']:
            first_video_url = task['videos'][0]['url']
            # 如果是生产环境，可能需要实现文件代理下载
            return jsonify({
                'code': 200,
                'msg': '获取下载链接成功',
                'data': {
                    'downloadUrl': first_video_url,
                    'videoCount': len(task['videos'])
                }
            })
        else:
            return jsonify({
                'code': 400,
                'msg': '没有可下载的视频',
                'data': None
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'下载视频失败: {str(e)}',
            'data': None
        })

@app.route('/sora2/task-stream/<task_id>', methods=['GET'])
def stream_task_status(task_id):
    """流式返回任务状态更新"""
    def generate():
        while True:
            task = get_task_info(task_id)
            if not task:
                yield f'data: {json.dumps({"error": "任务不存在"})}\n\n'
                break
            
            # 发送任务状态
            yield f'data: {json.dumps(task)}\n\n'
            
            # 如果任务已完成或失败，停止流
            if task['status'] in ['completed', 'failed', 'cancelled']:
                break
            
            # 等待任务更新
            updated = task_manager.wait_for_update(task_id, timeout=10)
            if not updated:
                # 定期发送保持连接
                pass
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5409)
