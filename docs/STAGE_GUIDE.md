# STAGE_GUIDE.md

# FlowRAG 预备营阶段指南

本文件定义 FlowRAG 正式主项目开始前的 8 个预备小实验。

核心原则：

- 每次只做一个小实验；
- 每个小实验都必须最小可运行；
- 每个实验都必须和未来 FlowRAG 主项目有关；
- 不要越阶段；
- 不要提前引入当前阶段不需要的技术；
- 口头问题和动手题不能只是把刚写过的代码换名重复一遍；必须尽量换业务场景、换判断角度，考察真实理解；
- 每阶段结束后更新 `docs/LEARNING_LOG.md` 和 `docs/STAGE_REPORT.md`；
- 用户理解检查问题后，再进入下一阶段。

## 课堂执行顺序

完整课堂规则以根目录 `AGENTS.md` 中“最高优先级：课堂规则”为准。

这里给出执行摘要，后续 Codex 不能违背：

1. 先讲当前阶段目标、边界、用途和掌握标准；
2. 讲解时要结合代码、例题或现有文件；
3. 每讲完一个小节后，先给用户提问空间；
4. 用户表示“这小节没问题了”后，先布置该小节的 `小节动手题`；
5. 小节动手题对应的目录、文件或基础骨架由 Codex 先创建，再指定用户去对应文件中完成；
6. 先检查小节动手题结果，再提出该小节的 `3-5 个口头问题`；
7. 根据小节动手题和口头回答情况，决定能否进入下一小节；
8. 只有当当前阶段计划中的关键小节已经讲完后，才允许开始讨论 `阶段主体实现`；
9. 在开始阶段主体实现前，必须等待用户明确回复“可以开始实现”；
10. 一整节课结束时，必须明确宣布结束，并布置 `综合课后动手题`；
11. 一个阶段结束后，必须先让用户回答 `阶段检查问题`，在用户回答并明确同意前，不能进入下一阶段。

## 阶段 6 起默认启用：详细概念块模式

从 `阶段 6：Celery 异步任务` 开始，后续预备营阶段默认使用 `详细概念块模式`。这是用户明确要求的提速方案，但必须注意：提速只压缩低信息量流程，不压缩讲解深度。阶段 6、7、8 用户基本都是 0 基础，讲解要更细、更贴代码、更贴运行过程。

从 2026-05-12 起，阶段 6 及后续阶段默认采用 `模式 D：Codex 主讲主写，用户主理解提问`。Codex 可以直接给出讲解、问题答案、代码实现、运行验证和代码复盘；用户主要负责理解和追问。除非用户主动要求自己动手写，不再强制用户完成每个小节动手题和口头问题后才能推进。

详细概念块模式的原则：

- 不再把每个微小知识点都拆成独立的“小节讲解 -> 小节动手题 -> 口头问题”；
- 每个阶段合并为 2-3 个概念块，每个概念块覆盖多个强相关小点；
- 复杂或 0 基础阶段优先使用 3 个概念块，不要硬压成 2 个；
- 每个概念块必须详细讲解，并结合代码、现有文件、错误示例、运行命令或最小可运行片段；
- 每个阶段通常只保留 1-2 个高质量小节动手题或主体实现前检查；
- 小节动手题和口头问题必须覆盖不同能力点，不能做同质化填空；
- 每个概念块后的口头问题默认压缩为 3 个高质量问题；
- 阶段主体实现、综合课后动手题、阶段检查问题仍然不能省略；
- 用户表示没懂、要求慢一点或要求重讲时，立即暂停提速，回到解释和局部练习；
- 阶段结束后仍必须更新 `docs/LEARNING_LOG.md` 和 `docs/STAGE_REPORT.md`。
- 阶段 6、7、8 必须默认按 0 基础设计讲解：先解释名词和运行角色，再解释代码，再解释 FlowRAG 场景迁移。
- 模式 D 下，小节动手题可以改为 Codex 自问自答式讲解或直接代码实现；阶段检查问题仍需给出，但可以附参考答案，用户只需指出不懂或不同意的地方。

推荐流程：

