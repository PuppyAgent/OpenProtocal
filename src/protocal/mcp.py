from typing import Any, Callable, Dict, Optional, List, Union
from .base import ProtocolHandler
from ..schema.json_rpc import JSONRPC

class MCPProtocolHandler(ProtocolHandler):
    def __init__(self, web_framework: Any):
        self.web_framework = web_framework
        self.registered_methods: Dict[str, Callable] = {}
        self.schema = JSONRPC()

    def create_response(self, id: Any = None, result: Any = None, error: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.schema.response(
            jsonrpc="2.0",
            id=id,
            result=result,
            error=error
        )
        return response.dict(exclude_none=True)

    async def handle_request(self, request: Any, body: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 使用 schema 验证请求
            request_data = self.schema.request(**body)
        except Exception as e:
            return self.create_response(
                id=body.get("id"),
                error={
                    "code": -32600,
                    "message": "Invalid Request",
                    "data": str(e)
                }
            )

        if request_data.method not in self.registered_methods:
            return self.create_response(
                id=request_data.id,
                error={
                    "code": -32601,
                    "message": "Method not found",
                    "data": f"Method '{request_data.method}' not found"
                }
            )
        
        method = self.registered_methods[request_data.method]
        try:
            result = await method(request, **request_data.params)
            return self.create_response(
                id=request_data.id,
                result=result
            )
        except Exception as e:
            error_response = self.web_framework.handle_exception(e)
            return self.create_response(
                id=request_data.id,
                error=error_response
            )