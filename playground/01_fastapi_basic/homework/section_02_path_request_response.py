from fastapi import FastAPI


app = FastAPI()


# 第 2 小节动手题：
# 1. 补一个处理 GET /items/{item_id} 的路由函数
# 2. 让这个函数通过路径参数接收 item_id
# 3. 返回一个简单字典，表示查询结果
# 4. 再补一个处理 POST /items 的路由函数
# 5. 让这个函数接收一个 item: dict，表示请求体
# 6. 返回一个简单字典，表示创建结果
# 7. 重点体会：
#    - 哪个是 path parameter
#    - 哪个是 request body
#    - 哪个是 response body
@app.get("/items/{item_id}")
def get_items(item_id: int):
    return {"message": f"{item_id}已查询到"}

@app.post("/items")
def post_items(item: dict):
    return {"message": f"{item}创建成功"}
