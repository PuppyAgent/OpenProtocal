# OpenProtocal

A flexible protocol adaptation utility that supports multiple LLM-friendly protocols and deployment frameworks, with initial support for MCP and FastAPI.

## Installation

```bash
pip install openprotocal
```

## Quick Start

```python
from fastapi import FastAPI
from protocals.mcp import mcp

app = FastAPI()

@app.get("/hello")
@mcp(hello)
async def hello(request, name: str = "World"):
    return f"Hello, {name}!"

# MCP routes will be automatically registered to the FastAPI application
```

## Features

- JSON-RPC 2.0 specification compliant MCP implementation
- Automatic route registration with FastAPI integration
- Comprehensive exception handling
- Full type hint support
- Flexible protocol adaptation framework
- Support for multiple deployment frameworks

## Example

Check out `demo.py` for a complete example showing:
- Path parameter handling
- Request body validation with Pydantic models
- Mixed parameter types support
- Error handling

## Requirements

- Python >= 3.7
- FastAPI >= 0.68.0
- Pydantic >= 1.8.0

## License

MIT License