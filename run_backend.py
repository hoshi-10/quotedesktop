#!/usr/bin/env python3
"""
报价桌面系统 - 后端服务启动脚本
最简单的一键启动方式
"""

import sys
import os

def check_dependencies():
    """检查并安装依赖"""
    print("检查Python依赖...")
    
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
        
        # 使用pip安装
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
            print("依赖安装完成")
        except subprocess.CalledProcessError:
            print("依赖安装失败，请手动运行: pip install -r backend/requirements.txt")
            return False
    else:
        print("所有依赖已安装")
    
    return True

def ensure_directories():
    """确保必要的目录存在"""
    print("检查数据目录...")
    
    directories = [
        "data/excel_files",
        "data/pictures",
        "data/excel_files/backups"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"创建目录: {directory}")
        else:
            print(f"目录已存在: {directory}")
    
    return True

def start_server():
    """启动FastAPI服务器"""
    print("\n" + "=" * 50)
    print("报价桌面系统 - 后端服务")
    print("=" * 50)
    print("服务地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("健康检查: http://localhost:8000/health")
    print("按 Ctrl+C 停止服务")
    print("=" * 50 + "\n")
    
    try:
        import uvicorn
        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n服务已停止")
        return True
    except Exception as e:
        print(f"启动服务失败: {e}")
        return False

def main():
    """主函数"""
    try:
        # 检查依赖
        if not check_dependencies():
            return 1
        
        # 确保目录存在
        if not ensure_directories():
            return 1
        
        # 启动服务
        if not start_server():
            return 1
        
        return 0
    except Exception as e:
        print(f"启动过程中发生错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
