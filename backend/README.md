# 报价桌面系统 - 后端

基于FastAPI的报价桌面系统后端服务，提供Excel文件管理、数据读写、撤回等功能。

## 项目结构

```
backend/
├── __init__.py              # 包初始化
├── main.py                  # FastAPI主应用
├── models.py                # 数据模型（Pydantic）
├── excel_service.py         # Excel服务逻辑
├── function.py              # 旧版功能（兼容保留）
├── requirements.txt         # Python依赖
└── README.md                # 本文档
```

## 功能特性

1. **Excel文件管理**
   - 列出data/excel_files目录下所有.xlsx文件
   - 读取Excel文件数据并自动计算总价
   - 保存数据到Excel文件（支持备份和撤回）

2. **数据操作**
   - 完整的CRUD操作
   - 数据验证（内容必填、数量>0、价格≥0）
   - 自动计算总价和合计

3. **撤回功能**
   - 每次保存前自动备份原文件
   - 支持撤回上次保存操作

4. **图片处理**
   - 支持将图片路径插入Excel
   - 图片文件管理

## API接口

### 基础信息
- `GET /` - API根路径，返回接口信息
- `GET /health` - 健康检查

### 文件操作
- `GET /files` - 获取所有Excel文件列表
- `GET /read/{file_name}` - 读取指定Excel文件数据
- `POST /save/{file_name}` - 保存数据到指定Excel文件
- `POST /undo/{file_name}` - 撤回上次保存操作

## 快速开始

### 前置步骤
进入虚拟环境：
python -m venv .venv
激活虚拟环境：
.venv\Scripts\activate.bat


### 1. 安装依赖
```bash
pip install -r backend/requirements.txt
```

### 2. 启动服务
```bash
python backend/main.py
```

**启动脚本会自动：**
- ✅ 检查并安装依赖
- ✅ 创建必要的目录
- ✅ 启动FastAPI服务

### 3. 访问API
- 服务地址: http://localhost:8000
- 交互式文档: http://localhost:8000/docs
- 备用文档: http://localhost:8000/redoc

### 其他启动方式

**使用uvicorn（支持热重载）：**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**使用Python模块：**
```bash
python -m backend.main
```

## 数据模型

### ExcelItem（Excel项目）
```python
{
    "序号": 1,                    # 自动生成
    "内容": "项目内容",           # 必填
    "材料": "材料名称",           # 可选
    "规格尺寸": 10.5,            # 可选
    "数量": 2,                   # 必填，必须>0
    "价格": 100.0,               # 必填，必须≥0
    "总价": 200.0,               # 自动计算
    "项目图片": "path/to/image.jpg",  # 可选
    "经办人": "张三",            # 可选
    "备注": "备注信息"           # 可选
}
```

## 开发说明

### 数据目录结构
```
data/
├── 文件1.xlsx
├── 文件2.xlsx
├── temp.xlsx        # 临时文件（自动生成）
└── backups/        # 备份文件目录
    └── 文件1.xlsx.bak
```

### 备份机制
- 每次保存前，原文件会被备份为`原文件名.xlsx.bak`
- 撤回操作会使用备份文件恢复原文件
- 临时文件`temp.xlsx`用于安全写入

## 测试

### 使用curl测试API
```bash
# 获取文件列表
curl http://localhost:8000/files

# 读取文件数据
curl http://localhost:8000/read/测试文件.xlsx

# 保存数据
curl -X POST http://localhost:8000/save/测试文件.xlsx \
  -H "Content-Type: application/json" \
  -d '{"records": [{"内容": "测试项目", "数量": 2, "价格": 100}]}'

# 撤回操作
curl -X POST http://localhost:8000/undo/测试文件.xlsx
```

## 注意事项

1. **文件安全**：API包含路径遍历防护，只允许操作data/excel_files目录下的.xlsx文件
2. **数据验证**：保存时会验证数据格式，不符合要求会返回错误
3. **并发处理**：系统设计为单用户使用，不考虑并发问题
4. **错误处理**：所有操作都有错误处理和友好的错误信息

## 故障排除

### 常见问题
1. **导入错误**：确保已安装所有依赖 `pip install -r requirements.txt`
2. **文件不存在**：检查data/excel_files目录是否存在且包含.xlsx文件
3. **权限问题**：确保对data目录有读写权限
4. **端口占用**：如果8000端口被占用，可修改main.py中的端口号

### 日志查看
服务启动时会显示详细日志，包括请求处理、错误信息等。
