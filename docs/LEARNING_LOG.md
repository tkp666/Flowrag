# LEARNING_LOG.md

本文件记录用户在 FlowRAG 项目驱动学习中的阶段性学习收获。

请 Codex 每完成一个阶段后，按下面格式追加内容。

---

## 模板

```markdown
## 日期 - 阶段名称

### 本阶段知识点

### 这些知识在 FlowRAG 中的用途

### 我应该掌握到什么程度

### 本阶段常见错误

### 面试可能怎么问

### 我还不熟的地方
```

## 2026-04-30 - 阶段 1：FastAPI 最小接口

### 本阶段知识点

- FastAPI 应用对象 `app = FastAPI(...)`
- 路由的基本组成：`method + path + 对应函数`
- `GET` 和 `POST` 的基本语义区别
- `path parameter`、`query parameter`、`request body`、`response body`
- Pydantic `BaseModel` 用来描述请求体和响应体结构
- `response_model=...` 用来声明成功响应的数据结构
- `/docs` 是根据路由和 schema 自动生成的
- `HTTPException` 用来返回真正的 HTTP 错误，而不是伪造错误字典
- 当前阶段先用内存 `dict`，不引入数据库

### 这些知识在 FlowRAG 中的用途

- 后续正式项目里的健康检查、知识库、文档、任务、对话接口都基于同样的路由模式
- 请求体 schema 会用于创建知识库、上传文档、发起聊天、发起检索等接口
- 响应体 schema 会用于统一返回知识库信息、任务状态、对话结果
- `/docs` 会成为后续接口联调和自测的重要入口
- `HTTPException` 会用于“资源不存在”“参数不合法”“权限不足”等错误场景

### 我应该掌握到什么程度

- 能读懂一个最小 FastAPI 文件，按 `app -> schema -> 路由` 的顺序理解
- 能分清 `path parameter`、`query parameter`、`request body`、`response body`
- 能解释 `response_model` 和函数里临时创建对象的区别
- 能自己写出 `GET /health`、`POST /items`、`GET /items/{item_id}` 这种最小接口
- 能说明为什么当前阶段先用内存 `dict` 而不是数据库

### 本阶段常见错误

- 把 `HTTPException` 从 `pydantic` 导入，而不是从 `fastapi` 导入
- 路径里的参数名和函数参数名写得不一致
- 误以为 `return {"status": "404"}` 就是真正的 404 响应
- 给接口写了 `response_model`，但失败分支返回了完全不同的结构
- 把 `dict`、schema、请求体、响应体这几个概念混在一起

### 面试可能怎么问

- `GET` 和 `POST` 在语义上有什么区别？
- `path parameter` 和 `request body` 的区别是什么？
- FastAPI 里为什么推荐用 Pydantic schema，而不是直接用 `dict`？
- `/docs` 是怎么自动生成的？
- 为什么 `response_model` 和 `HTTPException` 经常一起出现？

### 我还不熟的地方

- 成功响应和错误响应为什么要分开处理
- `response_model` 对 `/docs` 和响应校验的具体影响
- `HTTPException` 的更多使用场景

## 2026-05-04 - 阶段 2：FastAPI 分层结构

### 本阶段知识点

- `router` 负责 HTTP 入口，不直接碰底层存储
- `service` 负责业务规则、流程编排和响应组装，不只是中转站
- `repository` 负责底层数据存取能力
- `schema` 负责接口输入输出格式，和 repository / 数据库 model 不是一回事
- 同一个业务对象可以有多套 schema
- service 可以调用多个 repository 完成一件完整业务事
- 完整目录结构的作用是让职责真正落位，而不是为了“看起来像项目”

### 这些知识在 FlowRAG 中的用途

- 知识库、文档、任务、对话等模块后面都要按层组织
- 路由层以后只保留请求入口和参数声明
- 业务判断、状态转换、组合响应要放到 service
- 数据库 / Redis / 向量库等底层实现后面都要封装进 repository
- 不同接口场景可以分别设计列表 schema、详情 schema、创建 schema

### 我应该掌握到什么程度

