import asyncio
import time

from fastapi import FastAPI


app = FastAPI(title="FlowRAG Stage 3 Async Intro")


def blocking_task(name: str, delay: int) -> dict:
    """
    TODO:
    - 用 time.sleep(delay) 模拟同步阻塞等待
    - 返回一个 dict，例如 {"name": name, "status": "done"}
    """
    time.sleep(delay)
    return {"name": name, "status": "done"}


async def async_task(name: str, delay: int) -> dict:
    """
    TODO:
    - 用 await asyncio.sleep(delay) 模拟异步等待
    - 返回一个 dict，例如 {"name": name, "status": "done"}
    """
    await asyncio.sleep(delay)
    return {"name": name, "status": "done"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/wait-sync")
def wait_sync() -> dict:
    """
    TODO:
    - 记录开始时间
    - 调用 blocking_task("sync-task", 2)
    - 记录结束时间
    - 返回 mode、result、cost_seconds
    """
    start = time.time()
    res = blocking_task("sync-task", 2)
    end = time.time()
    return {
        "mode": "sync",
        "result": res,
        "cost_seconds": end - start
    }


@app.get("/wait-async")
async def wait_async() -> dict:
    """
    TODO:
    - 记录开始时间
    - await async_task("async-task", 2)
    - 记录结束时间
    - 返回 mode、result、cost_seconds
    """
    start = time.time()
    res = await async_task("async-task", 2)
    end = time.time()
    return {
        "mode": "async",
        "result": res,
        "cost_seconds": end - start
    }


@app.get("/fanout-sequential")
async def fanout_sequential() -> dict:
    """
    TODO:
    - 顺序 await 3 次 async_task，每次 delay=2
    - 总耗时应该接近 6 秒
    - 返回 mode、results、cost_seconds
    """
    start = time.time()
    results: list[dict] = []
    results.append(await async_task("async-task", 2))
    results.append(await async_task("async-task", 2))
    results.append(await async_task("async-task", 2))
    end = time.time()
    return {
        "mode": "async",
        "results": results,
        "cost_seconds": end - start
    }
    


@app.get("/fanout-concurrent")
async def fanout_concurrent() -> dict:
    """
    TODO:
    - 用 asyncio.gather(...) 并发等待 3 个 async_task，每个 delay=2
    - 总耗时应该接近 2 秒
    - 返回 mode、results、cost_seconds
    """
    start = time.time()
    results = await asyncio.gather(
        async_task("async-task", 2),
        async_task("async-task", 2),
        async_task("async-task", 2)
    )
    end = time.time()
    return {
        "mode": "async",
        "results": results,
        "cost_seconds": end - start
    }
