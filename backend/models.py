from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ExcelItem(BaseModel):
    """Excel表格中的项目数据模型"""
    序号: Optional[int] = Field(None, description="项目序号，自动生成")
    内容: str = Field(..., description="项目内容，必填")
    材料: Optional[str] = Field(None, description="材料")
    规格尺寸: Optional[float] = Field(None, description="规格尺寸")
    数量: float = Field(..., gt=0, description="数量，必须大于0")
    价格: float = Field(..., ge=0, description="价格，不能为负")
    总价: Optional[float] = Field(None, description="总价 = 数量 * 价格")
    项目图片: Optional[str] = Field(None, description="图片路径")
    经办人: Optional[str] = Field(None, description="经办人")
    备注: Optional[str] = Field(None, description="备注")

class ExcelFile(BaseModel):
    """Excel文件信息"""
    name: str = Field(..., description="文件名")
    path: str = Field(..., description="文件路径")
    size: Optional[int] = Field(None, description="文件大小")
    modified: Optional[datetime] = Field(None, description="修改时间")

class ExcelData(BaseModel):
    """Excel数据响应"""
    file_name: str = Field(..., description="文件名")
    records: List[ExcelItem] = Field(..., description="数据记录")
    total: float = Field(..., description="总价合计")

class SaveRequest(BaseModel):
    """保存请求"""
    records: List[ExcelItem] = Field(..., description="要保存的数据记录")

class UndoResponse(BaseModel):
    """撤回响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
