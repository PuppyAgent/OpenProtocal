from typing import List, Dict, Any, Callable
from fastapi import FastAPI
import inspect
import functools
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APITracer:
    def __init__(self, app: FastAPI):
        self.app = app
        self.endpoints: List[Dict[str, Any]] = []
        self._trace_all_routes()

    def _trace_all_routes(self):
        """追踪所有路由并添加装饰器"""
        for route in self.app.routes:
            original_endpoint = route.endpoint
            if not inspect.isfunction(original_endpoint):
                continue

            @functools.wraps(original_endpoint)
            async def traced_endpoint(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await original_endpoint(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self._log_request(route.path, route.methods, execution_time, "success")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._log_request(route.path, route.methods, execution_time, "error", str(e))
                    raise

            route.endpoint = traced_endpoint
            self.endpoints.append({
                "path": route.path,
                "methods": route.methods,
                "name": original_endpoint.__name__,
                "doc": original_endpoint.__doc__
            })

    def _log_request(self, path: str, methods: List[str], execution_time: float, status: str, error: str = None):
        """记录请求信息"""
        log_data = {
            "path": path,
            "methods": methods,
            "execution_time": f"{execution_time:.3f}s",
            "status": status,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        if error:
            log_data["error"] = error

        logger.info(f"API Request: {log_data}")

    def get_endpoints(self) -> List[Dict[str, Any]]:
        """获取所有已追踪的端点信息"""
        return self.endpoints

def trace_fastapi_app(app: FastAPI) -> APITracer:
    """
    为 FastAPI 应用添加追踪功能
    
    Args:
        app: FastAPI 应用实例
        
    Returns:
        APITracer: 追踪器实例
    """
    return APITracer(app) 