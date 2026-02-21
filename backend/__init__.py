"""
报价桌面系统后端模块
"""

__version__ = "1.0.0"
__author__ = "1x1,Melsm"

from .models import ExcelItem, ExcelFile, ExcelData, SaveRequest, UndoResponse
from .excel_service import ExcelService, excel_service
from .main import app

__all__ = [
    "ExcelItem",
    "ExcelFile", 
    "ExcelData",
    "SaveRequest",
    "UndoResponse",
    "ExcelService",
    "excel_service",
    "app"
]