- 能看出一段代码应该放在 `router / service / repository / schema` 的哪一层
- 能解释为什么 `service` 不只是纯转发
- 能解释为什么 `repository` 可以做 count / filter / limit，但不该决定业务规则
- 能看懂一个分层目录结构，并知道每个文件的职责
- 能从接口需求反推调用链，而不是把所有逻辑都写进 router

### 本阶段常见错误

- 把 `router` 写成胖层，直接操作底层存储
- 把 `service` 写成空壳，只会 `return repository_xxx(...)`
- 把 `schema` 和 repository record 混为一谈
- 认为 `repository` 只能做最原始的增删改查，不能做筛选统计
- 目录结构看起来分层了，但职责实际上没分开

### 面试可能怎么问

- `router / service / repository` 分别负责什么？
- 为什么 `service` 不是纯中转层？
- `schema` 和数据库 model 的区别是什么？
- 为什么列表页和详情页可能需要不同 schema？
- repository 可以做哪些查询能力，哪些事情不该它决定？

### 我还不熟的地方

- 如何把分层思维更自然地迁移到真实 MySQL / Redis / Celery 项目中
- service 调多个 repository 时，哪些属于流程编排，哪些属于过度耦合
- 什么时候该为列表、详情、创建、更新分别设计独立 schema

## 2026-05-05 - 阶段 3：FastAPI 异步入门

### 本阶段知识点

- `async def` 调用后先得到协程对象，真正执行需要 `await`
- `time.sleep(...)` 是同步阻塞等待
- `await asyncio.sleep(...)` 是异步等待，会在等待期间交出事件循环控制权
- `def` 路由适合普通同步/阻塞式逻辑
- `async def` 路由适合当前请求必须等待、且主要等待 I/O 的逻辑
- 顺序 `await` 会按依赖顺序执行，不会缩短当前请求链路
- `asyncio.gather(...)` 可以并发等待多个互不依赖的异步 I/O
- FastAPI 的协程异步和 Celery 后台任务异步不是一回事
- CPU 重计算不能指望只靠 `async def` 自动变快

### 这些知识在 FlowRAG 中的用途

- 聊天接口等待外部 LLM API 时，可以用异步 I/O，避免等待期间卡住事件循环
- 多个互不依赖的外部 I/O 查询可以用 `asyncio.gather(...)` 合并等待
- 文档上传后的解析、切块、embedding、入库流程不应堵在当前请求里，后续更适合交给 Celery
- 流式接口之前需要先理解协程异步和阻塞调用的边界
- CPU 重的 OCR、复杂 PDF 解析、批量计算后续要结合线程/进程/Celery 选型，而不是只写成 `async def`

### 我应该掌握到什么程度

- 能解释 `time.sleep` 和 `asyncio.sleep` 的本质区别
- 能写出 `def` 同步等待接口和 `async def` 异步等待接口
- 能写出顺序 `await` 和 `asyncio.gather(...)` 的最小模板
- 能根据场景初步判断当前请求是否应该等待完成
- 能说明为什么 FastAPI 的 `async/await` 不能替代 Celery
- 能说明顺序 `await` 虽然不缩短当前请求，但能提升整体并发能力

### 本阶段常见错误

- 以为函数写成 `async def` 后，内部所有逻辑都会自动变快
- 在 `async def` 里调用 `time.sleep(...)` 或同步阻塞库，导致事件循环被卡住
- 创建协程对象后忘记 `await`，出现 `coroutine was never awaited`
- 把 `res = ...` 写进 `asyncio.gather(...)` 参数列表，误以为是在接返回值
- 把“当前请求必须等结果”和“应该用 async def”直接画等号，忽略 CPU 重计算场景
- 把“任务很长”和“async def 能解决”直接画等号，忽略 Celery 后台任务场景

### 面试可能怎么问

- `def` 和 `async def` 在 FastAPI 中分别适合什么场景？
- `time.sleep` 和 `await asyncio.sleep` 的区别是什么？
- `asyncio.gather` 适合什么样的 I/O 场景？
- 为什么顺序 `await` 仍然有价值？
- 为什么 FastAPI 的异步不能替代 Celery？
- CPU 密集任务为什么不能只靠 `async def` 优化？

