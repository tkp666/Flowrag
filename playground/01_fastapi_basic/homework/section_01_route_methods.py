from fastapi import FastAPI


app = FastAPI()


# 第 1 小节动手题：
# 1. 补一个处理 GET /items 的路由函数
# 2. 再补一个处理 POST /items 的路由函数
# 3. 两个函数必须分开写
# 4. 函数名要体现不同职责
# 5. 这个作业先用简单 return 即可


@app.get("/items")
def get_items():
    return {"message": "这是 GET /items 的响应"}

@app.post("/items")
def create_item():
    return {"message": "这是 POST /items 的响应"}