```text
阶段目标 / 边界 / 掌握标准
  -> 概念块 A：详细讲解 + 代码/命令/错误示例 + 提问空间
  -> 概念块 B：详细讲解 + 代码/命令/错误示例 + 提问空间
  -> 概念块 C：详细讲解 + FlowRAG 迁移 + 提问空间（复杂阶段必须保留）
  -> 1-2 个综合小节动手题或主体实现前检查
  -> 每个关键概念块 3 个高质量口头问题
  -> 阶段主体实现规划
  -> 用户明确同意后开始实现
  -> 运行 / 测试 / 复盘
  -> 明确宣布本节课结束
  -> 综合课后动手题
  -> 阶段检查问题
```

对阶段 6、7、8 的具体建议：

- 阶段 6 Celery：默认 3 个概念块：
  1. 任务边界与角色模型：什么时候用 Celery、什么时候不用、`.delay`、broker、worker、task、result backend、为什么不传文件字节流；
  2. 最小 Celery worker 运行：`celery_app.py`、`tasks.py`、Redis broker/backend、worker 启动命令、任务成功/失败；
  3. FastAPI 接入 Celery 与状态查询：保持 `router / schema / service / repository` 分层思路，`POST /tasks` 立即返回 `task_id`、`GET /tasks/{task_id}` 查询状态、Celery 状态和业务状态的区别。
- 阶段 7 Qdrant：默认 3 个概念块：
  1. 向量检索基本模型：embedding 向量、相似度搜索、collection、point、payload、top-k；
  2. Qdrant 最小写入与查询：创建 collection、upsert points、query/search、payload 返回、向量维度一致性；
  3. FlowRAG 检索边界：MySQL 存文档元数据，Qdrant 存 chunk 向量，检索结果如何回到引用和 chunk 信息。
- 阶段 8 Streaming：默认 3 个概念块：
  1. 普通响应 vs 流式响应：为什么 LLM 回答适合流式、普通 JSON 的等待问题、生成器基本形态；
  2. FastAPI `StreamingResponse` 最小实现：`yield`、`StreamingResponse`、`text/plain` 或 SSE 基础、客户端如何消费；
  3. FlowRAG 流式问答边界：检索先完成再流式生成、引用信息如何处理、流式接口和 Celery 的区别、什么时候用 WebSocket。

## 出题质量要求

后续 Codex 布置口头问题、小节动手题、综合课后动手题时，必须避免严重同质化。

- 不要把用户刚完成的主体实现换一组函数名、接口名后原样作为课后题；
- 不要连续用同一种问题模板反复问同一个知识点；
- 每个小节的口头问题应为 3-5 个，用来判断用户是否真正掌握当前小节，能否进入下一小节；
- 口头问题应优先考察边界判断、错误识别、设计取舍和 FlowRAG 真实场景迁移；
- 动手题应尽量引入新的业务约束，例如依赖关系、失败分支、返回结构设计、是否应该等待、是否应该后台化；
- 如果只是为了确认基础语法，可以设置很短的小题，不要把重复劳动包装成综合题。

阶段主体实现也必须提前规划，不能临时堆接口。开始主体实现前，Codex 必须说明：

- 本次主体实现为什么这样拆；
- 每个文件承担什么职责；
- 哪些部分由用户主写，哪些部分由 Codex 演示或共写；
- 哪些接口、命令或脚本用来验收；
- 这个主体实现和未来 FlowRAG 主项目的连接点是什么；
- 本次实现刻意不做哪些内容，避免越阶段。

出题和主体实现都要优先服务“用户真的掌握并能迁移”，而不是服务“文件数量多”或“流程看起来完整”。

---

# 阶段 0：项目初始化

## 目标

创建项目根目录和基础文档，不写业务代码。

## 目录

```text
FlowRAG/
  AGENTS.md
  README.md
  docs/
    PROJECT_CONTEXT.md
    STAGE_GUIDE.md
    LEARNING_LOG.md
    STAGE_REPORT.md
  prompts/
    FIRST_CODEX_PROMPT.txt
    STAGE_PROMPTS.md
  playground/
```

## 必须讲清楚

