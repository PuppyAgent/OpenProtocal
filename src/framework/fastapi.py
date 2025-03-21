from typing import Any, Dict, Optional, Callable
from fastapi import APIRouter, HTTPException, FastAPI, Request
import inspect
from .base import WebFramework

class FastAPIFramework(WebFramework):
    def __init__(self):
        self._app = None
        self._routers = []

    def create_router(self, prefix: str, tags: list) -> APIRouter:
        router = APIRouter(prefix=prefix, tags=tags)
        self._routers.append(router)
        return router

    def create_response(self, result: Any) -> Any:
        return result

    def handle_exception(self, e: Exception) -> Any:
        if isinstance(e, HTTPException):
            return {
                "code": e.status_code,
                "message": "HTTP Exception",
                "data": e.detail
            }
        return {
            "code": -32000,
            "message": "Server error",
            "data": str(e)
        }

    def get_request_from_args(self, args: tuple) -> Optional[Request]:
        """从函数参数中获取 FastAPI Request 对象"""
        return next((arg for arg in args if isinstance(arg, Request)), None)

    async def parse_request_body(self, request: Request) -> Dict[str, Any]:
        """解析 FastAPI 请求体"""
        try:
            return await request.json()
        except:
            return {}

    def register_app(self, app: FastAPI):
        """注册 FastAPI 应用并自动包含所有路由"""
        self._app = app
        for router in self._routers:
            app.include_router(router)

    def find_and_register_app(self):
        """查找并注册 FastAPI 应用"""
        for frame_info in inspect.stack():
            local_vars = frame_info.frame.f_locals
            for var in local_vars.values():
                if isinstance(var, FastAPI):
                    self.register_app(var)
                    return