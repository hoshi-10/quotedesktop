# backend/main.py 修改说明

## 修改目的

让 `backend/main.py` 可以直接运行，替代 `sundry/run_backend.py` 的功能。

## 修改内容

### 1. 修复相对导入问题

**问题**：直接运行 `python backend/main.py` 时，相对导入会报错：
```
ImportError: attempted relative import with no known parent package
```

**解决方案**：
- `backend/main.py`：已有 try-except 处理相对导入
- `backend/excel_service.py`：添加 try-except 处理相对导入

### 2. 添加启动脚本功能

在 `backend/main.py` 的 `if __name__ == "__main__"` 部分添加：

- ✅ **依赖检查**：自动检查并安装缺失的依赖
- ✅ **目录创建**：自动创建 `data/excel_files`、`data/pictures`、`data/excel_files/backups` 目录
- ✅ **友好提示**：显示服务地址、API文档等信息
- ✅ **错误处理**：完善的异常处理和退出码

### 3. 修改启动方式

**之前**：
```python
uvicorn.run(
    "backend.main:app",  # 字符串方式，需要reload模式
    host="0.0.0.0",
    port=8000,
    reload=True,
    log_level="info"
)
```

**现在**：
```python
uvicorn.run(
    app,  # 直接传递app对象
    host="0.0.0.0",
    port=8000,
    reload=False,  # 直接运行时不使用reload，避免模块导入问题
    log_level="info"
)
```

## 使用方式

### 方式1：直接运行（推荐）⭐
```bash
python backend/main.py
```

### 方式2：使用uvicorn（支持热重载）
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 方式3：使用Python模块
```bash
python -m backend.main
```

## 启动输出示例

```
============================================================
报价桌面系统 - 后端服务
============================================================

检查Python依赖...
所有依赖已安装

检查数据目录...
目录已存在: D:\computer\auto-quotation software system\quotedesktop\data\excel_files
目录已存在: D:\computer\auto-quotation software system\quotedesktop\data\pictures
目录已存在: D:\computer\auto-quotation software system\quotedesktop\data\excel_files\backups

============================================================
服务地址: http://localhost:8000
API文档: http://localhost:8000/docs
健康检查: http://localhost:8000/health
按 Ctrl+C 停止服务
============================================================

INFO:     Started server process [16628]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 测试结果

✅ 所有API端点正常工作
✅ Excel文件读取、保存、撤回功能正常
✅ 数据验证问题已修复
✅ 可以直接运行，无需额外脚本

## 优势

1. **更简洁**：不需要额外的 `run_backend.py` 文件
2. **更直观**：直接运行 `backend/main.py` 即可
3. **更完整**：自动处理依赖和目录
4. **更友好**：清晰的启动信息和错误提示

## 注意事项

- 直接运行时不支持热重载（reload=False）
- 如需热重载功能，请使用 `uvicorn backend.main:app --reload`
- `sundry/run_backend.py` 仍然保留，可以继续使用
