from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from protocals.op import op

app = FastAPI(
    title="示例 API",
    description="展示不同参数类型的接口示例",
    version="1.0.0"
)

# 请求参数模型
class UserQuery(BaseModel):
    age: int
    city: str
    active: Optional[bool] = True

# 1. 使用默认FastAPI框架的接口
@app.post("/users/{user_id}/orders/{order_id}")
@op(protocol_type="mcp", web_framework="fastapi")
async def get_order_detail(
    request: Request,
    user_id: int,
    order_id: str
):
    """示例：使用默认FastAPI框架的接口"""
    return {
        "user_id": user_id,
        "order_id": order_id,
        "status": "completed"
    }

# 2. 使用自定义Web框架的接口
@app.post("/users/search")
@op(protocol_type="mcp", web_framework="fastapi")
async def search_users(
    request: Request,
    query: UserQuery
):
    """示例：使用自定义Web框架的接口"""
    return {
        "users": [
            {
                "age": query.age,
                "city": query.city,
                "active": query.active
            }
        ],
        "total": 1
    }

# 3. 混合参数的接口
@app.post("/users/{user_id}/profile")
@op(protocol_type="mcp", web_framework="fastapi")
async def update_profile(
    request: Request,
    user_id: int,
    query: UserQuery,
    nickname: Optional[str] = None,
    tags: List[str] = []
):
    """示例：同时使用路径参数、请求体参数和查询参数的接口"""
    return {
        "user_id": user_id,
        "profile": {
            "age": query.age,
            "city": query.city,
            "active": query.active,
            "nickname": nickname,
            "tags": tags
        }
    }

if __name__ == "__main__":
    uvicorn.run("demo:app", host="0.0.0.0", port=8000, reload=True)