- 为什么要有 `AGENTS.md`
- 为什么要有 `PROJECT_CONTEXT.md`
- 为什么先做 `playground`
- 为什么现在不直接写完整项目

## 验收标准

- 项目根目录存在；
- Git 已初始化；
- 文档文件存在；
- Codex 能说明当前阶段边界。

---

# 阶段 1：FastAPI 最小接口

## 目录

```text
playground/01_fastapi_basic/
```

## 学习目标

让用户理解一个后端 HTTP API 是如何被 FastAPI 暴露出来的。

## 必须实现

- `GET /health`
- `POST /items`
- `GET /items/{item_id}`

## 推荐文件结构

```text
playground/01_fastapi_basic/
  README.md
  requirements.txt
  main.py
```

或者：

```text
playground/01_fastapi_basic/
  README.md
  pyproject.toml
  main.py
```

## 必须讲清楚

- FastAPI 是什么；
- 路由是什么；
- HTTP method 是什么；
- path parameter 是什么；
- request body 是什么；
- response body 是什么；
- Pydantic schema 是什么；
- OpenAPI docs 是什么；
- 为什么 FastAPI 适合 AI 后端项目；
- 为什么当前阶段不引入数据库。

## 当前禁止

- 数据库；
- 登录；
- Redis；
- Celery；
- Qdrant；
- RAG；
- Docker Compose；
- 微服务；
- 复杂目录分层。

## 运行命令示例

```bash
cd playground/01_fastapi_basic
python -m venv .venv
source .venv/bin/activate  # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 测试方式示例

```bash
curl http://127.0.0.1:8000/health

curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"demo","description":"first item"}'

curl http://127.0.0.1:8000/items/1
```

浏览器访问：

```text
http://127.0.0.1:8000/docs
```

## 验收标准

- `/health` 返回正常；
- `/items` 能创建内存中的 item；
- `/items/{item_id}` 能读取 item；
- `/docs` 能看到接口文档；
- 用户能解释 path parameter 和 request body 的区别。

## 检查问题示例

1. `GET /health` 为什么通常不用 request body？
2. `POST /items` 里的 JSON 是怎么变成 Python 对象的？
3. Pydantic schema 在这里起什么作用？
4. `/docs` 是谁自动生成的？
5. 为什么现在不用数据库？

---

# 阶段 2：FastAPI 分层结构

## 目录

```text
playground/02_fastapi_layering/
```

## 学习目标

让用户理解 API 层、Service 层、Repository 层、Schema 的基本职责，避免后面主项目中把所有逻辑都写进 router。

## 必须实现

基于内存 dict/list 模拟知识库管理：

- `POST /knowledge-bases`
- `GET /knowledge-bases`
- `GET /knowledge-bases/{kb_id}`
- `DELETE /knowledge-bases/{kb_id}`

## 推荐文件结构

```text
playground/02_fastapi_layering/
  README.md
  requirements.txt
  app/
    main.py
    api/
      kb_router.py
    schemas/
      kb.py
    services/
      kb_service.py
    repositories/
      kb_repository.py
```

## 必须讲清楚

- router 层负责什么；
- schema 层负责什么；
- service 层负责什么；
- repository 层负责什么；
- 为什么不能把所有业务逻辑写在 router；
- 为什么当前 repository 可以先用内存模拟数据库；
- 以后合入 FlowRAG 时，这些层分别会放在哪里。

## 当前禁止

- 真实数据库；
- SQLAlchemy；
- Redis；
- Celery；
- Qdrant；
- 登录鉴权；
- 复杂依赖注入框架。

## 验收标准

- 能创建知识库；
- 能查看知识库列表；
- 能根据 id 查看知识库；
- 能删除知识库；
- 代码中 router 不直接操作底层数据结构；
- 用户能说清楚 router/service/repository 的区别。

## 检查问题示例

1. 如果把所有逻辑都写进 router，会有什么问题？
2. repository 和 service 的区别是什么？
3. schema 为什么不等于数据库 model？
4. 当前内存 repository 将来如何替换成 MySQL repository？
5. FlowRAG 主项目里哪些模块需要分层？

---

# 阶段 3：FastAPI 异步入门

## 目录

```text
playground/03_fastapi_async_intro/
```

## 学习目标

让用户先把同步 / 异步 / 阻塞 / 并发这些基础概念分清楚，再理解 FastAPI 中 `def`、`async def`、`await` 的基本用法，为后面的 Celery 异步任务和流式接口打基础。

## 必须实现

- 一个同步等待接口，例如 `GET /wait-sync`；
- 一个异步等待接口，例如 `GET /wait-async`；
- 一个顺序等待多个子任务的接口，例如 `GET /fanout-sequential`；
- 一个并发等待多个子任务的接口，例如 `GET /fanout-concurrent`；
- 至少演示一次 `time.sleep` 和 `asyncio.sleep` 的区别；
- 至少演示一次 `asyncio.gather`。

## 推荐文件结构

```text
playground/03_fastapi_async_intro/
  README.md
  requirements.txt
  main.py
