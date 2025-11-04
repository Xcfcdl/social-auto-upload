@echo off

echo ====================================
echo 正在启动 Social Auto Upload 系统
echo ====================================

:: 定义端口号
set "BACKEND_PORT=5409"
set "FRONTEND_PORT=5173"

:: 检查并关闭占用后端端口的进程
echo 检查端口 %BACKEND_PORT% 是否被占用...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%BACKEND_PORT%') do (
    echo 发现端口 %BACKEND_PORT% 被进程 %%a 占用，正在关闭...
    taskkill /PID %%a /F >nul 2>&1
    if %errorlevel% equ 0 (
        echo 成功关闭进程 %%a
    ) else (
        echo 关闭进程 %%a 失败，请手动关闭
    )
)

:: 检查并关闭占用前端端口的进程
echo 检查端口 %FRONTEND_PORT% 是否被占用...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%FRONTEND_PORT%') do (
    echo 发现端口 %FRONTEND_PORT% 被进程 %%a 占用，正在关闭...
    taskkill /PID %%a /F >nul 2>&1
    if %errorlevel% equ 0 (
        echo 成功关闭进程 %%a
    ) else (
        echo 关闭进程 %%a 失败，请手动关闭
    )
)

:: 等待1秒，确保进程已完全关闭
timeout /t 1 /nobreak >nul

:: 创建新窗口并启动后端服务
echo 启动后端服务...
start "后端服务" cmd /k "cd /d d:\Projects\social-auto-upload && python sau_backend.py"

:: 等待2秒，确保后端开始启动
timeout /t 2 /nobreak >nul

:: 创建新窗口并启动前端服务
echo 启动前端服务...
start "前端服务" cmd /k "cd /d d:\Projects\social-auto-upload\sau_frontend && npm run dev"

echo 启动完成！
echo 请等待服务完全启动...
echo 后端服务将在 http://localhost:%BACKEND_PORT% 运行
echo 前端服务将在 http://localhost:%FRONTEND_PORT% 或其他提示端口运行
echo ====================================