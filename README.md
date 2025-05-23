# OpenProtocal

## Vision

OpenProtocal is a genetic wheel, aims to bridge the gap between different LLM protocols and deployment frameworks, making it easier for developers to maintain applications and upgrade to AI friendly. Our vision is to create a unified, extensible protocol adaptor that supports:

<details>
<summary>All AI protocols supports</summary>

- Support for all AI interface protocols and forward auto-upgrading
- Compatible for clis-native authentication mechanism
</details>

<details>
<summary>Seamless integration to living endpoints</summary>

- Fast, elegant and Non-invasive intergration
- Zero-downtime integration with existing services
- Plug-and-play endpoint configuration
- Automatic error adapting and retry mechanisms
- Automatic schema validation and correction
- Automated protocol switching implicitly as responding
</details>

<details>
<summary>Cross-framework Cross-languages compatibility</summary>

- Language-agnostic implementation
- Deploy Framework independent design without AST changes
- Consistent API experience across ternimal types
- Map-reducable data structures for minitoring and natural language summarization
</details>

## Installation

```bash
pip install openprotocol
```

## Quick Start

```python
from fastapi import FastAPI
from protocals.op import op

app = FastAPI()

@app.get("/hello")
@op(protocol_type="mcp", web_framework="fastapi")
async def hello(request, name: str = "World"):
    return f"Hello, {name}!"

# Protocol routes will be automatically registered to the FastAPI application
```

## Features

- Generic protocol adapter with support for multiple protocols
- Automatic request parsing and error handling
- Framework-agnostic design
- Full type hint support
- Flexible protocol adaptation framework
- Support for multiple deployment frameworks
- Automatic error response formatting
- Request body validation and parsing

## Example

Check out `demo.py` for a complete example showing:
- Path parameter handling
- Request body validation with Pydantic models
- Mixed parameter types support
- Error handling
- Protocol-specific request processing

## Requirements

- Python >= 3.7
- FastAPI >= 0.68.0
- Pydantic >= 1.8.0

## License

MIT License