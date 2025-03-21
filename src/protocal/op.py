from functools import wraps
from typing import Any, Callable, Dict, Optional, List, Union, Type
from framework import get_web_framework
from protocal import get_protocol


# 创建协议管理器实例


def op(protocol_type: str = "mcp", web_framework: str = "fastapi"):
    def decorator(func: Callable):
        method = func.__name__
        frameworks = get_web_framework(web_framework)
        protocols = get_protocol(protocol_type)
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 使用框架提供的方法获取请求对象
            request = frameworks.get_request_from_args(args)
            if not request:
                return await func(*args, **kwargs)

            # 使用框架提供的方法解析请求体
            body = await frameworks.parse_request_body(request)

            try:
                # 使用协议处理器处理请求
                handler = protocols.get_handler(protocol_type, frameworks)
                result = await handler.handle_request(request, body)
                return result
            except Exception as e:
                handler = protocols.get_handler(protocol_type, frameworks)
                return handler.create_response(
                    id=body.get("id") if "body" in locals() else None,
                    error=frameworks.handle_exception(e)
                )

        return wrapper
    return decorator 