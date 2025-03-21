from pydantic import BaseModel
from typing import Any, Dict, Optional
from .base import Schema

class JSONRPC(Schema):
    def __init__(self):
        pass

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