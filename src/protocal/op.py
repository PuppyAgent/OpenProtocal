from functools import wraps
from typing import Any, Callable, Dict, Optional, List, Union, Type
from fastapi import FastAPI, Request, APIRouter, HTTPException
import inspect
from framework.fastapi import FastAPIFramework
from .mcp import MCPProtocolHandler

def get_web_framework(framework_name: str) -> Any:
    framework_map = {
        "fastapi": FastAPIFramework,
        # 在这里可以添加其他框架的映射
    }
    framework_class = framework_map.get(framework_name.lower())
    if not framework_class:
        raise ValueError(f"Unsupported web framework: {framework_name}")
    framework = framework_class()
    if isinstance(framework, FastAPIFramework):
        framework.find_and_register_app()
    return framework

def get_protocol_handler(protocol_type: str, web_framework: Any) -> Any:
    protocol_map = {
        "mcp": MCPProtocolHandler,
        # 在这里可以添加其他协议的映射
    }
    handler_class = protocol_map.get(protocol_type.lower())
    if not handler_class:
        raise ValueError(f"Unsupported protocol type: {protocol_type}")
    return handler_class(web_framework)

# 全局协议处理器字典
protocol_handlers: Dict[str, Any] = {}

def op(protocol_type: str = "mcp", web_framework: str = "fastapi"):
    def decorator(func: Callable):
        method = func.__name__

        # 获取或创建协议处理器
        handler_key = f"{protocol_type}_{web_framework}"
        if handler_key not in protocol_handlers:
            framework = get_web_framework(web_framework)
            protocol_handler = get_protocol_handler(protocol_type, framework)
            protocol_handlers[handler_key] = protocol_handler
        
        handler = protocol_handlers[handler_key]
        handler.registered_methods[method] = func
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 使用框架提供的方法获取请求对象
            request = handler.web_framework.get_request_from_args(args)
            if not request:
                return await func(*args, **kwargs)

            # 使用框架提供的方法解析请求体
            body = await handler.web_framework.parse_request_body(request)

            try:
                # 使用协议处理器处理请求
                result = await handler.handle_request(request, body)
                return result
            except Exception as e:
                return handler.create_response(
                    id=body.get("id") if "body" in locals() else None,
                    error=handler.web_framework.handle_exception(e)
                )

        return wrapper
    return decorator 