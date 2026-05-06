# 阶段 3：FastAPI 异步入门主体实现

本实验采用模式 A：用户主写。

## 你要完成什么

在 `main.py` 中完成 4 个接口：

- `GET /wait-sync`
- `GET /wait-async`
- `GET /fanout-sequential`
- `GET /fanout-concurrent`

## 文件职责

- `main.py`：FastAPI 应用、同步阻塞任务、异步等待任务、4 个实验接口。
- `requirements.txt`：本实验需要的 Python 依赖。
- `README.md`：运行方式、测试方式和验收标准。

## 实现要求

`blocking_task(name, delay)`：

- 使用 `time.sleep(delay)`。
- 返回一个 dict，例如 `{"name": name, "status": "done"}`。

`async_task(name, delay)`：

- 使用 `await asyncio.sleep(delay)`。
- 返回一个 dict，例如 `{"name": name, "status": "done"}`。

`/wait-sync`：

- 使用普通 `def`。
- 调用 `blocking_task("sync-task", 2)`。
- 返回 `mode`、`result`、`cost_seconds`。

`/wait-async`：

- 使用 `async def`。
- 调用 `await async_task("async-task", 2)`。
- 返回 `mode`、`result`、`cost_seconds`。

`/fanout-sequential`：

- 使用 `async def`。
- 顺序 `await` 3 次 `async_task(...)`。
- 总耗时应该接近 6 秒。

`/fanout-concurrent`：

- 使用 `async def`。
- 用 `await asyncio.gather(...)` 并发等待 3 个 `async_task(...)`。
- 总耗时应该接近 2 秒。

## 运行方式

```bash
cd /home/tkp666/FlowRAG/playground/03_fastapi_async_intro
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn main:app --reload
```

## 测试方式

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/wait-sync
curl http://127.0.0.1:8000/wait-async
curl http://127.0.0.1:8000/fanout-sequential
curl http://127.0.0.1:8000/fanout-concurrent
```

浏览器也可以打开：

```text
http://127.0.0.1:8000/docs
```

## 验收标准

- `/health` 返回 `{"status":"ok"}`。
- `/wait-sync` 能看到同步阻塞等待的耗时。
- `/wait-async` 能看到异步等待的耗时。
- `/fanout-sequential` 总耗时接近 6 秒。
- `/fanout-concurrent` 总耗时接近 2 秒。
- 你能解释为什么 `asyncio.gather` 能让多个 I/O 等待重叠。
- 你能解释为什么这个实验不能替代后面的 Celery。
