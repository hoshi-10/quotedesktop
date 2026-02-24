#!/usr/bin/env python3
"""
测试Excel文件读取
"""

import requests
import json

def test_read_excel():
    """测试读取Excel文件"""
    base_url = "http://localhost:8000"
    
    # 1. 测试健康检查
    print("1. 测试健康检查...")
    response = requests.get(f"{base_url}/health")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    # 2. 获取文件列表
    print("\n2. 获取文件列表...")
    response = requests.get(f"{base_url}/files")
    print(f"   状态码: {response.status_code}")
    files = response.json()
    print(f"   文件列表: {files}")
    
    if not files:
        print("   没有找到Excel文件")
        return
    
    # 3. 读取第一个文件
    file_name = files[0]
    print(f"\n3. 读取文件: {file_name}")
    response = requests.get(f"{base_url}/read/{file_name}")
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   文件名称: {data['file_name']}")
        print(f"   记录数量: {len(data['records'])}")
        print(f"   总价合计: {data['total']}")
        
        # 显示前几条记录
        print(f"\n   前3条记录:")
        for i, record in enumerate(data['records'][:3], 1):
            print(f"   记录{i}:")
            for key, value in record.items():
                print(f"     {key}: {value}")
            print()
    else:
        print(f"   错误: {response.text}")

if __name__ == "__main__":
    try:
        test_read_excel()
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到后端服务，请确保后端正在运行")
    except Exception as e:
        print(f"错误: {e}")
