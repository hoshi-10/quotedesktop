from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

try:
    # 当作为模块导入时使用相对导入
    from .models import ExcelData, ExcelFile, SaveRequest, UndoResponse
    from .excel_service import excel_service
except ImportError:
    # 当直接运行时使用绝对导入
    from models import ExcelData, ExcelFile, SaveRequest, UndoResponse
    from excel_service import excel_service

app = FastAPI(
    title="报价桌面系统API",
    description="轻量级桌面报价管理系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "报价桌面系统API",
        "version": "1.0.0",
        "endpoints": {
            "GET /files": "获取所有Excel文件列表",
            "GET /read/{file}": "读取指定Excel文件数据",
            "POST /save/{file}": "保存数据到指定Excel文件",
            "POST /undo/{file}": "撤回上次保存操作"
        }
    }

@app.get("/files", response_model=List[str])
async def get_files():
    """
    获取所有Excel文件列表
    
    返回data/excel_files目录下所有.xlsx文件
    """
    try:
        files = excel_service.list_excel_files()
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")

@app.get("/read/{file_name}", response_model=ExcelData)
async def read_file(file_name: str):
    """
    读取指定Excel文件数据
    
    - **file_name**: Excel文件名（需包含.xlsx扩展名）
    """
    # 安全检查：防止路径遍历
    if ".." in file_name or "/" in file_name or "\\" in file_name:
        raise HTTPException(status_code=400, detail="文件名不合法")
    
    if not file_name.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="文件必须是.xlsx格式")
    
    try:
        data = excel_service.read_excel(file_name)
        return ExcelData(
            file_name=file_name,
            records=data["records"],
            total=data["total"]
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"文件不存在: {file_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取文件失败: {str(e)}")

@app.post("/save/{file_name}")
async def save_file(file_name: str, request: SaveRequest):
    """
    保存数据到指定Excel文件
    
    - **file_name**: Excel文件名（需包含.xlsx扩展名）
    - **request**: 包含要保存的数据记录
    """
    # 安全检查：防止路径遍历
    if ".." in file_name or "/" in file_name or "\\" in file_name:
        raise HTTPException(status_code=400, detail="文件名不合法")
    
    if not file_name.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="文件必须是.xlsx格式")
    
    try:
        # 转换为字典列表
        records = [item.dict() for item in request.records]
        
        success = excel_service.save_excel(file_name, records)
        
        if success:
            return {
                "success": True,
                "message": f"文件 {file_name} 保存成功",
                "file_name": file_name
            }
        else:
            raise HTTPException(status_code=500, detail="保存失败")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"数据验证失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件失败: {str(e)}")

@app.post("/undo/{file_name}", response_model=UndoResponse)
async def undo_file(file_name: str):
    """
    撤回上次保存操作
    
    - **file_name**: Excel文件名（需包含.xlsx扩展名）
    """
    # 安全检查：防止路径遍历
    if ".." in file_name or "/" in file_name or "\\" in file_name:
        raise HTTPException(status_code=400, detail="文件名不合法")
    
    if not file_name.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="文件必须是.xlsx格式")
    
    try:
        success = excel_service.undo(file_name)
        
        if success:
            return UndoResponse(
                success=True,
                message=f"文件 {file_name} 已撤回上次保存"
            )
        else:
            return UndoResponse(
                success=False,
                message=f"无法撤回 {file_name}，没有备份文件"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"撤回操作失败: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "quotedesktop-backend"}

if __name__ == "__main__":
    import sys
    import subprocess
    from pathlib import Path
    
    print("=" * 60)
    print("报价桌面系统 - 后端服务")
    print("=" * 60)
    
    # 检查并安装依赖
    print("\n检查Python依赖...")
    required_packages = [
        "fastapi",
        "uvicorn[standard]", 
        "pandas",
        "openpyxl",
        "pydantic"
    ]
    
    missing = []
    for package in required_packages:
        package_name = package.split('[')[0] if '[' in package else package
        try:
            __import__(package_name)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"缺少依赖: {', '.join(missing)}")
        print("正在安装依赖...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("依赖安装完成")
        except subprocess.CalledProcessError:
            print("依赖安装失败，请手动运行: pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("所有依赖已安装")
    
    # 确保必要的目录存在
    print("\n检查数据目录...")
    base_dir = Path(__file__).parent.parent / "data"
    directories = [
        base_dir,
        base_dir / "backups"
    ]
    
    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {directory}")
        else:
            print(f"目录已存在: {directory}")
    
    # 启动服务
    print("\n" + "=" * 60)
    print("服务地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("健康检查: http://localhost:8000/health")
    print("按 Ctrl+C 停止服务")
    print("=" * 60 + "\n")
    
    try:
        import uvicorn
        # 直接运行时，不使用reload模式，避免模块导入问题
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n服务已停止")
        sys.exit(0)
    except Exception as e:
        print(f"启动服务失败: {e}")
        sys.exit(1)