### 我还不熟的地方

- 对“并发、并行、线程、进程、Celery”的边界还需要通过补充专题继续梳理
- 后续动手题应减少同质化，改成更贴近 FlowRAG 业务场景的综合判断题
- 对真实 HTTP 客户端、数据库驱动哪些是异步库、哪些是同步阻塞库还需要后续结合具体工具学习

## 2026-05-05 - 阶段 3 补充专题：并发选型与线程/进程最小模板

### 本阶段知识点

- `async_io` 适合当前请求必须等结果、且主要等待异步 I/O 的场景
- `ThreadPoolExecutor` 适合当前请求必须等结果、但内部调用同步阻塞 I/O SDK 的场景
- `ProcessPoolExecutor` 适合当前请求必须等结果、且任务是 CPU 密集计算的场景
- `Celery` 适合当前请求不应该等待、任务需要后台慢慢执行的场景
- `loop.run_in_executor(...)` 可以把同步函数交给线程池或进程池执行
- `functools.partial(...)` 可以给 `run_in_executor(...)` 包装关键字参数
- `asyncio.gather(...)` 可以等待多个互不依赖的线程池/进程池任务
- 线程池、进程池、Celery 不是同一层工具，Celery 任务内部以后也可以再结合进程池

### 这些知识在 FlowRAG 中的用途

- PDF 前几页预览如果必须马上返回，且 PDF SDK 是同步阻塞的，可以用线程池
- chunk 质量扫描、OCR 后处理、规则清洗这类 CPU 重计算，可以考虑进程池
- 上传 200 篇文档后的解析、切块、embedding、入库，不应堵住当前请求，应交给 Celery
- 聊天接口等待外部 LLM API 且必须返回结果时，更适合异步 I/O
- 后续设计任务接口时，需要区分 `200 当前结果已完成` 和 `202 后台任务已接收`

### 我应该掌握到什么程度

- 能先判断当前 HTTP 请求是否必须等待结果
- 能根据 I/O 等待、同步阻塞 SDK、CPU 重计算、后台长任务区分四类工具
- 能写出线程池和进程池的最小 `run_in_executor(...)` 模板
- 能说明为什么同步阻塞函数直接放进 `async def` 会卡住事件循环
- 能说明为什么复杂对象不适合直接传入进程池
- 能为后台任务接口设计最小响应结构，例如 `task_id` 和 `status`

### 本阶段常见错误

- 以为只要任务耗时长就应该用 `async def`
- 以为线程池可以很好解决纯 Python CPU 重计算
- 在 `run_in_executor(...)` 里提前调用函数，导致阻塞函数仍然在当前线程执行
- 忘记 `return`，导致分支实际返回 `None`
- 把后台任务状态写成 `done`，混淆“已入队”和“已完成”
- 把 `request`、数据库 session、Qdrant client 等复杂对象直接传进进程池

### 面试可能怎么问

- `async`、线程池、进程池、Celery 分别适合什么场景？
- 为什么 FastAPI 的 `async def` 不能替代 Celery？
- 为什么同步阻塞 SDK 在 `async def` 中需要特别处理？
- CPU 密集任务为什么通常更适合进程池？
- Celery 和进程池是二选一吗？

### 我还不熟的地方

- 真实 Celery 的任务定义、投递、状态查询还没开始学
- 真实 MySQL / Redis / Qdrant 客户端哪些是同步、哪些是异步，还需要后续结合具体工具判断
- 进程池底层细节、GIL、进程通信目前只需要知道边界，不需要深挖

## 2026-05-06 - 阶段 4：MySQL + SQLAlchemy 基础

### 本阶段知识点

- MySQL 适合存用户、知识库、文档元数据、任务状态等结构化业务数据
- SQLAlchemy model 对应数据库表，Pydantic schema 对应 API 输入输出结构
- 主键用于唯一标识一条记录，外键用于保证跨表引用关系合法
- 普通索引用于加速常见查询，唯一约束用于保证业务唯一性
- `Session` 是一次数据库操作上下文，负责 add / query / commit / refresh
- `session.get(Model, id)` 按主键查询，`select(...).where(...)` 用于更灵活的条件查询
- `offset / limit / order_by` 用于分页查询，`count` 用于统计总数
- 软删除需要在 active 查询里统一过滤 `is_deleted == False`
- service 层负责业务规则和权限边界，repository 层负责封装数据库查询能力

