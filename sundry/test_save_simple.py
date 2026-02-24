#!/usr/bin/env python3
"""
简单测试保存功能
"""

import requests
import json

def test_save_simple():
    """简单测试保存功能"""
    base_url = "http://localhost:8000"
    file_name = "一次买够 结算清单.xlsx"
    
    print("测试保存功能...")
    
    # 1. 读取当前数据
    print("1. 读取当前数据...")
    response = requests.get(f"{base_url}/read/{file_name}")
    if response.status_code != 200:
        print(f"   读取失败: {response.text}")
        return
    
    data = response.json()
    records = data['records']
    print(f"   当前记录数: {len(records)}")
    print(f"   当前总价: {data['total']}")
    
    # 2. 准备保存数据（不修改，直接保存相同数据）
    save_data = {
        "records": records
    }
    
    # 3. 保存
    print("\n2. 保存数据...")
    response = requests.post(
        f"{base_url}/save/{file_name}",
        json=save_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   保存成功: {result['message']}")
        print("✅ 保存功能正常")
    else:
        print(f"   保存失败: {response.text}")
        print("❌ 保存功能异常")

if __name__ == "__main__":
    try:
        test_save_simple()
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到后端服务，请确保后端正在运行")
    except Exception as e:
        print(f"错误: {e}")
