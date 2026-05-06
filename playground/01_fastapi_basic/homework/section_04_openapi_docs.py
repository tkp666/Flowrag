from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


# 第 4 小节动手题：
# 1. 补一个 GET /items/{item_id} 路由函数
# 2. 再补一个 POST /items 路由函数
# 3. POST /items 要接收 item: ItemCreate
# 4. 两个函数都返回简单字典即可
# 5. 完成后你需要自己启动这个文件，并访问 /docs
# 6. 重点观察：
#    - /docs 里出现了哪些接口
#    - path parameter 在哪里显示
#    - request body 在哪里显示
#    - schema 字段信息是怎么显示出来的
@app.get("/items/{item_id}")
def get_items(item_id: int):
    return {"message": f"{item_id}已查询到"}


@app.post("/items")
def post_item(item: ItemCreate):
    return {"message": f"{item}已创建"}