```

## 必须讲清楚

- 同步是什么；
- 异步是什么；
- 阻塞是什么；
- 并发是什么；
- I/O 密集和 CPU 密集的区别；
- `def` 和 `async def` 在 FastAPI 里的区别；
- `await` 在等待什么；
- `time.sleep` 和 `asyncio.sleep` 的区别；
- `asyncio.gather` 为什么能并发等待多个 I/O；
- 为什么“写成 async”不等于“所有代码都自动更快”；
- 为什么 FastAPI 协程异步不等于 Celery 后台任务异步；
- 这个阶段和后面 Celery、流式接口的承接关系。

## 当前禁止

- Celery；
- Redis；
- MySQL；
- Qdrant；
- 真实外部 API；
- 真实 LLM；
- WebSocket；
- 复杂并发压测工具；
- CPU 密集型性能优化。

## 验收标准

- 用户能说清同步 / 异步 / 阻塞 / 并发的基本区别；
- 能跑通同步等待和异步等待接口；
- 能解释为什么 `time.sleep` 不适合直接塞进 `async def`；
- 能解释 `asyncio.gather` 在做什么；
- 能说明为什么后面还需要 Celery，而不是“有了 async 就够了”。

## 检查问题示例

1. `def` 和 `async def` 在 FastAPI 里什么时候该分别使用？
2. `time.sleep` 和 `asyncio.sleep` 有什么本质区别？
3. `asyncio.gather` 适合解决什么问题？
4. 为什么 FastAPI 的异步不能替代 Celery？
5. 为什么异步对 I/O 等待更有意义，而不是让 CPU 计算自动变快？

---

# 阶段 3 补充专题：并发选型与线程/进程最小模板（不是独立大阶段）

## 定位

这是阶段 3 结束后的短专题，不单独算新的主阶段。

它的作用是：

- 防止用户只会说“这个场景该用线程/进程/Celery”，但不会写最小模板；
- 帮助用户在进入 MySQL / Redis / Celery / Streaming 前，先建立最基本的并发选型能力；
- 明确 `async / 多线程 / 多进程 / Celery` 解决的不是同一类问题。

## 学习目标

让用户掌握“够用的最小并发选型判断”和“最小模板写法”，不深挖底层实现细节。

## 必须讲清楚

- `async` 更适合 I/O 等待；
- 多线程更适合阻塞式 I/O 库的过渡性处理；
- 多进程更适合 CPU 重计算；
- Celery 更适合“不该堵在当前请求里的长后台任务”；
- `async`、线程、进程、Celery 不是替代关系，而是不同场景下的不同工具；
- 为什么“知道该用哪个”还不够，还要掌握最小模板写法。

## 必须覆盖的最小模板

- `ThreadPoolExecutor` 的最小用法；
- `ProcessPoolExecutor` 的最小用法；
- 如何把一个小函数丢进线程池 / 进程池；
- 如何在后端代码里安全地接回返回结果；
- 只要求最小模板，不要求当前就展开锁、条件变量、共享内存、进程通信等复杂主题。

## 当前禁止

- 深挖 GIL 底层实现；
- 深挖线程锁、条件变量、信号量源码；
- 深挖进程通信、共享内存；
- 把这个专题扩展成一个完整的大并发课程；
- 脱离 FlowRAG 主线去做大量纯并发 demo。

## 验收标准

- 用户能根据场景初步判断该优先考虑 `async / 多线程 / 多进程 / Celery` 中的哪一个；
- 用户能写出线程池和进程池的最小模板；
- 用户能解释为什么“必须当前拿结果的 CPU 重任务”不能只靠 `async def`；
- 用户能解释为什么 Celery 和协程异步不是一回事。

## 检查问题示例

1. 什么场景下更适合线程，而不是 `async`？
2. 什么场景下更适合进程，而不是线程？
3. 为什么 CPU 重计算不该指望 `async def` 本身解决？
4. Celery 和线程池 / 进程池最大的职责差别是什么？
5. 如果一个任务不需要当前请求立刻等完，为什么更可能考虑 Celery？

---

# 阶段 4：MySQL + SQLAlchemy 基础

## 目录

```text
playground/04_mysql_sqlalchemy/
```

## 学习目标

让用户理解业务数据为什么放 MySQL，以及 ORM、表、主键、外键、索引、session、CRUD 的基本用法。

## 必须实现

- 连接 MySQL；
- 定义 `users` 表；
- 定义 `knowledge_bases` 表；
- 实现知识库 CRUD；
- `knowledge_bases.user_id` 关联 `users.id`；
- 支持分页查询知识库列表。

## 推荐文件结构

```text
playground/04_mysql_sqlalchemy/
  README.md
  requirements.txt
  app/
    main.py
    db.py
    models.py
    schemas.py
    repositories.py
    services.py
    routers.py
