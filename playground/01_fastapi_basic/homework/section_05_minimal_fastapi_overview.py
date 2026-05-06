from fastapi import FastAPI
from pydantic import BaseModel

#这是app
app = FastAPI(
    title="第 5 小节整体视图练习",
    description="把 app、schema、route、path parameter、request body、response body、/docs 串起来",
    version="0.1.0",
)

#这是 schema
class HealthResponse(BaseModel):
    status: str

#这是 schema
class ItemCreate(BaseModel):
    name: str
    description: str | None = None


# 第 5 小节动手题：
# 这次不要再机械重复上一小节“只把接口写出来”。
# 这一小节重点是：把整个最小 FastAPI 文件按结构串起来看明白。
#
# 你要完成的内容：
# 1. 补一个 GET /health 路由：
#    - 使用 response_model=HealthResponse
#    - 返回 {"status": "ok"}
# 2. 补一个 GET /items/{item_id} 路由：
#    - 通过路径参数接收 item_id
#    - 返回简单字典
# 3. 补一个 POST /items 路由：
#    - 接收 item: ItemCreate
#    - 返回简单字典
# 4. 在每个关键代码块上方补 1 行中文注释，明确标出：
#    - 这是 app
#    - 这是 schema
#    - 这是 health 路由
#    - 这是带 path parameter 的路由
#    - 这是带 request body 的路由
# 5. 启动后访问 /docs，观察：
#    - /health 为什么没有请求体
#    - /items/{item_id} 为什么会显示路径参数
#    - POST /items 为什么会显示 ItemCreate 的字段
#
# 完成标准：
# - 代码能启动
# - /docs 能正常打开
# - 你自己能指出这份文件里 app、schema、路由分别在哪里

#这是 health 路由
@app.get("/health", response_model=HealthResponse)
def get_status():
    response = HealthResponse(status="OK")
    return response

#这是带 path parameter 的路由
@app.get("/items/{item_id}")
def get_items(item_id: int):
    return {"message": f"{item_id}已查询到"}

#这是带 request body 的路由
@app.post("/items")
def post_item(item: ItemCreate):
    return {"message": f"{item}已创建"}
