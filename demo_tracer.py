from fastapi import FastAPI
from protocals.tracer import trace_fastapi_app

app = FastAPI()

# 创建追踪器
tracer = trace_fastapi_app(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(name: str, price: float):
    return {"name": name, "price": price}

if __name__ == "__main__":
    import uvicorn
    # 打印所有被追踪的端点
    print("追踪的端点列表：")
    for endpoint in tracer.get_endpoints():
        print(f"- {endpoint['path']} ({', '.join(endpoint['methods'])})")
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 