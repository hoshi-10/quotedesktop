import os
import pandas as pd
import shutil
from typing import List, Dict, Any
from datetime import datetime
import time

try:
    from .models import ExcelItem
except ImportError:
    from models import ExcelItem

class ExcelService:
    """Excel文件服务类"""
    
    def __init__(self, base_dir: str = "data"):
        self.base_dir = base_dir
        # 确保目录存在
        os.makedirs(base_dir, exist_ok=True)
        # 备份目录
        self.backup_dir = os.path.join(base_dir, "backups")
        os.makedirs(self.backup_dir, exist_ok=True)
        # 文件操作重试次数
        self.max_retries = 3
        self.retry_delay = 0.5
    
    def _wait_for_file_unlock(self, file_path: str) -> bool:
        """等待文件解锁"""
        for _ in range(self.max_retries):
            try:
                # 尝试以只读模式打开文件，检查是否被锁定
                with open(file_path, 'rb') as f:
                    pass
                return True
            except (PermissionError, IOError):
                time.sleep(self.retry_delay)
        return False
    
    def list_excel_files(self) -> List[str]:
        """列出所有Excel文件"""
        try:
            return [
                f for f in os.listdir(self.base_dir)
                if f.endswith(".xlsx") 
                and f != "temp.xlsx"
                and not f.startswith("~$")  # 过滤Excel临时文件
            ]
        except FileNotFoundError:
            return []
    
    def read_excel(self, file_name: str) -> Dict[str, Any]:
        """读取Excel文件数据"""
        path = os.path.join(self.base_dir, file_name)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"文件不存在: {file_name}")
        
        df = pd.read_excel(path, dtype=str)
        
        # 清理列名：去除前后空格
        df.columns = [col.strip() if pd.notna(col) else col for col in df.columns]
        
        # 过滤掉无效行：序号列包含非数字的行（如"合计"、"单位"等）
        valid_records = []
        total = 0.0
        
        for _, row in df.iterrows():
            # 检查是否是有效的数据行
            if self._is_valid_record(row):
                item = {}
                for col in df.columns:
                    value = row[col]
                    
                    # 处理NaN值
                    if pd.isna(value):
                        item[col] = None
                    else:
                        # 清理值：去除前后空格和换行符，并替换中间的换行符为空格
                        cleaned_value = str(value).strip().replace('\n', ' ').replace('\r', ' ')
                        # 尝试转换为适当类型
                        item[col] = self._convert_value(cleaned_value, col)
                
                # 计算总价
                if item.get("数量") and item.get("价格"):
                    try:
                        quantity = float(item["数量"]) if item["数量"] else 0
                        price = float(item["价格"]) if item["价格"] else 0
                        item["总价"] = quantity * price
                        total += item["总价"]
                    except (ValueError, TypeError):
                        item["总价"] = 0
                
                valid_records.append(item)
        
        return {
            "records": valid_records,
            "total": float(total)
        }
    
    def save_excel(self, file_name: str, records: List[Dict[str, Any]]) -> bool:
        """保存数据到Excel文件"""
        path = os.path.join(self.base_dir, file_name)
        temp_path = os.path.join(self.base_dir, "temp.xlsx")
        # 备份放到备份目录，保留原始文件名并添加 .bak 后缀
        backup_path = os.path.join(self.backup_dir, f"{file_name}.bak")
        
        # 验证数据
        self._validate_records(records)
        
        # 添加序号
        records_with_index = self._add_index(records)
        
        # 转换为DataFrame
        df = pd.DataFrame(records_with_index)
        
        # 计算总价
        if "数量" in df.columns and "价格" in df.columns:
            df["总价"] = df["数量"] * df["价格"]
        
        # 备份原文件
        if os.path.exists(path):
            if not self._wait_for_file_unlock(path):
                raise RuntimeError(f"文件 {file_name} 被占用，无法访问")
            try:
                shutil.copy2(path, backup_path)
            except Exception as e:
                print(f"备份文件失败: {e}")
        
        # 写入临时文件
        df.to_excel(temp_path, index=False)
        
        # 替换原文件（先删除原文件，再重命名临时文件）
        try:
            if os.path.exists(path):
                if not self._wait_for_file_unlock(path):
                    raise RuntimeError(f"文件 {file_name} 被占用，无法访问")
                os.remove(path)
            os.rename(temp_path, path)
        except Exception as e:
            # 如果替换失败，尝试使用shutil.move
            try:
                if os.path.exists(path):
                    if not self._wait_for_file_unlock(path):
                        raise RuntimeError(f"文件 {file_name} 被占用，无法访问")
                    os.remove(path)
                shutil.move(temp_path, path)
            except Exception as e2:
                print(f"替换文件失败: {e2}")
                raise
        
        return True
    
    def undo(self, file_name: str) -> bool:
        """撤回上次保存"""
        path = os.path.join(self.base_dir, file_name)
        backup_path = os.path.join(self.backup_dir, f"{file_name}.bak")

        if os.path.exists(backup_path):
            try:
                # 先删除原文件
                if os.path.exists(path):
                    os.remove(path)
                # 移动备份文件
                shutil.move(backup_path, path)
                return True
            except Exception as e:
                print(f"撤回文件失败: {e}")
                return False
        return False
    
    def _validate_records(self, records: List[Dict[str, Any]]):
        """验证数据记录"""
        for i, r in enumerate(records, start=1):
            # 内容可以为空，但如果有内容，则数量和价格应该有效
            if r.get("内容"):
                # 如果有内容，检查数量和价格
                quantity = r.get("数量")
                price = r.get("价格")
                
                if quantity is None or quantity <= 0:
                    raise ValueError(f"第{i}行: 数量必须大于0")
                if price is None or price < 0:
                    raise ValueError(f"第{i}行: 价格不能为负")
            
            # 如果没有内容，但提供了数量或价格，也进行验证
            else:
                quantity = r.get("数量")
                price = r.get("价格")
                
                if quantity is not None and quantity < 0:
                    raise ValueError(f"第{i}行: 数量不能为负")
                if price is not None and price < 0:
                    raise ValueError(f"第{i}行: 价格不能为负")
    
    def _add_index(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """添加序号"""
        for i, r in enumerate(records, start=1):
            r["序号"] = i
        return records
    
    def get_file_info(self, file_name: str) -> Dict[str, Any]:
        """获取文件信息"""
        path = os.path.join(self.base_dir, file_name)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"文件不存在: {file_name}")
        
        stat = os.stat(path)
        return {
            "name": file_name,
            "path": path,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime)
        }
    
    def _is_valid_record(self, row) -> bool:
        """检查是否是有效的数据行"""
        try:
            # 检查序号列：如果存在且可以转换为整数，则是有效行
            if "序号" in row.index:
                seq_value = row["序号"]
                if pd.isna(seq_value) or seq_value is None:
                    return False
                
                # 清理序号值
                seq_str = str(seq_value).strip()
                if seq_str == "":
                    return False
                
                try:
                    # 尝试转换为整数
                    int(float(seq_str))
                    return True
                except (ValueError, TypeError):
                    # 如果序号是"合计"、"单位"等字符串，则不是有效数据行
                    return False
            
            # 如果没有序号列，检查是否有内容
            if "内容" in row.index:
                content = row["内容"]
                if pd.isna(content) or content is None:
                    return False
                content_str = str(content).strip()
                if content_str == "":
                    return False
                return True
            
            # 默认返回False，不处理没有明确标识的行
            return False
        except Exception:
            return False
    
    def _convert_value(self, value: Any, column_name: str) -> Any:
        """根据列名转换值类型"""
        if value is None or value == "":
            return None
        
        # 确保是字符串
        str_value = str(value).strip()
        if str_value == "":
            return None
        
        # 根据列名决定转换类型
        if column_name in ["序号"]:
            try:
                return int(float(str_value))
            except (ValueError, TypeError):
                return None
        elif column_name in ["数量", "价格", "总价"]:
            try:
                # 尝试转换为浮点数
                return float(str_value)
            except (ValueError, TypeError):
                # 如果转换失败，返回None
                return None
        elif column_name in ["规格尺寸"]:
            # 规格尺寸可能是"40*60*120厘米"这样的字符串，保持原样
            return str_value
        else:
            # 其他列保持字符串
            return str_value


# 创建全局服务实例
excel_service = ExcelService()
