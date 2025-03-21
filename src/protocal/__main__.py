from typing import Any
from .mcp import MCPProtocolHandler


def get_protocol(protocol_type: str) -> Any:
    """
    获取协议处理器实例
    
    Args:
        protocol_type: 协议类型，例如 "mcp"
        
    Returns:
        协议处理器实例
        
    Raises:
        ValueError: 当协议类型不支持时
    """
    protocol_map = {
        "mcp": MCPProtocolHandler,
        # 在这里可以添加其他协议的映射
    }
    
    protocol_class = protocol_map.get(protocol_type.lower())
    if not protocol_class:
        raise ValueError(f"Unsupported protocol type: {protocol_type}")
        
    return protocol_class
