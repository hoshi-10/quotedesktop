#!/usr/bin/env python3
"""
测试保存和撤回功能
"""

import requests
import json

def test_save_and_undo():
    """测试保存和撤回功能"""
    base_url = "http://localhost:8000"
    file_name = "一次买够 结算清单.xlsx"
    
    # 1. 先读取当前数据
    print("1. 读取当前数据...")
    response = requests.get(f"{base_url}/read/{file_name}")
    if response.status_code != 200:
        print(f"   读取失败: {response.text}")
        return
    
    original_data = response.json()
    original_records = original_data['records']
    print(f"   原始记录数量: {len(original_records)}")
    print(f"   原始总价: {original_data['total']}")
    
    # 2. 修改一条记录（增加数量）
    modified_records = original_records.copy()
    if len(modified_records) > 0:
        # 修改第一条记录的数量
        modified_records[0]['数量'] = modified_records[0]['数量'] + 1
        # 重新计算总价（后端会自动计算）
    
    # 3. 保存修改
    print("\n2. 保存修改...")
    save_data = {
        "records": modified_records
    }
    
    response = requests.post(
        f"{base_url}/save/{file_name}",
        json=save_data
    )
    
    if response.status_code == 200:
        print(f"   保存成功: {response.json()}")
    else:
        print(f"   保存失败: {response.text}")
        return
    
    # 4. 验证保存结果
    print("\n3. 验证保存结果...")
    response = requests.get(f"{base_url}/read/{file_name}")
    if response.status_code == 200:
        saved_data = response.json()
        print(f"   保存后记录数量: {len(saved_data['records'])}")
        print(f"   保存后总价: {saved_data['total']}")
        
        # 检查第一条记录的数量是否已更新
        if len(saved_data['records']) > 0:
            print(f"   第一条记录数量: {saved_data['records'][0]['数量']}")
            print(f"   第一条记录总价: {saved_data['records'][0]['总价']}")
    else:
        print(f"   验证失败: {response.text}")
    
    # 5. 测试撤回功能
    print("\n4. 测试撤回功能...")
    response = requests.post(f"{base_url}/undo/{file_name}")
    if response.status_code == 200:
        undo_result = response.json()
        print(f"   撤回结果: {undo_result}")
    else:
        print(f"   撤回失败: {response.text}")
        return
    
    # 6. 验证撤回结果
    print("\n5. 验证撤回结果...")
    response = requests.get(f"{base_url}/read/{file_name}")
    if response.status_code == 200:
        undone_data = response.json()
        print(f"   撤回后记录数量: {len(undone_data['records'])}")
        print(f"   撤回后总价: {undone_data['total']}")
        
        # 检查第一条记录的数量是否已恢复
        if len(undone_data['records']) > 0:
            print(f"   第一条记录数量: {undone_data['records'][0]['数量']}")
            print(f"   第一条记录总价: {undone_data['records'][0]['总价']}")
            
            # 比较是否与原始数据一致
            if undone_data['total'] == original_data['total']:
                print("\n✅ 撤回成功：数据已恢复到原始状态")
            else:
                print("\n❌ 撤回失败：数据未完全恢复")
    else:
        print(f"   验证失败: {response.text}")

if __name__ == "__main__":
    try:
        test_save_and_undo()
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到后端服务，请确保后端正在运行")
    except Exception as e:
        print(f"错误: {e}")
