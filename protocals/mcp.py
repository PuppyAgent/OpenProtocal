from functools import wraps
from typing import Any, Callable, Dict, Optional, List, Union
from fastapi import FastAPI, Request, APIRouter, HTTPException
from pydantic import BaseModel
import inspect

class MCP(JSONRPC):
    def __init__(self):
        
        super().__init__()
        self.router = APIRouter(prefix="/mcp", tags=["mcp"])

    @property
    def request(self):

        class JsonRpcRequest(BaseModel):
            jsonrpc: str
            method: str
            params: Dict[str, Any] = {}
            id: Any

        return JsonRpcRequest

    
    @property
    def error(self):
        class JsonRpcError(BaseModel):
            code: int
            message: str
            data: Optional[Any] = None
        return JsonRpcError

    @property
    def response(self):
        class JsonRpcResponse(BaseModel):
            jsonrpc: str = "2.0"
            result: Optional[Any] = None
            error: Optional[self.error] = None
            id: Optional[Any] = None
        return JsonRpcResponse


# 存储所有注册的方法
registered_methods: Dict[str, Callable] = {}

# 创建路由
router = APIRouter(prefix="/mcp", tags=["mcp"])

def create_jsonrpc_response(
    id: Any = None,
    result: Any = None,
    error: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    response = {"jsonrpc": "2.0", "id": id}
    if error:
        response["error"] = error
    else:
        response["result"] = result
    return response

@router.post("/")
async def mcp_endpoint(request: Request):
    try:
        body = await request.json()
        
        if "jsonrpc" not in body or "method" not in body:
            return create_jsonrpc_response(
                id=body.get("id"),
                error={
                    "code": -32600,
                    "message": "Invalid Request",
                    "data": "Missing required fields"
                }
            )
        
        method_name = body.get("method")
        if method_name not in registered_methods:
            return create_jsonrpc_response(
                id=body.get("id"),
                error={
                    "code": -32601,
                    "message": "Method not found",
                    "data": f"Method '{method_name}' not found"
                }
            )
        
        method = registered_methods[method_name]
        params = body.get("params", {})
        result = await method(request, **params)
        
        # 结果已经是 JSON-RPC 格式，直接返回
        return result
        
    except Exception as e:
        return create_jsonrpc_response(
            id=body.get("id"),
            error={
                "code": -32000,
                "message": "Server error",
                "data": str(e)
            }
        )

def mcp(method_name: Optional[str] = None):
    def decorator(func: Callable):
        nonlocal method_name
        method = method_name or func.__name__
        registered_methods[method] = func
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = next((arg for arg in args if isinstance(arg, Request)), None)
            if not request:
                return await func(*args, **kwargs)

            try:
                body = await request.json()
                request_id = body.get("id")
            except:
                request_id = None

            try:
                result = await func(*args, **kwargs)
                # 处理 HTTPException
                if isinstance(result, HTTPException):
                    return create_jsonrpc_response(
                        id=request_id,
                        error={
                            "code": result.status_code,
                            "message": "HTTP Exception",
                            "data": result.detail
                        }
                    )
                # 确保返回标准的 JSON-RPC 响应格式
                return create_jsonrpc_response(
                    id=request_id,
                    result=result
                )
            except HTTPException as e:
                return create_jsonrpc_response(
                    id=request_id,
                    error={
                        "code": e.status_code,
                        "message": "HTTP Exception",
                        "data": e.detail
                    }
                )
            except Exception as e:
                return create_jsonrpc_response(
                    id=request_id,
                    error={
                        "code": -32000,
                        "message": "Server error",
                        "data": str(e)
                    }
                )

        return wrapper
    return decorator

# 自动注册路由到 FastAPI 应用
def _find_fastapi_app():
    for frame_info in inspect.stack():
        local_vars = frame_info.frame.f_locals
        for var in local_vars.values():
            if isinstance(var, FastAPI):
                return var
    return None

app = _find_fastapi_app()
if app:
    app.include_router(router)