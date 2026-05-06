import asyncio
import time

from fastapi import FastAPI


# 第 3 阶段 · 综合课后动手题
#
# 作业目标：
# 1. 复习 FastAPI 中 def / async def 的基本写法
# 2. 复习 await asyncio.sleep(...) 和 time.sleep(...) 的区别
# 3. 复习顺序 await 和 asyncio.gather 并发等待的耗时差异
# 4. 复习为什么 FastAPI async 不能替代 Celery
#
# 自查方式：
# 1. 运行：
#    python lesson_03_async_routes_practice.py
# 2. 你应该看到：
#    lesson 03 async routes homework looks good
#
# 可选 HTTP 运行方式：
#    cd /home/tkp666/FlowRAG/playground/03_fastapi_async_intro/homework
#    /home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn lesson_03_async_routes_practice:app --reload


app = FastAPI(title="Lesson 03 Async Routes Practice")


def blocking_read_file(name: str, delay: int) -> dict:
    """
    TODO:
    - 用 time.sleep(delay) 模拟一个阻塞式文件读取
    - 返回 {"name": name, "status": "done"}
    """
    time.sleep(delay)
    return {"name": name, "status": "done"}


async def async_fetch_api(name: str, delay: int) -> dict:
    """
    TODO:
    - 用 await asyncio.sleep(delay) 模拟一个异步外部 API 请求
    - 返回 {"name": name, "status": "done"}
    """
    await asyncio.sleep(delay)
    return {"name": name, "status": "done"}


@app.get("/file-preview")
def file_preview() -> dict:
    """
    TODO:
    - 用普通 def
    - 调用 blocking_read_file("preview-file", 1)
    - 返回 mode、result、cost_seconds
    """
    start = time.time()
    res = blocking_read_file("preview-file", 1)
    end = time.time()
    return {
        "mode": "blocking",
        "result": res,
        "cost_seconds": end - start
    }


@app.get("/llm-call")
async def llm_call() -> dict:
    """
    TODO:
    - 用 async def
    - await async_fetch_api("llm-api", 1)
    - 返回 mode、result、cost_seconds
    """
    start = time.time()
    res = await async_fetch_api("llm-api", 1)
    end = time.time()
    return {
        "mode": "async",
        "result": res,
        "cost_seconds": end - start
    }


@app.get("/dashboard-sequential")
async def dashboard_sequential() -> dict:
    """
    TODO:
    - 顺序 await 3 个 async_fetch_api，每个 delay=1
    - name 分别用 "profile-api"、"kb-api"、"quota-api"
    - 返回 mode、results、cost_seconds
    - 总耗时应该接近 3 秒
    """
    start = time.time()
    results: list[dict] = []
    results.append(await async_fetch_api("profile-api", 1))
    results.append(await async_fetch_api("kb-api", 1))
    results.append(await async_fetch_api("quota-api", 1))
    end = time.time()
    return {
        "mode": "async",
        "results": results,
        "cost_seconds": end - start
    }


@app.get("/dashboard-concurrent")
async def dashboard_concurrent() -> dict:
    """
    TODO:
    - 用 asyncio.gather(...) 并发等待 3 个 async_fetch_api，每个 delay=1
    - name 分别用 "profile-api"、"kb-api"、"quota-api"
    - 返回 mode、results、cost_seconds
    - 总耗时应该接近 1 秒
    """
    start = time.time()
    results: list[dict] = []
    results = await asyncio.gather(
        async_fetch_api("profile-api", 1),
        async_fetch_api("kb-api", 1),
        async_fetch_api("quota-api", 1)
    )
    end = time.time()
    return {
        "mode": "async",
        "results": results,
        "cost_seconds": end - start
    }


# 文字回答区：
#
# 1. 为什么 /dashboard-concurrent 比 /dashboard-sequential 更快？
# 答：/dashboard-concurrent 用了await asyncio.gather，不需要等三个顺序执行的await，能去异步执行，充分利用等待时间
#
# 2. 如果“上传 200 篇文档并入库”不要求当前请求等完，为什么不该只靠 async def？
# 答：如果只靠async def会导致当前请求很长时间都得不到响应，应该用Celery，放到后台执行
#
# 3. 如果你在 async def 里写 time.sleep(5)，会破坏什么？
# 答：会破坏异步，因为这是阻塞等待



async def check_homework() -> None:
    file_result = file_preview()
    llm_result = await llm_call()
    sequential_result = await dashboard_sequential()
    concurrent_result = await dashboard_concurrent()

    assert file_result["mode"] == "blocking"
    assert llm_result["mode"] == "async"
    assert len(sequential_result["results"]) == 3
    assert len(concurrent_result["results"]) == 3

    sequential_cost = sequential_result["cost_seconds"]
    concurrent_cost = concurrent_result["cost_seconds"]

    assert 2.5 <= sequential_cost <= 3.8, sequential_cost
    assert 0.8 <= concurrent_cost <= 1.8, concurrent_cost
    assert sequential_cost > concurrent_cost * 2, (
        sequential_cost,
        concurrent_cost,
    )

    print("lesson 03 async routes homework looks good")


if __name__ == "__main__":
    asyncio.run(check_homework())
