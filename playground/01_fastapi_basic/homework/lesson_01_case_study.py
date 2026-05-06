from fastapi import FastAPI
from pydantic import BaseModel

#app
app = FastAPI(
    title="第 1 课综合案例",
    description="用于综合作业的完整最小接口案例",
    version="0.1.0",
)

#响应体 schema
class HealthResponse(BaseModel):
    status: str

#请求体 schema
class BookCreate(BaseModel):
    title: str
    author: str

#响应体 schema
class BookResponse(BaseModel):
    id: int
    title: str
    author: str

#带响应体格式的路由
@app.get("/health", response_model=HealthResponse)
def get_health():
    return {"status": "ok"}

#带 request body 的路由  同时也带了响应体格式
@app.post("/books", response_model=BookResponse)
def create_book(book: BookCreate):
    return {"id": 1, "title": book.title, "author": book.author}

#带 path parameter 的路由
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    return {"id": book_id, "title": "demo book", "author": "demo author"}
