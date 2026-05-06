# 第 1 课综合作业说明

这次综合作业不要求你再从零重写一遍最小 FastAPI 接口。

这次要练的是：

1. 你能不能读懂一份新的最小 FastAPI 文件；
2. 你能不能把 `app`、`schema`、`path parameter`、`request body`、`response_model`、`response body` 对应起来；
3. 你能不能运行它，并把 `/docs` 看到的内容和代码对应起来。

## 你要做的事

### 第 1 步：修改代码文件

打开：

`lesson_01_case_study.py`

在这个文件里补上 5 行中文注释，明确标出：

1. 哪一段是 `app`
2. 哪一段是 `请求体 schema`
3. 哪一段是 `响应体 schema`
4. 哪一个路由是 `带 request body 的路由`
5. 哪一个路由是 `带 path parameter 的路由`

不要改动接口路径和整体结构，重点是“看懂并标出来”。

### 第 2 步：运行并观察

运行命令：

```bash
conda activate flowrag
cd /home/tkp666/FlowRAG/playground/01_fastapi_basic/homework
uvicorn lesson_01_case_study:app --reload --port 8005
```

打开：

`http://127.0.0.1:8005/docs`

再自己执行：

```bash
curl http://127.0.0.1:8005/health
```

```bash
curl http://127.0.0.1:8005/books/1
```

```bash
curl -X POST http://127.0.0.1:8005/books \
  -H "Content-Type: application/json" \
  -d '{"title":"fastapi intro","author":"demo author"}'
```

### 第 3 步：填写下面的回答

1. `app` 在代码的哪一段？它的作用是什么？

答：在5~9行，实例化一下FastAPI

2. 哪个 schema 描述的是 `request body`？你为什么这么判断？

答：class BookCreate(BaseModel):
    title: str
    author: str  这一段描述的是请求体，因为它在33行中被当作POST的参数传进去了

3. 哪个 schema 描述的是 `response body`？你为什么这么判断？

答：class HealthResponse(BaseModel):
    status: str
    和
    class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    都是，因为他们分别作为了两个函数的response_model

4. `GET /books/{book_id}` 里的 `book_id` 为什么是 `path parameter`？

答：因为在{}中，并且被当作函数的参数传进去了

5. `POST /books` 为什么会在 `/docs` 里显示请求体？

答：因为他定义了请求体 book: BookCreate

6. `GET /health` 为什么没有请求体？

答：GET方法一般不带请求体

7. 你实际运行后，下面三个请求分别返回了什么？

- `GET /health`

答：{"status":"ok"}

- `GET /books/1`

答：{"id":1,"title":"demo book","author":"demo author"}


- `POST /books`

答：{"id":1,"title":"fastapi intro","author":"demo author"}

8. 如果让你用一句话概括这份文件的阅读顺序，你会怎么说？

答：先看app，再看请求体和响应体的格式定义，最后去看各种函数