### 这些知识在 FlowRAG 中的用途

- `users` 会保存用户基础信息
- `knowledge_bases` 会保存知识库归属、名称、描述、软删除状态
- `documents` 会保存上传文档的元数据、入库状态和所属知识库
- 文档属于知识库、知识库属于用户，这类关系后续都需要用外键和业务校验共同保证
- 分页会用于知识库列表、文档列表、任务列表、对话列表
- schema 边界会用于防止用户伪造 `user_id / kb_id / is_deleted / ingest_status` 等内部字段

### 我应该掌握到什么程度

- 能定义一个最小 SQLAlchemy model，并区分字段类型、nullable、index、unique、ForeignKey
- 能说明 SQLAlchemy model 和 Pydantic schema 的职责差异
- 能写出最小创建、按主键查询、列表分页、更新、软删除流程
- 能解释 `add / commit / refresh` 分别做什么
- 能判断哪些字段应该由用户传，哪些字段应该由后端上下文或数据库生成
- 能说明外键和索引不是一回事：外键管关系合法性，索引管查询速度

### 本阶段常见错误

- 把外键理解成“自动加索引的 int”，忽略外键真正作用是保证引用合法
- 把数据库 model 直接当 API schema 暴露，导致内部字段泄漏
- 在创建 schema 中允许用户传 `user_id / kb_id / is_deleted / status` 这类内部控制字段
- 软删除后列表查询忘记过滤 `is_deleted == False`
- 把 `len(items)` 当成总数，忽略分页总数需要单独 `count`
- 更新名称时把当前记录自己误判成重名冲突
- 忘记软删除和唯一约束之间的策略冲突：`(user_id, name)` 唯一约束会阻止删除后重建同名知识库

### 面试可能怎么问

- MySQL 和 Qdrant 分别适合存什么？
- SQLAlchemy model 和 Pydantic schema 有什么区别？
- 主键、外键、索引、唯一约束分别解决什么问题？
- `session.add()`、`session.commit()`、`session.refresh()` 分别做什么？
- 分页接口为什么通常要同时查 `items` 和 `total`？
- 软删除有什么好处和代价？
- service 和 repository 在数据库 CRUD 中怎么分工？

### 我还不熟的地方

- 外键和索引的边界已经纠正，但后续需要在真实表设计里继续巩固
- 软删除和唯一约束的组合策略还需要在主项目正式 schema 设计时再决策
- 当前使用 SQLite 做教学检查，真实 MySQL 连接、迁移和部署还没有深入展开
- Alembic 迁移、复杂事务、并发写入冲突、数据库调优暂时不深挖

## 2026-05-08 - 阶段 5：Redis 基础

### 本阶段知识点

- Redis 适合缓存、计数器、限流、短期过程状态和 Celery broker，不适合替代 MySQL 做权威业务存储
- MySQL 保存长期、结构化、需要追溯的权威数据
- Redis 的 key 命名只是约定，冒号没有真实目录含义
- TTL / expire 用来控制短期数据生命周期
- `INCR` 是 Redis 原子计数操作，适合并发计数和简单限流
- Cache Aside 的基本流程是先查 Redis，未命中再查 MySQL，然后写回 Redis
- MySQL 更新后应主动删除相关缓存，让下一次查询回源 MySQL
- 限流 key 应按用户、动作等维度拆开，超限返回 `429`
- `ttl(key) == -1` 表示 key 存在但没有过期时间，验证码、限流、短期状态类 key 需要修复 TTL
- Python 的 `**dict` 可以把字典展开成 Pydantic schema 的字段参数

### 这些知识在 FlowRAG 中的用途

- 知识库详情、热点检索结果、非关键统计结果可以放 Redis 缓存
- 用户聊天、验证码、上传等接口可以用 Redis 计数做限流
- 文档入库任务的实时进度可以放 Redis，最终状态和错误原因写 MySQL
- Celery 后续可以使用 Redis 作为 broker
- 知识库新增文档、改名、删除等操作需要主动失效相关缓存

