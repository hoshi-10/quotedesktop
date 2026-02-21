#!/usr/bin/env python3
"""
后端功能测试脚本
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        from backend.models import ExcelItem, ExcelData
        from backend.excel_service import ExcelService
        from backend.main import app
        print("✓ 模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_service():
    """测试服务功能"""
    print("\n测试Excel服务...")
    
    try:
        service = ExcelService()
        
        # 测试列出文件
        files = service.list_excel_files()
        print(f"✓ 列出Excel文件: {len(files)} 个文件")
        
        # 测试数据验证
        test_records = [
            {"内容": "测试项目", "数量": 2, "价格": 100},
            {"内容": "另一个项目", "数量": 3, "价格": 50}
        ]
        
        try:
            service._validate_records(test_records)
            print("✓ 数据验证通过")
        except ValueError as e:
            print(f"✗ 数据验证失败: {e}")
        
        # 测试添加序号
        indexed = service._add_index(test_records)
        if indexed[0]["序号"] == 1 and indexed[1]["序号"] == 2:
            print("✓ 序号添加成功")
        else:
            print("✗ 序号添加失败")
        
        return True
    except Exception as e:
        print(f"✗ 服务测试失败: {e}")
        return False

def test_models():
    """测试数据模型"""
    print("\n测试数据模型...")
    
    try:
        # 测试创建ExcelItem
        item = ExcelItem(
            内容="测试内容",
            数量=2,
            价格=100.0,
            材料="测试材料",
            经办人="测试人员"
        )
        
        print(f"✓ 创建ExcelItem: {item.内容}")
        
        # 测试转换为字典
        item_dict = item.dict()
        assert item_dict["内容"] == "测试内容"
        assert item_dict["数量"] == 2
        print("✓ 模型转换成功")
        
        return True
    except Exception as e:
        print(f"✗ 模型测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("报价桌面系统后端测试")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 0
    
    # 运行测试
    tests = [
        ("模块导入", test_imports),
        ("数据模型", test_models),
        ("服务功能", test_service),
    ]
    
    for test_name, test_func in tests:
        tests_total += 1
        if test_func():
            tests_passed += 1
        else:
            print(f"✗ {test_name} 测试失败")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {tests_passed}/{tests_total} 通过")
    
    if tests_passed == tests_total:
        print("✓ 所有测试通过！")
        return 0
    else:
        print("✗ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
