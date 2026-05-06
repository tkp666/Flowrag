# STAGE_PROMPTS.md

本文件用于后续每个阶段开始时复制给 Codex。

每次新阶段开始前，都先让 Codex 读取：

- `AGENTS.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/STAGE_GUIDE.md`
- `docs/LEARNING_LOG.md`
- `docs/STAGE_REPORT.md`

---

# 通用阶段启动提示词

```text
请先阅读并严格遵守项目根目录的 AGENTS.md。

然后阅读：
- docs/PROJECT_CONTEXT.md
- docs/STAGE_GUIDE.md
- docs/LEARNING_LOG.md
- docs/STAGE_REPORT.md

请先查看当前目录树，判断已完成哪些阶段。不要直接改代码。

当前我要进入预备营第 X 阶段：[阶段名称]，目录是：[目录路径]。

请严格按照 docs/STAGE_GUIDE.md 中对应阶段的要求执行。

要求：
1. 先讲解本阶段知识点；
2. 说明它以后在 FlowRAG 中用在哪里；
3. 说明我学到什么程度就够；
4. 再实现最小可运行代码；
5. 不要越阶段引入后续技术；
6. 阶段结束后更新 docs/LEARNING_LOG.md 和 docs/STAGE_REPORT.md；
7. 输出运行命令、测试命令、预期结果、常见报错和 3-5 个检查问题。
```

---

# 阶段 1：FastAPI 最小接口

```text
请先阅读并严格遵守 AGENTS.md、docs/PROJECT_CONTEXT.md、docs/STAGE_GUIDE.md、docs/LEARNING_LOG.md、docs/STAGE_REPORT.md。

当前进入预备营第 1 阶段：FastAPI 最小接口。

目录：
playground/01_fastapi_basic/

请严格按照 docs/STAGE_GUIDE.md 中“阶段 1：FastAPI 最小接口”的要求执行。

只实现：
- GET /health
- POST /items
- GET /items/{item_id}

不要引入数据库、Redis、Celery、Qdrant、RAG、Docker Compose、微服务。

请先讲解，再编码。阶段结束后更新学习日志和阶段报告，并给我检查问题。
```

---

# 阶段 2：FastAPI 分层结构

```text
请先阅读并严格遵守 AGENTS.md、docs/PROJECT_CONTEXT.md、docs/STAGE_GUIDE.md、docs/LEARNING_LOG.md、docs/STAGE_REPORT.md，并查看当前目录树。

当前进入预备营第 2 阶段：FastAPI 分层结构。

目录：
playground/02_fastapi_layering/

请严格按照 docs/STAGE_GUIDE.md 中“阶段 2：FastAPI 分层结构”的要求执行。

本阶段目标：
- 理解 API 层、Service 层、Repository 层、Schema 的职责；
- 使用内存 list 或 dict 模拟知识库数据；
- 实现知识库 CRUD 的最小接口；
- 不引入真实数据库。

只允许实现：
- POST /knowledge-bases
- GET /knowledge-bases
- GET /knowledge-bases/{kb_id}
- DELETE /knowledge-bases/{kb_id}

不要引入 MySQL、Redis、Celery、Qdrant、RAG、登录、Docker Compose、微服务。

请先讲解每一层职责，再编码。阶段结束后更新学习日志和阶段报告，并给我检查问题。
```

---

# 阶段 3：MySQL + SQLAlchemy 基础

```text
请先阅读并严格遵守 AGENTS.md、docs/PROJECT_CONTEXT.md、docs/STAGE_GUIDE.md、docs/LEARNING_LOG.md、docs/STAGE_REPORT.md，并查看当前目录树。

当前进入预备营第 3 阶段：MySQL + SQLAlchemy 基础。

目录：
playground/03_mysql_sqlalchemy/

请严格按照 docs/STAGE_GUIDE.md 中“阶段 3：MySQL + SQLAlchemy 基础”的要求执行。

本阶段目标：
- 连接 MySQL；
- 定义 users 表和 knowledge_bases 表；
- 实现知识库 CRUD；
- 支持分页查询；
- 理解 SQLAlchemy model、Pydantic schema、session、主键、外键、索引。

可以使用本机 MySQL，或者单独用一个 MySQL 容器。不要引入完整 FlowRAG Docker Compose 全家桶。

不要引入 Redis、Celery、Qdrant、RAG、微服务、复杂权限系统。

请先讲解 MySQL 和 SQLAlchemy 的基础概念，再编码。阶段结束后更新学习日志和阶段报告，并给我检查问题。
```

---

# 阶段 4：Redis 基础