### 我应该掌握到什么程度

- 能解释 Redis 和 MySQL 的职责边界
- 能设计清晰的 Redis key，并说明每个 key 的 TTL
- 能写出 `setex / get / delete / incr / expire / ttl` 的基本代码
- 能实现 Cache Aside，并解释缓存命中、未命中、更新失效三个分支
- 能用 `INCR + 首次 expire` 实现固定窗口限流
- 能说明 Redis 过程状态丢失时，不能直接把任务判定为失败
- 能把知识库缓存场景迁移到文档任务进度场景

### 本阶段常见错误

- 把 Redis 当成 MySQL 替代品，把关键业务数据只放 Redis
- 过程进度和最终任务状态混在一起，导致 Redis 丢数据后误判任务失败
- 每次 `INCR` 后都重新 `expire`，把固定窗口限流变成不断续期
- 超限后删除限流 key，导致用户可以绕过限流
- MySQL 更新后只等 TTL 自然过期，忽略应主动删除强相关缓存
- Redis key 没有 TTL，导致验证码、限流、任务进度长期残留
- 把所有用户或所有动作混到同一个限流 key 里

### 面试可能怎么问

- Redis 和 MySQL 在项目里分别负责什么？
- Cache Aside 是什么流程？更新 MySQL 后为什么通常删缓存而不是更新缓存？
- Redis 的 `INCR` 为什么比 `get -> +1 -> set` 更适合并发计数？
- 为什么固定窗口限流通常只在第一次计数时设置 TTL？
- 任务进度适合放 Redis 吗？最终失败原因应该放哪里？
- 如果 Redis 缓存和 MySQL 数据不一致，你以谁为准？

### 我还不熟的地方

- 当前阶段还没有学习 Celery，文档入库任务只是进度状态设计，没有真正后台执行
- Redis 持久化、集群、哨兵、Lua 限流暂时不深入
- 当前主体实现使用 SQLite + SQLAlchemy 模拟真实数据库，正式主项目再切到 MySQL
- 阶段 5 综合课后动手题已完成并通过检查
- 限流题回答时要主动提到 `INCR` 的原子性：并发下不能用 `get -> +1 -> set`

## 2026-05-11 - 阶段 6 起课堂节奏调整：详细概念块模式

### 调整原因

- 用户反馈前面阶段按完整逐小节流程推进过慢，每个阶段大约需要两天
- 后续还需要完成 Celery、Qdrant、Streaming，并尽快进入 FlowRAG 主项目
- 继续机械拆分小节会增加低信息量重复，影响 6 月投递版进度

### 新节奏

- 从阶段 6 起默认启用 `详细概念块模式`
- 每个阶段合并为 2-3 个概念块
- 复杂或 0 基础阶段优先使用 3 个概念块，不硬压成 2 个
- 每个概念块仍必须详细讲解，并结合代码、错误示例、运行命令或最小可运行片段
- 每个阶段保留 1-2 个高质量小节动手题或主体实现前检查
- 口头问题压缩为 3 个关键问题
- 阶段主体实现、综合课后动手题、阶段检查问题仍不可省略
- 阶段 6、7、8 必须按 0 基础组织：先讲名词和运行角色，再讲代码，再讲 FlowRAG 迁移

### 质量底线

- 不减少必须掌握的知识点
- 不压缩讲解深度，只压缩低信息量流程
- 不跳过代码运行和检查
- 不再布置大量同质化填空题
- 优先做真实可运行实验、错误设计修正和 FlowRAG 场景迁移
- 如果用户表示没懂或要求慢一点，立即暂停提速并回到解释

### 阶段 6 重置说明

- 用户要求清空阶段 6 目录，并按详细概念块模式重新进入阶段 6
- 旧的阶段 6 小节练习文件已删除
- 新阶段 6 应直接围绕 Celery 最小可运行实验组织讲解和练习
- 已讲过的 `.delay / broker / worker / result backend / 不传文件字节流` 概念不需要机械重复出题，但需要在主体实现和检查问题中确认掌握

### 阶段 6 分层纠偏

