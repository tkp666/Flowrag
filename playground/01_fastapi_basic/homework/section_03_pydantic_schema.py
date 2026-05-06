from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# 第 3 小节动手题：
# 1. 定义一个 ItemCreate schema
# 2. 让它至少包含 name 和 description 两个字段
# 3. 写一个 POST /items 路由函数
# 4. 让这个函数接收 item: ItemCreate，而不是 item: dict
# 5. 返回一个简单字典，表示创建结果
# 6. 重点体会：
#    - schema 和 dict 的区别
#    - BaseModel 在这里扮演什么角色

class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    

@app.post("/items")
def post_items(item: ItemCreate):
    return {"message" : f"{item}已成功创建"}