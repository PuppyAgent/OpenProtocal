# FastAPI MCP

一个基于FastAPI的JSON-RPC MCP协议实现。

## 安装

```bash
pip install fastapi-mcp
```

## 快速开始

```python
from fastapi import FastAPI
from fastapi_mcp import mcp

app = FastAPI()

@mcp()
async def hello(request, name: str = "World"):
    return f"Hello, {name}!"

# MCP路由会自动注册到FastAPI应用
```

## 特性

- 完全兼容JSON-RPC 2.0规范
- 自动注册路由
- 异常处理
- 类型提示支持

## License

MIT License