- Celery 不是新的业务分层，不应讲成“Celery 层”
- 继续坚持阶段 2 的 `router / schema / service / repository` 思路
- `celery_app.py` 是 Celery 配置文件，属于工具接入
- `tasks.py` 是 worker 入口文件，用于注册 Celery task，也属于工具接入
- service 可以封装任务投递、状态查询和业务流程编排
- router 不应散落复杂 `.delay(...)` 调用，应该调用 service
- 本阶段不接 MySQL / Qdrant，因此可以暂时没有 repository；后续接存储时由 repository 负责底层访问

### 2026-05-12 课堂职责调整

- 用户要求后续由 Codex 主讲、主写、给出问题答案、给代码并讲代码
- 用户主要负责理解和追问，不再强制承担每个小节的动手题和口头问题
- 后续默认使用 `模式 D：Codex 主讲主写，用户主理解提问`
- 小节动手题和口头问题可以改为 Codex 自问自答式讲解
- 阶段主体实现由 Codex 直接规划、实现、运行验证和复盘
- 质量底线不变：不能省略关键概念、运行验证、常见报错和 FlowRAG 迁移说明

### 阶段 6-8 默认概念块

- 阶段 6 Celery：
  1. 任务边界与角色模型；
  2. 最小 Celery worker 运行；
  3. FastAPI 接入 Celery 与状态查询。
- 阶段 7 Qdrant：
  1. 向量检索基本模型；
  2. Qdrant 最小写入与 top-k 查询；
  3. MySQL / Qdrant 职责边界与 FlowRAG 检索迁移。
- 阶段 8 Streaming：
  1. 普通响应与流式响应区别；
  2. FastAPI `StreamingResponse` 最小实现；
  3. FlowRAG 流式问答、引用返回和 Celery 边界。

## 2026-05-12 - 阶段 6：Celery 异步任务主体实现

### 本阶段知识点

- Celery 适合当前 API 不应该等待完成的后台耗时任务
- `.delay(...)` 是任务投递快捷方式，不是在当前 API 进程里直接执行函数
- Redis 在本阶段同时作为 Celery broker 和 result backend，但二者职责不同
- broker 负责暂存待执行任务消息，worker 从 broker 取任务并执行
- result backend 负责保存任务执行结果和状态，API 可通过 `task_id` 查询
- `tasks.py` 是 worker 可发现的任务入口，不是新的业务层
- `service` 可以封装任务投递、状态查询和业务函数，router 不直接散落 Celery 细节
- `PENDING` 既可能表示任务还没执行，也可能表示 result backend 查不到该 `task_id`
- `task_track_started=True` 只能让 worker 有机会写入 `STARTED`，查询端是否看见还取决于任务执行时机和轮询时机

### 这些知识在 FlowRAG 中的用途

- 文档上传后，API 应尽快返回任务 ID，不应该等待解析、切块、embedding 和入库全部完成
- 文档入库任务可由 Celery worker 在后台执行
- Redis 可以作为 Celery broker，也可以保存短期进度；最终任务状态仍应写入 MySQL
- 正式项目中 router 继续调用 service，service 负责投递 Celery 任务和查询任务状态
- worker 入口任务应保持较薄，真正业务流程应交给 service 或后续专门的业务编排函数

### 我应该掌握到什么程度

- 能画出 `API -> service -> broker -> worker -> result backend -> API 查询` 的链路
- 能解释 `.delay(...)` 为什么立即返回 `task_id`
- 能区分 broker、worker、task、result backend
- 能解释为什么不把大文件字节流直接塞进 Celery 消息
- 能读懂 `celery_app.py / tasks.py / task_service.py / task_router.py` 的职责
- 能说明 Celery 不改变原来的 `router / schema / service / repository` 分层

### 本阶段常见错误

- 把 Celery 当成新的业务层，破坏原来的 service 分层
- 在 router 里到处直接调用 `.delay(...)`，导致任务投递逻辑分散
- 以为 `.delay(...)` 会在当前请求里等待任务执行完
- 把文件字节流、数据库 session、request 对象等复杂或大对象直接传给 worker
- 没有让 worker 导入任务模块，导致 worker 不知道任务存在
- 把 `PENDING` 直接理解成“任务一定正在排队”