```text
请先阅读并严格遵守 AGENTS.md、docs/PROJECT_CONTEXT.md、docs/STAGE_GUIDE.md、docs/LEARNING_LOG.md、docs/STAGE_REPORT.md，并查看当前目录树。

当前进入预备营第 4 阶段：Redis 基础。

目录：
playground/04_redis_basic/

请严格按照 docs/STAGE_GUIDE.md 中“阶段 4：Redis 基础”的要求执行。

本阶段目标：
- 连接 Redis；
- 练习 set/get；
- 练习 expire；
- 练习 incr；
- 实现简单缓存接口；
- 实现简单限流接口；
- 理解 Redis 和 MySQL 的定位区别。

可以使用本机 Redis，或者单独用一个 Redis 容器。不要引入完整项目 Docker Compose。

不要引入 Celery、Qdrant、RAG、微服务、复杂 Lua 限流、Redis 集群。

请先讲解 Redis 基础概念，再编码。阶段结束后更新学习日志和阶段报告，并给我检查问题。
```

---

# 阶段 5：Celery 异步任务

```text
请先阅读并严格遵守 AGENTS.md、docs/PROJECT_CONTEXT.md、docs/STAGE_GUIDE.md、docs/LEARNING_LOG.md、docs/STAGE_REPORT.md，并查看当前目录树。

当前进入预备营第 5 阶段：Celery 异步任务。

目录：
playground/05_celery_basic/

请严格按照 docs/STAGE_GUIDE.md 中“阶段 5：Celery 异步任务”的要求执行。

本阶段目标：
- 实现 POST /tasks，提交模拟耗时任务并立即返回 task_id；
- Celery worker 后台执行任务；
- GET /tasks/{task_id} 查询任务状态；
- 理解 broker、worker、task、result backend；
- 理解为什么 FlowRAG 的文档入库需要异步任务。

可以使用 Redis 作为 Celery broker/result backend。

不要实现真实文档解析、真实 embedding、Qdrant 写入、完整文档入库链路、RAG、微服务。

请先讲解 Celery 基础概念，再编码。阶段结束后更新学习日志和阶段报告，并给我检查问题。
```

---

# 阶段 6：Qdrant 最小向量检索

```text
请先阅读并严格遵守 AGENTS.md、docs/PROJECT_CONTEXT.md、docs/STAGE_GUIDE.md、docs/LEARNING_LOG.md、docs/STAGE_REPORT.md，并查看当前目录树。

当前进入预备营第 6 阶段：Qdrant 最小向量检索。

目录：
playground/06_qdrant_basic/

请严格按照 docs/STAGE_GUIDE.md 中“阶段 6：Qdrant 最小向量检索”的要求执行。

本阶段目标：
- 连接 Qdrant；
- 创建 collection；
- 写入模拟 chunks；
- 每个 chunk 带 text、document_id、kb_id、chunk_index；
- 实现 top-k 检索；
- 实现 kb_id metadata filter；
- 理解 vector、point、payload、collection、top-k、metadata filter。

可以先使用 mock embedding，不要接真实 embedding API。

不要实现真实 LLM、真实 RAG 问答、文档上传、Celery 入库、混合检索、rerank、Elasticsearch、微服务。

请先讲解 Qdrant 和向量检索基础概念，再编码。阶段结束后更新学习日志和阶段报告，并给我检查问题。
```

---

# 阶段 7：流式接口

```text
请先阅读并严格遵守 AGENTS.md、docs/PROJECT_CONTEXT.md、docs/STAGE_GUIDE.md、docs/LEARNING_LOG.md、docs/STAGE_REPORT.md，并查看当前目录树。

当前进入预备营第 7 阶段：流式接口。

目录：
playground/07_streaming_basic/

请严格按照 docs/STAGE_GUIDE.md 中“阶段 7：流式接口”的要求执行。

本阶段目标：
- 实现普通 JSON 响应接口；
- 实现 StreamingResponse 或 SSE 流式接口；
- 模拟 token streaming；
- 用 curl 观察逐步输出；
- 理解普通响应、流式响应、首 token 时间。

不要引入真实 LLM、真实 RAG、Qdrant、Celery、WebSocket、复杂前端、登录权限。

请先讲解流式响应基础概念，再编码。阶段结束后更新学习日志和阶段报告，并给我检查问题。
```

---

# 预备营结束后：进入正式主项目的提示词

```text
请先阅读并严格遵守 AGENTS.md、docs/PROJECT_CONTEXT.md、docs/STAGE_GUIDE.md、docs/LEARNING_LOG.md、docs/STAGE_REPORT.md，并查看当前目录树。

现在 7 个 playground 预备小实验已经完成。请先总结这些实验分别会如何合入正式 FlowRAG 主项目。

然后规划正式主项目 v0.1 的第一阶段，但不要直接写大量代码。

正式主项目 v0.1 第一阶段建议目标：
- 创建 app/ 主项目骨架；
- 建立 common/config、common/response、common/exceptions；
- 建立 api/v1/router；
- 建立 kb 模块；
- 实现 health check；
- 实现 knowledge base CRUD；
- 继续保持 API / Service / Repository 分层。

请先给出阶段计划和目录设计，等待我确认后再开始编码。
```