```

简单版可以先不引入 Alembic；如果 Codex 判断用户能承受，再作为“可选扩展”介绍 Alembic，不要强制一开始使用。

## 必须讲清楚

- MySQL 存什么类型的数据；
- 为什么业务数据不放 Qdrant；
- ORM 是什么；
- SQLAlchemy model 是什么；
- Pydantic schema 和 SQLAlchemy model 的区别；
- session 是什么；
- 主键、外键、唯一约束、普通索引分别是什么；
- 为什么 `knowledge_bases.user_id` 需要索引；
- 分页为什么不能一次查全表。

## 当前禁止

- Redis；
- Celery；
- Qdrant；
- RAG；
- 登录完整鉴权；
- 复杂事务；
- 复杂数据库调优；
- 微服务。

## 环境说明

可以使用本机 MySQL，也可以用 Docker 启动单独 MySQL 容器。不要在这个阶段引入完整 FlowRAG Docker Compose 全家桶。

## 验收标准

- MySQL 能连接成功；
- 能创建 user；
- 能创建 knowledge_base；
- 能查询知识库列表；
- 能分页；
- 用户能解释 MySQL、ORM、session、model、schema 的区别和关系。

## 检查问题示例

1. MySQL 和 Qdrant 以后分别存什么？
2. SQLAlchemy model 和 Pydantic schema 有什么区别？
3. session 的作用是什么？
4. 为什么知识库表要有 user_id？
5. 分页查询为什么重要？

---

# 阶段 5：Redis 基础

## 目录

```text
playground/05_redis_basic/
```

## 学习目标

让用户理解 Redis 不是 MySQL 替代品，而是适合做缓存、计数、限流、短期状态和 Celery broker 的内存型组件。

## 必须实现

- Redis 连接；
- `set/get`；
- `expire`；
- `incr`；
- 简单缓存接口；
- 简单限流接口。

## 推荐接口

- `GET /cache/{key}`
- `POST /cache/{key}`
- `POST /counter/{name}/incr`
- `GET /limited-resource`

## 推荐文件结构

```text
playground/05_redis_basic/
  README.md
  requirements.txt
  app/
    main.py
    redis_client.py
