from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# 整个 FastAPI 应用对象
app = FastAPI(
    title="FastAPI 最小接口实验",
    description="阶段 1：GET /health、POST /items、GET /items/{item_id}",
    version="0.1.0",
)


# 响应体 schema：健康检查接口返回的数据结构
class HealthResponse(BaseModel):
    status: str


# 请求体 schema：创建 item 时客户端提交的数据结构
class ItemCreate(BaseModel):
    name: str
    description: str | None = None


# 响应体 schema：创建成功或查询成功后返回的数据结构
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


# 内存存储：当前阶段先不用数据库
items_store: dict[int, ItemResponse] = {}
next_item_id = 1


@app.get("/health", response_model=HealthResponse)
def get_health():
    return {"status": "ok"}

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate):
    global next_item_id
    item_res = ItemResponse(
        id=next_item_id,
        name=item.name,
        description=item.description
    )
    items_store[next_item_id] = item_res
    next_item_id += 1
    return item_res

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id in items_store:
        return items_store[item_id]
    raise HTTPException(status_code=404, detail="Item not found!")
