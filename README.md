# FastAPI MCP

A JSON-RPC MCP protocol implementation based on FastAPI.

## Installation

```bash
pip install fastapi-mcp
```

## Quick Start

```python
from fastapi import FastAPI
from fastapi_mcp import mcp

app = FastAPI()

@mcp()
async def hello(request, name: str = "World"):
    return f"Hello, {name}!"

# MCP routes will be automatically registered to the FastAPI application
```

## Features

- Fully compatible with JSON-RPC 2.0 specification
- Automatic route registration
- Exception handling
- Type hint support

## License

MIT License