### 面试可能怎么问

- Celery 的 broker、worker、result backend 分别是什么？
- `.delay(...)` 做了什么？它和直接调用函数有什么区别？
- 为什么上传文件后通常只传文件路径或对象存储 key 给 Celery？
- Celery 接入后，原来的 router / service / repository 分层怎么保持？
- 为什么 `PENDING` 不能直接等同于“任务正在执行中”？

### 我还不熟的地方

- 正式 FlowRAG 中还需要把任务最终状态写入 MySQL，本阶段暂时只查 Celery result backend
- 文档入库的真实解析、切块、embedding、Qdrant 写入还没开始
- Celery 重试、超时、任务幂等、并发池调优和监控暂时不深挖

## 2026-06-04 - 阶段 7：Qdrant 最小向量检索

### 课堂纠偏说明

- 阶段 7 代码曾被 Codex 直接生成并验证通过，但没有先完成基础概念讲解和代码导读
- 用户已明确反馈看不懂实现内容，说明阶段 7 不能按“已完成学习”处理
- 已暂停推进阶段 8，并从 Qdrant / embedding / vector / payload / top-k / filter 的基础概念重新讲起
- 已围绕现有代码完成 mock embedding、Qdrant 写入、top-k 查询、`kb_id` filter、运行命令和阶段检查问题导读
- 用户已在 2026-06-10 确认阶段 7 检查问题没有不清楚的地方

### 本阶段知识点

- embedding 向量是文本的数值表示，真实项目中由 `EmbeddingProvider` 产生
- 本阶段用 mock embedding 稳定模拟向量，避免把模型 API 和 Qdrant 基础混在一起
- Qdrant `collection` 是一组向量点的集合，collection 内向量维度必须一致
- Qdrant `point` 通常包含 `id`、`vector` 和 `payload`
- `payload` 保存检索后需要回溯的业务信息，例如 `text`、`document_id`、`kb_id`、`chunk_index`
- top-k 检索返回最相似的前 k 条 point
- `kb_id` filter 用于把检索范围限制在当前知识库内，避免跨知识库返回结果
- 低分结果仍可能被 top-k 返回，真实项目后续还需要 `score_threshold`、rerank 或更好的 embedding

### 这些知识在 FlowRAG 中的用途

- 文档入库时，文档会先切成 chunks，再为每个 chunk 生成 embedding
- chunk 向量会写入 Qdrant，chunk 的业务归属和引用字段会放在 payload 中
- 用户发起问答时，查询文本会先转成 query embedding，再到 Qdrant 做 top-k 检索
- `kb_id` filter 会确保只在当前知识库内检索
- Qdrant 返回的 `document_id` 和 `chunk_index` 是后续引用回溯的基础
- MySQL 保存权威业务数据，Qdrant 保存向量和检索必要 payload，二者不是替代关系

### 我应该掌握到什么程度

- 能解释 `collection / point / vector / payload / top-k / filter` 的含义
- 能读懂 `mock_embedding.py` 如何把文本转成固定维度向量
- 能读懂 `qdrant_client.py` 如何创建 collection、写入 points、执行检索
- 能说明为什么检索必须带 `kb_id` filter
- 能说明为什么 Qdrant 不适合替代 MySQL 存权威业务数据
- 能说明真实项目中 mock embedding 会被 `EmbeddingProvider` 替换

### 本阶段常见错误

- 把 Qdrant 当成 MySQL 的替代品，把所有业务字段都塞进 Qdrant
- 只存 vector，不存 `document_id / kb_id / chunk_index`，导致检索后无法引用回溯
- 创建 collection 时向量维度和后续写入向量维度不一致
- 检索时忘记加 `kb_id` filter，导致跨知识库返回结果
- 误以为 top-k 返回的一定都是高质量结果，忽略低分结果和阈值判断
- 把 mock embedding 当成真实语义能力，忽略它只是教学替身

### 面试可能怎么问

