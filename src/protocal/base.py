from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable


class ProtocolHandler(ABC):
    @abstractmethod
    def create_response(self, id: Any = None, result: Any = None, error: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """创建协议响应"""
        pass

    @abstractmethod
    async def handle_request(self, request: Any, body: Dict[str, Any]) -> Dict[str, Any]:
        """处理协议请求"""
        pass