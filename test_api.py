import requests
import json

# 测试创建任务
def test_create_task():
    url = 'http://localhost:5409/sora2/create-task'
    data = {
        'theme': '测试主题',
        'scripts': [
            {
                'title': '测试视频',
                'prompt': '测试视频描述',
                'description': '测试视频详细描述'
            }
        ],
        'duration': '10',
        'aspectRatio': '16:9'
    }
    
    print('创建测试任务...')
    response = requests.post(url, json=data)
    print(f'创建任务响应: {response.status_code}')
    result = response.json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get('code') == 200:
        return result.get('data', {}).get('taskId')
    else:
        print(f'创建任务失败: {result.get("msg")}')
        return None

# 测试查询任务状态
def test_get_task_status(task_id):
    if not task_id:
        return
    
    url = f'http://localhost:5409/sora2/task-status/{task_id}'
    print(f'\n查询任务状态 {task_id}...')
    response = requests.get(url)
    result = response.json()
    print(f'查询任务状态响应: {response.status_code}')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get('code') == 200:
        # 检查响应格式是否符合规范
        data = result.get('data', {})
        required_fields = ['id', 'status', 'progress', 'actual_time', 'completed', 'created', 'estimated_time']
        all_required_exists = True
        
        for field in required_fields:
            if field not in data:
                print(f'❌ 缺少必需字段: {field}')
                all_required_exists = False
            else:
                print(f'✅ 字段 {field} 存在')
        
        # 检查状态为completed时是否有result
        if data.get('status') == 'completed':
            if 'result' not in data:
                print('❌ 状态为completed时缺少result字段')
            else:
                print('✅ 状态为completed时包含result字段')
                if 'videos' in data['result']:
                    print('✅ 字段 result.videos 存在')
                else:
                    print('❌ 字段 result.videos 不存在')
        else:
            print('⚠️  任务状态不是completed，不需要验证result字段')
    else:
        print(f'查询任务状态失败: {result.get("msg")}')

# 直接测试指定的任务ID
def test_specific_task(task_id):
    print(f'\n=== 测试特定任务ID: {task_id} ===')
    test_get_task_status(task_id)

if __name__ == '__main__':
    print('=== API响应格式测试 ===')
    
    # 测试用户指定的任务ID
    test_specific_task('task_01K96Z1X9YZVX3DC4TXF37FVB9')
    
    # 同时测试创建新任务并查询，验证完整流程
    print('\n=== 创建新任务并测试响应格式 ===')
    task_id = test_create_task()
    if task_id:
        # 等待一会儿让任务开始处理
        import time
        time.sleep(2)
        test_get_task_status(task_id)
