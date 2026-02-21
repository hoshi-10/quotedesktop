from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import os

from .models import ExcelData, ExcelFile, SaveRequest, UndoResponse
from .excel_service import excel_service

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
    # 开发服务器
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
