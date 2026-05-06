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