```

## 必须讲清楚

- Redis 是什么；
- Redis 和 MySQL 的区别；
- key-value 是什么；
- TTL / expire 是什么；
- incr 为什么适合计数；
- 简单限流的基本思想；
- Redis 在 FlowRAG 中会用于哪些地方：
  - 缓存热点检索结果；
  - 接口限流；
  - 短期任务状态；
  - Celery broker。

## 当前禁止

- Celery；
- Qdrant；
- RAG；
- Redis 集群；
- Redis 哨兵；
- Redis 持久化深入讲解；
- 复杂 Lua 限流；
- 完整鉴权。

## 环境说明

可以使用本机 Redis，也可以用一个单独 Redis 容器，不要引入完整项目 Compose。

## 验收标准

- 能 set/get；
- 能设置过期时间；
- 能 incr；
- 简单限流能在超过次数后返回 429；
- 用户能解释 Redis 为什么不能替代 MySQL。

## 检查问题示例

1. Redis 和 MySQL 最大的定位差异是什么？
2. expire 有什么用？
3. incr 为什么适合做计数？
4. 简单限流是怎么判断请求过多的？
5. FlowRAG 哪些地方适合用 Redis？

---

# 阶段 6：Celery 异步任务

## 目录

```text
playground/06_celery_basic/
```

## 学习目标

让用户理解为什么耗时任务不能阻塞 API 请求线程，以及 Celery、broker、worker、task、result backend 的基本关系。

## 必须实现

- `POST /tasks`：提交一个模拟耗时任务，立即返回 `task_id`；
- Celery worker 后台执行任务；
- 任务中 sleep 几秒模拟耗时处理；
- `GET /tasks/{task_id}`：查询任务状态；
- 任务成功 / 失败状态可见；
- 可选：演示一次重试。

## 推荐文件结构

```text
playground/06_celery_basic/
  README.md
  requirements.txt
  app/
    __init__.py
    main.py
    celery_app.py
    schemas.py
    tasks.py
    api/
      __init__.py
      task_router.py
    services/
      __init__.py
      task_service.py
```

说明：

- `app/api/task_router.py`：HTTP 入口，调用 service，不直接写复杂 Celery 逻辑；
- `app/schemas.py`：请求体和响应体结构；
- `app/services/task_service.py`：封装任务提交、状态查询、模拟业务执行逻辑；Celery 作为 service 使用的后台任务工具；
- `app/celery_app.py`：Celery 工具配置，负责 broker/backend/include；
- `app/tasks.py`：Celery worker 入口文件，用 `@celery_app.task` 注册任务；不要把它理解成新的业务层；
- 本阶段暂时不接 MySQL / Qdrant，因此可以没有 repository；后续正式 FlowRAG 中，service 会通过 repository 访问 MySQL / Redis / Qdrant。

## 必须讲清楚

- 同步请求和异步任务的区别；
- 为什么文档解析、切块、embedding 不应该放在请求线程里；
- Celery 是什么；
- broker 是什么；
- worker 是什么；
- task 是什么；
- result backend 是什么；
- Redis 在 Celery 中可以承担什么角色；
- 队列里为什么不要传大文件内容，只传 task_id / document_id / file_path 这类小信息。
- Celery 不是 `router / schema / service / repository` 之外的新业务层；
- `tasks.py` 是 worker 入口文件，复杂业务逻辑仍应放在 service；
- service 可以使用 Celery 投递后台任务，但 router 不应到处散落 `.delay(...)`。

## 当前禁止

- 真实文档解析；
- 真实 embedding；
- Qdrant；
- 完整文档入库链路；
- 复杂任务编排；
- 微服务；
- 完整 FlowRAG 主项目。

## 验收标准

- API 提交任务后立即返回；
- worker 后台能执行任务；
- 能查询任务状态；
- 用户能解释为什么 Celery 对 FlowRAG 的文档入库重要。

## 检查问题示例

1. 为什么不能在上传接口里直接完成文档解析和 embedding？
2. broker 和 worker 分别是什么？
3. Celery 任务里为什么不建议传完整文件内容？
4. 如果 worker 挂了，API 服务是否一定会挂？
5. FlowRAG 的文档入库任务未来大概包括哪些步骤？

---

# 阶段 7：Qdrant 最小向量检索

## 目录

```text
playground/07_qdrant_basic/
```

## 学习目标

让用户理解向量数据库的基本概念，以及 FlowRAG 为什么需要 MySQL + Qdrant 双存储。

## 必须实现

- 连接 Qdrant；
- 创建 collection；
- 写入若干条模拟 chunk；
- 每个 chunk 至少包含：
  - `text`
  - `document_id`
  - `kb_id`
  - `chunk_index`
- 每个 chunk 有一个向量；
- 支持 top-k 检索；
- 支持按 `kb_id` 做 metadata filter；
- 不要求接真实 embedding 模型，可以先用固定向量或简单 mock embedding。

## 推荐文件结构

```text
playground/07_qdrant_basic/
  README.md
  requirements.txt
  app/
    main.py
    qdrant_client.py
    mock_embedding.py
