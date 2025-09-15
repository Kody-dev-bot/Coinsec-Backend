# Coinsec Backend

一句话 AI 记账后端服务

## 项目概述

Coinsec 是一个基于 AI 技术的智能记账系统，旨在通过人工智能技术简化用户的记账流程，提供智能化的财务管理服务。该系统能够自动识别和分类用户的收支记录，生成财务报表，并提供个性化的理财建议。

## 技术栈

- [FastAPI](https://fastapi.tiangolo.com/) - 现代、快速（高性能）的 Web 框架
- [SQLModel](https://sqlmodel.tiangolo.com/) - SQL 数据库库，基于 Pydantic 和 SQLAlchemy
- [LiteLLM](https://litellm.ai/) - 提供统一接口访问各种大语言模型
- [Loguru](https://github.com/Delgan/loguru) - 简化 Python 日志记录
- [Uvicorn](https://www.uvicorn.org/) - 用于运行 Python 异步 Web 应用的轻量级 ASGI 服务器
- [Pydantic](https://docs.pydantic.dev/) - 数据验证和设置管理

## 项目结构

```text
.
├── alembic                     # 数据库迁移工具配置
│   └── __init__.py
├── app                         # 主应用目录
│   ├── api                     # API 路由定义
│   │   └── __init__.py
│   ├── core                    # 核心配置和安全相关
│   │   └── __init__.py
│   ├── crud                    # 数据库增删改查操作
│   │   └── __init__.py
│   ├── db                      # 数据库连接和会话管理
│   │   └── __init__.py
│   ├── main.py                 # 应用入口文件
│   ├── models                  # 数据模型定义
│   │   └── __init__.py
│   ├── schemas                 # Pydantic 模型/数据结构定义
│   │   └── __init__.py
│   └── utils                   # 工具函数和辅助模块
│       └── __init__.py
├── pyproject.toml              # 项目配置文件
├── README.md                   # 项目说明文档
└── tests                       # 测试文件
    └── __init__.py
```

## 安装与运行

### 环境要求

- Python 3.13 或更高版本

### 安装依赖

推荐使用 `uv` 工具进行依赖管理：

```bash
pip install uv
uv sync
```

或者使用传统 pip 方式：

```bash
pip install -r requirements.txt
```

### 运行应用

开发模式运行：

```bash
uv run dev
```

或者使用 uvicorn 直接运行：

```bash
uvicorn app.main:app --reload
```

或者：

```bash
python -m uvicorn app.main:app --reload
```

## 数据库迁移

使用 Alembic 进行数据库迁移:

```bash
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

## API 文档

启动服务后，可以通过以下地址访问自动生成的 API 文档:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试

运行测试:

```bash
python -m pytest
```