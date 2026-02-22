@echo off
chcp 65001 >nul
echo ========================================
echo   报价桌面系统 - 后端服务启动器
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo 检查Python依赖...
python -c "import fastapi, uvicorn, pandas, openpyxl, pydantic" >nul 2>&1
if errorlevel 1 (
    echo 依赖未安装，正在安装...
    pip install -r backend/requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
    echo 依赖安装完成
) else (
    echo 依赖已安装
)

REM 检查数据目录
echo 检查数据目录...
if not exist "data\excel_files" mkdir "data\excel_files"
if not exist "data\pictures" mkdir "data\pictures"
echo 数据目录就绪

REM 启动服务
echo.
echo 启动后端服务...
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 按 Ctrl+C 停止服务
echo.

python run_backend.py

if errorlevel 1 (
    echo [错误] 服务启动失败
    pause
    exit /b 1
)

pause
