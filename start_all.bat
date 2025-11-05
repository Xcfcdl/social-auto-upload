@echo off

echo ====================================
echo Starting Social Auto Upload System
echo ====================================

:: Define port numbers
set "BACKEND_PORT=5409"
set "FRONTEND_PORT=5173"

:: Check and close processes occupying backend port
echo Checking if port %BACKEND_PORT% is in use...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%BACKEND_PORT%') do (
    echo Found port %BACKEND_PORT% occupied by process %%a, closing...
    taskkill /PID %%a /F >nul 2>&1
    if %errorlevel% equ 0 (
        echo Successfully closed process %%a
    ) else (
        echo Failed to close process %%a, please close manually
    )
)

:: Check and close processes occupying frontend port
echo Checking if port %FRONTEND_PORT% is in use...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%FRONTEND_PORT%') do (
    echo Found port %FRONTEND_PORT% occupied by process %%a, closing...
    taskkill /PID %%a /F >nul 2>&1
    if %errorlevel% equ 0 (
        echo Successfully closed process %%a
    ) else (
        echo Failed to close process %%a, please close manually
    )
)

:: Wait 1 second to ensure processes are fully closed
timeout /t 1 /nobreak >nul

:: Create new window and start backend service
echo Starting backend service...
start "Backend Service" cmd /k "cd /d d:\Projects\social-auto-upload && python sau_backend.py"

:: Wait 2 seconds to ensure backend starts
timeout /t 2 /nobreak >nul

:: Create new window and start frontend service
echo Starting frontend service...
start "Frontend Service" cmd /k "cd /d d:\Projects\social-auto-upload\sau_frontend && npm run dev"

echo Startup complete!
echo Please wait for services to fully start...
echo Backend service will run at http://localhost:%BACKEND_PORT%
echo Frontend service will run at http://localhost:%FRONTEND_PORT% or other prompted port
echo ====================================