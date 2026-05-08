# 阶段 5：Redis 基础主体实现

本实验把前面几节内容组装起来：

- FastAPI 分层结构；
- SQLAlchemy 数据库读写；
- Redis 缓存、计数器、限流；
- Cache Aside：先查 Redis，未命中再查 MySQL，然后写回 Redis；
- MySQL 更新后主动删除 Redis 缓存。

本阶段不做异步数据库读写，不做 Celery，不做 Qdrant，也不进入正式 FlowRAG 主项目。

## 文件职责

```text
playground/05_redis_basic/
  app/
    main.py              FastAPI 路由入口
    db.py                SQLAlchemy engine / Session / 建表
    models.py            数据库表模型
    schemas.py           请求体和响应体
    repositories.py      MySQL 查询、更新、演示数据写入
    services.py          业务流程，尤其是 Cache Aside
    redis_client.py      Redis 连接
    redis_services.py    Redis key、缓存、计数器、限流
  check_stage5.py        一键检查脚本
  requirements.txt       依赖
```

## 你需要完成的 TODO

主要集中在 3 个文件：

- `app/repositories.py`
  - `kb_repository_get_active_by_id`
  - `kb_repository_update`
- `app/redis_services.py`
  - `get_kb_detail_cache`
  - `set_kb_detail_cache`
  - `delete_kb_detail_cache`
  - `incr_counter`
  - `check_rate_limit`
- `app/services.py`
  - `kb_service_get_detail_with_cache`
  - `kb_service_update_and_invalidate_cache`

## 运行方式

先确认 Redis 正在运行：

```bash
redis-cli ping
```

应该返回：

```text
PONG
```

安装依赖：

```bash
cd /home/tkp666/FlowRAG/playground/05_redis_basic
/home/tkp666/miniconda3/envs/flowrag/bin/pip install -r requirements.txt
```

启动服务：

```bash
cd /home/tkp666/FlowRAG/playground/05_redis_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --reload
```

## 手动测试接口

初始化演示数据：

```bash
curl -X POST http://127.0.0.1:8000/dev/seed
```

第一次查知识库，应该从 MySQL 回源：

```bash
curl http://127.0.0.1:8000/knowledge-bases/1
```

预期 `source` 是：

```text
mysql
```

第二次查同一个知识库，应该命中 Redis：

```bash
curl http://127.0.0.1:8000/knowledge-bases/1
```

预期 `source` 是：

```text
redis
```

更新知识库，并删除缓存：

```bash
curl -X PATCH http://127.0.0.1:8000/knowledge-bases/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"paper-kb-v2","description":"更新后的论文知识库"}'
```

再次查询，应该重新从 MySQL 回源，且看到新名称：

```bash
curl http://127.0.0.1:8000/knowledge-bases/1
```

计数器：

```bash
curl -X POST http://127.0.0.1:8000/counter/demo/incr
curl -X POST http://127.0.0.1:8000/counter/demo/incr
```

限流接口，默认 60 秒内最多 3 次：

```bash
curl "http://127.0.0.1:8000/limited-resource?user_id=1&action=chat"
curl "http://127.0.0.1:8000/limited-resource?user_id=1&action=chat"
curl "http://127.0.0.1:8000/limited-resource?user_id=1&action=chat"
curl -i "http://127.0.0.1:8000/limited-resource?user_id=1&action=chat"
```

第 4 次应该返回 `429`。

## 一键检查

```bash
cd /home/tkp666/FlowRAG/playground/05_redis_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage5.py
```

通过时输出：

```text
100分：阶段 5 主体实现检查全部通过
```

## 验收标准

- 第一次查知识库返回 `source=mysql`；
- 第二次查同一个知识库返回 `source=redis`；
- 更新知识库后，对应 Redis 缓存被删除；
- 更新后再次查询返回 MySQL 新值；
- 计数器使用 `INCR`，首次创建时设置 TTL；
- 限流按 `user_id + action` 分 key；
- 超过阈值返回 `429`；
- router 不直接写 MySQL 查询和 Redis 细节。
