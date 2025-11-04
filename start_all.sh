#!/bin/bash

echo "===================================="
echo "正在启动 Social Auto Upload 系统"
echo "===================================="

# 定义端口号
BACKEND_PORT=5409
FRONTEND_PORT=5173

# 检查并关闭占用后端端口的进程
echo "检查端口 $BACKEND_PORT 是否被占用..."
BACKEND_PID=$(lsof -ti:$BACKEND_PORT)
if [ ! -z "$BACKEND_PID" ]; then
    echo "发现端口 $BACKEND_PORT 被进程 $BACKEND_PID 占用，正在关闭..."
    kill -9 $BACKEND_PID 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "成功关闭进程 $BACKEND_PID"
    else
        echo "关闭进程 $BACKEND_PID 失败，请手动关闭"
    fi
fi

# 检查并关闭占用前端端口的进程
echo "检查端口 $FRONTEND_PORT 是否被占用..."
FRONTEND_PID=$(lsof -ti:$FRONTEND_PORT)
if [ ! -z "$FRONTEND_PID" ]; then
    echo "发现端口 $FRONTEND_PORT 被进程 $FRONTEND_PID 占用，正在关闭..."
    kill -9 $FRONTEND_PID 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "成功关闭进程 $FRONTEND_PID"
    else
        echo "关闭进程 $FRONTEND_PID 失败，请手动关闭"
    fi
fi

# 等待1秒，确保进程已完全关闭
sleep 1

# 启动后端服务
echo "启动后端服务..."
# 使用相对路径，更灵活
nohup python3 $(dirname "$0")/sau_backend.py > $(dirname "$0")/backend.log 2>&1 &
BACKEND_PID=$!

# 等待2秒，确保后端开始启动
sleep 2

# 启动前端服务
echo "启动前端服务..."
cd $(dirname "$0")/sau_frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

echo "启动完成！"
echo "请等待服务完全启动..."
echo "后端服务将在 http://localhost:$BACKEND_PORT 运行"
echo "前端服务将在 http://localhost:$FRONTEND_PORT 或其他提示端口运行"
echo "===================================="
echo "后端进程ID: $BACKEND_PID"
echo "前端进程ID: $FRONTEND_PID"
echo "要停止服务，请使用: kill -9 $BACKEND_PID $FRONTEND_PID"