- Qdrant 里的 collection、point、vector、payload 分别是什么？
- 为什么 FlowRAG 需要 MySQL + Qdrant，而不是只用其中一个？
- 为什么向量检索时必须加 `kb_id` filter？
- document_id 和 chunk_index 对引用回溯有什么作用？
- 真实项目中 mock embedding 应该替换成什么？

### 我还不熟的地方

- 真实 embedding 模型的选择、调用和批量写入还没开始
- Qdrant 的索引参数、集合优化、删除更新、备份迁移暂时不深挖
- 混合检索、rerank、score threshold、引用排序会在正式 FlowRAG 或后续阶段再展开

## 2026-06-11 - 阶段 8：Streaming 流式接口

### 本阶段知识点

- 普通 JSON 响应必须等完整结果生成后一次性返回，流式响应可以在一个 HTTP 连接中分多次返回内容
- Python 生成器 / 异步生成器可以通过 `yield` 一段段产出数据，`StreamingResponse` 会消费这些数据并写回客户端
- SSE 是基于 HTTP 的单向服务端推送格式，典型格式是 `event: ...`、`data: ...`，并用空行分隔事件
- `media_type="text/event-stream"` 表示当前响应是 SSE 流
- `curl -N` 可以关闭客户端侧缓冲，更容易观察一段段返回
- 流式响应开始前还能返回正常 HTTP 错误；流开始后通常不能再改 HTTP 状态码，只能在流里发送 `error` 事件
- FlowRAG 问答一般应先完成检索，再返回 references，然后流式返回 LLM token
- Celery 适合后台长任务，SSE 适合当前请求正在生成并需要持续返回结果，WebSocket 适合双向实时通信

### 这些知识在 FlowRAG 中的用途

- 聊天问答接口可以用 SSE 边生成边返回 token，降低用户等待感
- 检索得到的引用片段可以先通过 `references` 事件返回给前端
- LLM 生成中的 token 可以通过 `token` 事件持续返回
- 检索失败或模型中途失败时，可以用 `error` 事件让前端停止等待并展示错误状态
- 文档上传和入库仍应交给 Celery，不应该用一个长 SSE 请求一直挂着做后台入库
- 正式主项目中，`mock_rag.py` 会逐步替换为 `RetrievalService`、`LLMProvider` 和 `ChatService`

### 我应该掌握到什么程度

- 能解释普通 JSON 响应和流式响应的区别
- 能读懂 `StreamingResponse(generator, media_type=...)` 的基本形态
- 能解释 SSE 的 `event / data / \n\n` 分别起什么作用
- 能说明为什么流开始前错误和流开始后错误处理方式不同
- 能设计 FlowRAG 最小事件顺序：`status -> references -> status -> token -> done/error`
- 能区分聊天流式生成、文档后台入库和双向实时通信分别适合 SSE、Celery 还是 WebSocket

### 本阶段常见错误

- 以为 `StreamingResponse` 自己会凭空生成数据，忽略必须传入可迭代对象或生成器
- 把所有失败都写成 `raise HTTPException(500)`，没有区分流开始前和流开始后
- 忘记 SSE 事件之间的空行，导致客户端无法正确拆分事件
- 把普通 `text/plain` 流当成完整业务流，导致前端无法区分 token、引用、错误和结束
- 在 `async def` 或异步生成器里调用同步阻塞 SDK，导致事件循环被卡住
- 误以为 SSE 能替代 Celery，把文档入库这类后台任务也设计成长连接

### 面试可能怎么问

- 普通响应和流式响应有什么区别？为什么 LLM 问答适合流式？
- FastAPI 的 `StreamingResponse` 需要什么样的数据源？
- SSE 的基本格式是什么？为什么要有 `event` 和 `data`？
- 流已经开始后，后端还能随便改 HTTP 状态码吗？出错怎么办？
- FlowRAG 为什么通常先检索再流式生成？
- SSE、WebSocket、Celery 分别适合什么场景？

### 我还不熟的地方

- 真实 LLM Provider 的流式 SDK 接入还没开始
- 真实 Qdrant 检索结果如何和 MySQL 文档元数据组合成更完整引用，还需要进入主项目后落地
- 生产环境中的代理缓冲、超时、心跳、断线重连和客户端取消暂时只讲了边界，没有深入实现