```

## 必须讲清楚

- 向量是什么；
- embedding 是什么；
- 向量数据库是什么；
- Qdrant collection 是什么；
- point 是什么；
- payload 是什么；
- top-k search 是什么；
- metadata filter 是什么；
- 为什么 chunk 要带 document_id / kb_id；
- 为什么业务数据放 MySQL，向量放 Qdrant；
- 引用回溯以后如何依赖 chunk_id / document_id。

## 当前禁止

- 真实 LLM；
- 真实 RAG 问答；
- 文档上传；
- Celery 入库；
- 混合检索；
- rerank；
- Elasticsearch；
- 微服务。

## 验收标准

- 能写入模拟 chunks；
- 能检索 top-k；
- 能用 kb_id 限制检索范围；
- 用户能解释 Qdrant 和 MySQL 的分工；
- 用户能解释 payload 的作用。

## 检查问题示例

1. Qdrant 里 point、vector、payload 分别是什么？
2. 为什么检索时要带 kb_id filter？
3. 为什么不能只用 MySQL 做语义检索？
4. document_id 和 chunk_index 对引用回溯有什么用？
5. 真实项目中 mock embedding 会替换成什么？

---

# 阶段 8：流式接口

## 目录

```text
playground/08_streaming_basic/
```

## 学习目标

让用户理解普通 JSON 响应和流式响应的区别，以及 AI 问答为什么常用流式输出。

## 必须实现

- 一个普通 JSON 接口，例如 `GET /normal-answer`；
- 一个流式接口，例如 `GET /stream-answer`；
- 流式接口每隔一小段时间返回一个 token；
- 支持用 curl 观察逐步输出。

## 推荐文件结构

```text
playground/08_streaming_basic/
  README.md
  requirements.txt
  main.py
```

## 必须讲清楚

- 普通响应和流式响应的区别；
- StreamingResponse 是什么；
- SSE 是什么；
- token streaming 是什么；
- 首 token 时间是什么；
- 为什么 AI 问答不能总是等完整回答生成完再返回；
- FlowRAG 未来的 `/chat/stream` 会如何使用这个能力。

## 当前禁止

- 真实 LLM；
- 真实 RAG；
- Qdrant；
- Celery；
- WebSocket；
- 复杂前端；
- 登录权限。

## 验收标准

- 普通接口一次性返回；
- 流式接口逐步返回；
- 用户能用 curl 观察流式输出；
- 用户能解释为什么流式问答有意义。

## 检查问题示例

1. 普通 JSON 响应和流式响应有什么区别？
2. 首 token 时间为什么重要？
3. StreamingResponse 的基本原理是什么？
4. SSE 和 WebSocket 有什么不同，为什么现在先不用 WebSocket？
5. FlowRAG 的 chat/stream 未来大概会经历哪些步骤？

---

# 预备营完成后的主项目启动条件

只有当用户完成以上 8 个小实验，并能回答各阶段检查问题后，才开始正式 FlowRAG 主项目。

正式主项目第一阶段建议：

```text
FlowRAG v0.1 主项目骨架：
- app/main.py
- app/api/v1/router.py
- app/common/config.py
- app/common/response.py
- app/common/exceptions.py
- app/modules/kb/
- health check
- knowledge base CRUD
```

正式主项目要把预备营中学过的内容逐步合入，而不是重新堆一个用户看不懂的大工程。
