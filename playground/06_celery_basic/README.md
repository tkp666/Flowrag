# Stage 6: Celery Basic

本阶段是 Celery 异步任务的最小可运行实验。

核心目标：

- API 提交任务后立即返回 `task_id`
- Celery worker 后台执行任务
- API 根据 `task_id` 查询任务状态
- 保持 `router / schema / service` 分层，不把 Celery 当成新的业务层

## 文件职责

```text
app/main.py
  创建 FastAPI app，挂载 task_router。

app/api/task_router.py
  HTTP 入口，只负责接收请求和调用 service。

app/schemas.py
  定义请求体和响应体。

app/services/task_service.py
  封装任务提交、状态查询和模拟业务函数。

app/celery_app.py
  创建 Celery app，配置 Redis broker / result backend。

app/tasks.py
  Celery worker 入口，注册 worker 能执行的任务函数。

check_stage6.py
  轻量检查脚本，不需要启动 Redis 或 worker。
```

## 运行前准备

确认 Redis 可用：

```bash
redis-cli ping
```

预期：

```text
PONG
```

安装依赖：

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/pip install -r requirements.txt
```

## 启动 worker

终端 1：

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/celery -A app.celery_app:celery_app worker --loglevel=info
```

教学阶段如果只想稳定观察一个 worker 的执行日志，也可以使用：

```bash
/home/tkp666/miniconda3/envs/flowrag/bin/celery -A app.celery_app:celery_app worker --loglevel=info --pool=solo
```

## 启动 API

终端 2：

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --reload
```

## 测试接口

提交成功任务：

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"a":1,"b":2,"fail":false}'
```

提交失败任务：

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"a":1,"b":2,"fail":true}'
```

查询任务：

```bash
curl http://127.0.0.1:8000/tasks/<task_id>
```

## 轻量检查

不启动 Redis / worker 的情况下，可以先跑：

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage6.py
```

通过时输出：

```text
100分：阶段 6 主体实现轻量检查通过
```

## 已验证的真实 Redis 流程

本阶段已经用真实 Redis、FastAPI 和 Celery worker 跑通过：

```bash
redis-cli ping
```

预期：

```text
PONG
```

启动 worker：

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/celery -A app.celery_app:celery_app worker --loglevel=info --pool=solo
```

启动 API：

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8006
```

已验证结果：

- `GET /health` 返回 `{"status":"ok"}`
- `POST /tasks` 会立即返回 `task_id` 和 `queued`
- `GET /tasks/{task_id}` 成功任务最终返回 `SUCCESS` 和结果 `3`
- 失败任务最终返回 `FAILURE` 和错误 `simulated task failure`
