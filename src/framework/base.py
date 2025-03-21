from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable

class WebFramework(ABC):
    @abstractmethod
    def create_router(self, prefix: str, tags: list) -> Any:
        pass

    @abstractmethod
    def create_response(self, result: Any) -> Any:
        pass

    @abstractmethod
    def handle_exception(self, e: Exception) -> Any:
        pass

    @abstractmethod
    def get_request_from_args(self, args: tuple) -> Optional[Any]:
        """从函数参数中获取请求对象"""
        pass

    @abstractmethod
    async def parse_request_body(self, request: Any) -> Dict[str, Any]:
        """解析请求体"""
        pass