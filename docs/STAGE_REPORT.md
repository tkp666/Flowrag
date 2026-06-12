# STAGE_REPORT.md

本文件记录 FlowRAG 预备营和主项目每个阶段的完成情况。

请 Codex 每完成一个阶段后，按下面格式追加内容。

---

## 当前课堂状态（后续 Codex 必须先看）

- 当前课堂规则以根目录 `AGENTS.md` 中“最高优先级：课堂规则”为准。
- 当前课堂顺序以 `AGENTS.md` 和 `docs/STAGE_GUIDE.md` 中的课堂执行顺序为准。
- 当前项目仍处于预备营阶段，只允许在 `playground/` 范围内教学与实验。
- 在用户未完成当前阶段检查问题、未明确同意继续前，任何 Codex 不得推进到下一阶段。
- 当前最重要目标不是赶进度，而是按课堂模式完成讲解、提问、小节动手题、口头问题、实现、复盘和阶段检查问答。
- 每个小节的小节动手题检查通过后，必须提出 3-5 个口头问题，用来判断用户是否能进入下一小节。
- 用户已再次强调：口头问题、动手题和阶段主体实现质量必须高，必须避免同质化；后续 Codex 出题和实现前要先规划考察点、业务差异、验收标准和 FlowRAG 迁移价值。
- 从阶段 5 第 3 小节开始，动手题应优先改为真实代码练习；在环境允许时，应连接真实 Redis，而不是继续只做文字判断题。
- 预备营阶段规划已更新：在原阶段 2 后新增“阶段 3：FastAPI 异步入门”，后续 MySQL / Redis / Celery / Qdrant / Streaming 阶段顺延。
- 阶段 5：Redis 基础已完成；综合课后动手题和阶段检查问题均已通过。
- 阶段 6：Celery 异步任务已完成主体实现、代码复盘、综合课后题参考答案和阶段检查题参考答案。
- 阶段 7：Qdrant 最小向量检索已完成主体代码、补充概念讲解、代码导读、运行命令导读和阶段检查问题确认。
- 用户已要求清空阶段 6 目录，并按 `详细概念块模式` 重新开始阶段 6；`playground/06_celery_basic/` 已清空并重新创建为空目录。
- 阶段 6 之前按旧节奏创建的 `section_01_task_boundary.py` 和 `section_02_celery_roles.py` 已删除，不再作为当前阶段 6 的必做作业；其中涉及的知识点会合并进新的阶段 6 概念块、主体实现前检查和阶段检查问题中。
- 用户已明确反馈：此前综合动手题和口头问题同质化严重。后续出题必须减少重复模板，改为考察边界判断、错误识别、设计取舍、FlowRAG 真实业务迁移；不要把刚写过的代码换名后再次布置。
- 用户已再次明确要求：后续阶段不要继续按完整逐小节流程拖慢进度。从阶段 6 起默认启用 `详细概念块模式`，每个阶段合并为 2-3 个概念块，复杂或 0 基础阶段优先使用 3 个概念块；讲解必须详细、结合代码和运行过程，保留 1-2 个高质量小节动手题或主体实现前检查、阶段主体实现、综合课后动手题和阶段检查问题。
- 阶段 6、7、8 用户基本都是 0 基础，后续 Codex 必须按 0 基础设计讲解：先解释名词和运行角色，再解释代码，再解释 FlowRAG 场景迁移，不能因为提速而跳过关键概念。
- 阶段 6 已完成一次重要纠偏：Celery 不是新的业务分层；后续必须继续坚持阶段 2 的 `router / schema / service / repository` 思路。`celery_app.py` 和 `tasks.py` 只是 Celery 工具接入文件，service 可以使用 Celery 投递任务和查询状态，router 不应散落复杂 Celery 逻辑；本阶段不接 MySQL / Qdrant 时可以暂时没有 repository。
- 用户已明确将后续课堂切换为 `模式 D：Codex 主讲主写，用户主理解提问`：Codex 负责讲课、给问题答案、给代码并讲代码，用户负责理解和追问。后续不再强制用户完成每个小节动手题或口头问题后才能推进，但 Codex 仍必须保证讲解质量、运行验证、代码复盘和 FlowRAG 迁移说明。
- 阶段 7：Qdrant 最小向量检索已完成，用户已在 2026-06-10 确认阶段 7 检查问题没有不清楚的地方。
- 阶段 8：Streaming 流式接口已完成概念块 A/B/C、主体实现、主体实现拆分、运行验证、综合课后题参考实现和阶段记录更新。
- 用户已在 2026-06-11 确认阶段 8 课后动手题和检查问题没有疑问。
- 预备营阶段 1-8 已完成；下一步可以开始讨论正式 FlowRAG 主项目第一版落地路线，但仍需先讲清范围、文件、验收标准和课堂实现模式。

---

## 模板

```markdown
## 日期 - 阶段名称

### 阶段目标

### 完成内容

### 新增 / 修改文件

### 运行命令

### 测试命令

### 测试结果

### 已知问题

### 用户需要回答的检查问题

### 下一阶段建议
```

## 2026-04-30 - 阶段 1：FastAPI 最小接口

### 阶段目标

- 理解 FastAPI 最小接口的基本组成
- 完成 `GET /health`
- 完成 `POST /items`
- 完成 `GET /items/{item_id}`
- 理解路由、HTTP method、path parameter、request body、response body、Pydantic schema、OpenAPI docs

### 完成内容

- 完成了 5 个核心小节讲解与练习
- 完成了 1 个综合课后动手题
- 完成了 `playground/01_fastapi_basic/main.py` 的主体实现
- 主体实现已升级到更规范版本：
  - `GET /items/{item_id}` 使用 `response_model=ItemResponse`
  - item 不存在时抛出 `HTTPException(status_code=404, ...)`

### 新增 / 修改文件

- `playground/01_fastapi_basic/main.py`
- `playground/01_fastapi_basic/requirements.txt`
- `playground/01_fastapi_basic/README.md`
- `playground/01_fastapi_basic/homework/section_01_route_methods.py`
- `playground/01_fastapi_basic/homework/section_02_path_request_response.py`
- `playground/01_fastapi_basic/homework/section_03_pydantic_schema.py`
- `playground/01_fastapi_basic/homework/section_04_openapi_docs.py`
- `playground/01_fastapi_basic/homework/section_05_minimal_fastapi_overview.py`
- `playground/01_fastapi_basic/homework/lesson_01_case_study.py`
- `playground/01_fastapi_basic/homework/lesson_01_case_study_answers.md`

### 运行命令

```bash
conda activate flowrag
cd /home/tkp666/FlowRAG/playground/01_fastapi_basic
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### 测试命令

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"demo","description":"first item"}'
```

```bash
curl http://127.0.0.1:8000/items/1
```

```bash
curl http://127.0.0.1:8000/items/999
```

### 测试结果

- `GET /health` 逻辑返回：`{"status": "ok"}`
- `POST /items` 逻辑返回：`{"id": 1, "name": "demo", "description": "first item"}`
- `GET /items/1` 逻辑返回：`{"id": 1, "name": "demo", "description": "first item"}`
- `GET /items/999` 会抛出真正的 `404`，错误信息为：`Item not found!`
- 当前执行环境对本地回环连接有隔离，无法在这里直接用 `curl 127.0.0.1:8000` 访问同一进程里的 `uvicorn`；
  已通过直接调用路由函数和路由注册检查验证逻辑正确

### 已知问题

- `GET /items/{item_id}` 当前还没有额外的输入约束，比如 `item_id > 0`
- 还没有引入正式数据库，重启服务后内存数据会丢失
- 还没有进入分层结构，当前所有逻辑都还在一个文件中

### 用户需要回答的检查问题

1. `GET /health` 为什么通常不需要 `request body`？
2. `POST /items` 里的 `item: ItemCreate` 为什么属于 `request body`？
3. `GET /items/{item_id}` 里的 `item_id` 为什么属于 `path parameter`？
4. `response_model=HealthResponse` 和在函数里临时创建 `HealthResponse(...)` 对象，本质区别是什么？
5. 为什么给 `GET /items/{item_id}` 补上 `response_model` 后，找不到 item 时不应该再 `return {"status": "404"}`？

### 下一阶段建议

- 如果阶段 1 检查问题回答稳定，再进入阶段 2：FastAPI 分层结构
- 阶段 2 的重点会从“最小接口”转向“router / service / repository 的职责划分”

## 2026-05-04 - 阶段 2：FastAPI 分层结构

### 阶段目标

- 理解 `router / service / repository / schema` 的职责边界
- 理解 `schema` 和 repository / 数据库 model 不是一回事
- 理解 `service` 不只是中转站，而是业务规则与流程编排的承载层
- 理解完整目录结构里各文件应该放什么
- 完成一个最小可运行的知识库分层实验

### 完成内容

- 完成了 5 个核心小节讲解与练习
- 完成了阶段 2 的主体实现骨架
- 完成了最小可运行的知识库分层实验：
  - `POST /knowledge-bases`
  - `GET /knowledge-bases`
  - `GET /knowledge-bases/{kb_id}`
  - `DELETE /knowledge-bases/{kb_id}`
- 通过 `flowrag` 环境直接调用 app / router / service 逻辑验证：
  - 创建、列表、详情、软删除都正常
  - 删除后再次查询会报 `知识库已删除`
- 预备营中已新增“阶段 3：FastAPI 异步入门”，后续阶段顺延

### 新增 / 修改文件

- `playground/02_fastapi_layering/README.md`
- `playground/02_fastapi_layering/requirements.txt`
- `playground/02_fastapi_layering/app/main.py`
- `playground/02_fastapi_layering/app/api/kb_router.py`
- `playground/02_fastapi_layering/app/schemas/kb.py`
- `playground/02_fastapi_layering/app/services/kb_service.py`
- `playground/02_fastapi_layering/app/repositories/kb_repository.py`
- `playground/02_fastapi_layering/homework/section_01_layer_split.py`
- `playground/02_fastapi_layering/homework/section_02_schema_vs_repository.py`
- `playground/02_fastapi_layering/homework/section_03_service_business_rules.py`
- `playground/02_fastapi_layering/homework/section_04_workflow_orchestration.py`
- `playground/02_fastapi_layering/homework/section_05_directory_landing.py`
- `playground/02_fastapi_layering/homework/lesson_02_layering_blueprint.md`

### 运行命令

```bash
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --reload
```

### 测试命令

```python
from app.main import app
from app.api.kb_router import create_kb, list_kbs, get_kb, delete_kb
from app.schemas.kb import KBCreate
from app.services.kb_service import kb_service_create, kb_service_list, kb_service_get, kb_service_delete
```

### 测试结果

- 路由注册正常：
  - `/knowledge-bases`
  - `/knowledge-bases/{kb_id}`
- 创建接口返回正常：
  - `{'id': 1, 'name': 'demo-kb', 'description': 'first kb'}`
- 列表接口返回正常：
  - 未删除知识库列表正确
- 详情接口返回正常：
  - 可返回单条知识库详情
- 删除接口返回正常：
  - `{'status': 'deleted'}`
- 重复查询已删除项会抛出：
  - `知识库已删除`
- 由于当前执行环境限制，不能直接起本地 `uvicorn` 监听端口并使用真实 `curl 127.0.0.1:8000`
  - 已通过 `flowrag` 环境下直接调用 app / router / service 逻辑完成验证

### 已知问题

- 当前 repository 仍然使用内存 `dict` 模拟数据库，重启后会丢失数据
- 当前 `owner_id` 还是教学阶段的固定值，没有接真实登录系统
- `kb_service.py` 里仍然导入了 `next_kb_id_ref`，这是教学阶段的简化写法，后面可再优化
- 目前还没有接真实数据库、Redis、Celery、Qdrant

### 用户需要回答的检查问题

1. 如果以后在 `app/api/kb_router.py` 里看到直接操作 `fake_kb_table[...]`，你第一反应应该是什么？
2. 如果以后新增知识库列表接口，`id / name / doc_count` 这几样分别会由哪些层配合完成？
3. 如果把 `KBCreate` 写进 `app/services/kb_service.py`，为什么仍然不是一个好放法？
4. 如果以后要新增“恢复已删除知识库”，这条逻辑核心应该主要放在 `service` 还是 `repository`？为什么？
5. 如果某个接口最终返回里同时混了基础信息、统计信息和展示裁剪字段，你第一反应应该怎么理解它？

### 下一阶段建议

- 先完成阶段 2 的检查问题与收尾确认
- 再进入新增的阶段 3：FastAPI 异步入门
- 阶段 3 结束后，再继续 MySQL / Redis / Celery / Qdrant / Streaming 的顺序推进

## 2026-05-05 - 阶段 3：FastAPI 异步入门

### 阶段目标

- 理解同步、异步、阻塞、并发的基本区别
- 理解 FastAPI 中 `def`、`async def`、`await` 的基本用法
- 理解 `time.sleep(...)` 和 `await asyncio.sleep(...)` 的区别
- 理解顺序 `await` 和 `asyncio.gather(...)` 的耗时差异
- 理解 FastAPI 协程异步不能替代 Celery 后台任务
- 为后续 Celery 和流式接口打基础

### 完成内容

- 完成了 3 个核心小节动手题：
  - 协程对象、同步等待、异步并发等待对比
  - `def` / `async def` / 阻塞调用边界
  - FastAPI async 和 Celery 适用边界
- 完成阶段 3 主体实现：
  - `GET /health`
  - `GET /wait-sync`
  - `GET /wait-async`
  - `GET /fanout-sequential`
  - `GET /fanout-concurrent`
- 完成阶段 3 综合课后动手题：
  - `GET /file-preview`
  - `GET /llm-call`
  - `GET /dashboard-sequential`
  - `GET /dashboard-concurrent`
- 完成阶段 3 检查问题，用户能说明：
  - `time.sleep` 会阻塞，`asyncio.sleep` 会交出控制权
  - `asyncio.gather` 能并发等待互不依赖的 I/O
  - 顺序 `await` 不一定缩短当前请求，但能提升整体并发能力
  - 文档批量入库这类长任务更适合 Celery
  - CPU 重计算不能只靠 `async def` 解决

### 新增 / 修改文件

- `playground/03_fastapi_async_intro/main.py`
- `playground/03_fastapi_async_intro/requirements.txt`
- `playground/03_fastapi_async_intro/README.md`
- `playground/03_fastapi_async_intro/homework/section_01_async_basics_compare.py`
- `playground/03_fastapi_async_intro/homework/section_02_def_vs_asyncdef.py`
- `playground/03_fastapi_async_intro/homework/section_03_async_vs_celery_boundary.py`
- `playground/03_fastapi_async_intro/homework/lesson_03_async_routes_practice.py`

### 运行命令

```bash
cd /home/tkp666/FlowRAG/playground/03_fastapi_async_intro
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn main:app --reload
```

综合课后动手题运行：

```bash
cd /home/tkp666/FlowRAG/playground/03_fastapi_async_intro/homework
/home/tkp666/miniconda3/envs/flowrag/bin/python lesson_03_async_routes_practice.py
```

### 测试命令

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/wait-sync
curl http://127.0.0.1:8000/wait-async
curl http://127.0.0.1:8000/fanout-sequential
curl http://127.0.0.1:8000/fanout-concurrent
```

直接调用验证：

```python
from main import health, wait_sync, wait_async, fanout_sequential, fanout_concurrent
```

### 测试结果

- 主体实现直接调用验证通过：
  - `/wait-sync` 耗时约 2 秒
  - `/wait-async` 耗时约 2 秒
  - `/fanout-sequential` 耗时约 6 秒
  - `/fanout-concurrent` 耗时约 2 秒
- 综合课后动手题验证通过：
  - 输出 `lesson 03 async routes homework looks good`
- 路由注册正常：
  - `/health`
  - `/wait-sync`
  - `/wait-async`
  - `/fanout-sequential`
  - `/fanout-concurrent`
  - `/file-preview`
  - `/llm-call`
  - `/dashboard-sequential`
  - `/dashboard-concurrent`

### 已知问题

- 当前只是最小教学实验，还没有接真实异步 HTTP 客户端、异步数据库驱动或 LLM API
- 当前还没有并发压测，只用耗时对比说明基本行为
- 当前综合课后动手题和主体实现同质化偏高，后续题目应提高业务差异度，避免重复劳动
- 当前还没有进入线程池、进程池、Celery 的模板级写法

### 用户需要回答的检查问题

用户已完成阶段 3 检查问题，本阶段通过。

复盘时需要记住的关键回答：

1. `time.sleep(2)` 会阻塞；`await asyncio.sleep(2)` 会在等待期间交出控制权。
2. `asyncio.gather(...)` 适合并发等待多个互不依赖的异步 I/O。
3. 顺序 `await` 不一定缩短当前请求，但会在 I/O 等待期间释放事件循环，让其他请求有机会继续执行。
4. 上传 200 篇文档并入库这类长任务不应让当前请求一直等待，更适合 Celery 后台任务。
5. CPU 重计算不能只靠 `async def` 加速，后续需要学习线程/进程/Celery 的选型边界。

### 下一阶段建议

- 在用户明确同意后，进入“阶段 3 补充专题：并发选型与线程/进程最小模板”
- 补充专题不是独立大阶段，但不能省略
- 专题完成后，再进入阶段 4：MySQL + SQLAlchemy 基础

## 2026-05-05 - 阶段 3 补充专题：并发选型与线程/进程最小模板

### 阶段目标

- 区分 `async_io`、线程池、进程池、Celery 的适用边界
- 理解当前请求是否必须等待结果，是并发工具选型的第一判断点
- 掌握线程池和进程池的最小模板
- 能把并发选型迁移到 FlowRAG 的聊天、PDF 预览、chunk 清洗、文档入库等场景

### 完成内容

- 完成小节 1：并发工具选型地图
  - 判断 `async_io / thread_pool / process_pool / celery_background`
  - 完成 `section_04_concurrency_choice.py`
- 完成小节 2：`ThreadPoolExecutor` 最小模板
  - 理解同步阻塞 SDK 在 `async def` 中的问题
  - 练习 `loop.run_in_executor(...)`
  - 练习位置参数和 `functools.partial(...)` 关键字参数
  - 完成 `section_05_thread_pool_preview.py`
- 完成小节 3：`ProcessPoolExecutor` 最小模板
  - 理解 CPU 密集任务和阻塞 I/O 的区别
  - 练习把多个 chunk 清洗任务提交到进程池
  - 完成 `section_06_process_pool_chunks.py`
- 完成综合课后动手题
  - 根据 FlowRAG 场景设计并发工具选型和响应结构
  - 完成 `lesson_04_concurrency_decision_plan.py`
- 完成专题最终检查问题
  - 用户能说明聊天接口更偏异步 I/O
  - 用户能说明文档批量入库更适合 Celery
  - 用户能说明同步 PDF SDK 应交给线程池
  - 用户能说明 CPU 重计算应考虑进程池
  - 用户能说明 Celery 和进程池不是二选一

### 新增 / 修改文件

- `playground/03_fastapi_async_intro/homework/section_04_concurrency_choice.py`
- `playground/03_fastapi_async_intro/homework/section_05_thread_pool_preview.py`
- `playground/03_fastapi_async_intro/homework/section_06_process_pool_chunks.py`
- `playground/03_fastapi_async_intro/homework/lesson_04_concurrency_decision_plan.py`
- `docs/LEARNING_LOG.md`
- `docs/STAGE_REPORT.md`

### 运行命令

```bash
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/03_fastapi_async_intro/homework/section_04_concurrency_choice.py
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/03_fastapi_async_intro/homework/section_05_thread_pool_preview.py
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/03_fastapi_async_intro/homework/section_06_process_pool_chunks.py
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/03_fastapi_async_intro/homework/lesson_04_concurrency_decision_plan.py
```

### 测试命令

同运行命令，当前补充专题使用脚本内置 `self_check()` / `assert` 完成自查。

### 测试结果

- `section_04_concurrency_choice.py` 通过，输出：
  - `concurrency choice answers are complete`
- `section_05_thread_pool_preview.py` 通过，输出：
  - `thread pool preview homework looks good`
  - `elapsed: 0.201s`
- `section_06_process_pool_chunks.py` 通过，输出：
  - `process pool chunks homework looks good`
- `lesson_04_concurrency_decision_plan.py` 通过，输出：
  - `concurrency decision plan homework looks good`

### 已知问题

- 当前只是线程池/进程池的最小模板，还没有进入真实 Celery 任务系统
- 当前没有接真实 PDF SDK、OCR、LLM API、数据库或向量库
- 当前没有做并发压测，只做了功能和选型验证
- 进程池在 Codex 沙箱中可能不稳定，真实 `flowrag` 环境运行通过

### 用户需要回答的检查问题

用户已完成补充专题最终检查问题，本专题通过。

复盘时需要记住的关键回答：

1. 当前请求必须等外部 LLM 返回结果时，更适合异步 I/O，不适合 Celery。
2. 上传 200 篇文档后的解析、切块、embedding、入库应返回 `task_id` 和状态，后台用 Celery 执行。
3. 在 `async def` 中直接调用同步 PDF SDK 会阻塞事件循环；当前请求必须返回预览时，可用线程池。
4. 纯 Python 大量循环计算是 CPU 密集任务，线程池通常不是最佳选择，应考虑进程池。
5. Celery 和进程池不是二选一，Celery 任务内部也可以把独立 CPU 重任务交给进程池。

### 下一阶段建议

- 用户明确同意后，进入阶段 4：MySQL + SQLAlchemy 基础
- 阶段 4 应继续保持预备营小实验，不直接开发完整 FlowRAG 主项目
- 阶段 4 重点应放在表、字段、主键、SQLAlchemy model、session、CRUD、事务边界的最小可运行实验

## 2026-05-06 - 阶段 4：MySQL + SQLAlchemy 基础

### 阶段目标

- 理解 MySQL 在 FlowRAG 中负责结构化业务数据，而不是向量检索数据
- 理解 SQLAlchemy model、Pydantic schema、Session、Repository、Service 的关系
- 掌握主键、外键、普通索引、唯一约束、联合唯一约束的最小用法
- 能实现知识库的创建、查询、分页、更新和软删除
- 能把文档元数据设计迁移到 `documents` 表，理解文档和知识库之间的外键关系

### 完成内容

- 完成小节 1：表、主键、外键、索引、唯一约束、联合唯一约束
  - 完成 `section_01_table_constraints.py`
- 完成小节 2：SQLAlchemy model 和 Pydantic schema 的职责边界
  - 完成 `section_02_model_vs_schema.py`
  - 追加完成 `section_02b_sqlalchemy_model_schema.py`
- 完成小节 3：Session 和 CRUD
  - 完成 `section_03_session_crud.py`
  - 追加实现“修改某个用户用户名”的练习
- 完成小节 4：分页查询
  - 完成 `section_04_pagination.py`
- 完成阶段 4 主体实现
  - `GET /health`
  - `POST /knowledge-bases`
  - `GET /knowledge-bases/{kb_id}`
  - `GET /knowledge-bases`
  - `PATCH /knowledge-bases/{kb_id}`
  - `DELETE /knowledge-bases/{kb_id}`
- 完成阶段 4 综合课后动手题
  - `lesson_04_document_metadata_design.py`
  - 设计 `documents` 表、文档创建、文档分页列表、文档软删除
- 完成阶段 4 检查问题
  - 用户能解释 schema 边界、session 三步、分页 total、软删除过滤
  - 外键概念已重点纠偏：外键管关系合法性，索引管查询速度

### 新增 / 修改文件

- `playground/04_mysql_sqlalchemy/README.md`
- `playground/04_mysql_sqlalchemy/requirements.txt`
- `playground/04_mysql_sqlalchemy/.gitignore`
- `playground/04_mysql_sqlalchemy/app/db.py`
- `playground/04_mysql_sqlalchemy/app/models.py`
- `playground/04_mysql_sqlalchemy/app/schemas.py`
- `playground/04_mysql_sqlalchemy/app/repositories.py`
- `playground/04_mysql_sqlalchemy/app/services.py`
- `playground/04_mysql_sqlalchemy/app/routers.py`
- `playground/04_mysql_sqlalchemy/app/main.py`
- `playground/04_mysql_sqlalchemy/check_stage4.py`
- `playground/04_mysql_sqlalchemy/check_stage4_detailed.py`
- `playground/04_mysql_sqlalchemy/demo_update_name_conflict.py`
- `playground/04_mysql_sqlalchemy/homework/section_01_table_constraints.py`
- `playground/04_mysql_sqlalchemy/homework/section_02_model_vs_schema.py`
- `playground/04_mysql_sqlalchemy/homework/section_02b_sqlalchemy_model_schema.py`
- `playground/04_mysql_sqlalchemy/homework/section_03_session_crud.py`
- `playground/04_mysql_sqlalchemy/homework/section_04_pagination.py`
- `playground/04_mysql_sqlalchemy/homework/lesson_04_document_metadata_design.py`
- `docs/LEARNING_LOG.md`
- `docs/STAGE_REPORT.md`

### 关键文件作用

- `app/db.py`：创建数据库 engine、SessionLocal、初始化表结构
- `app/models.py`：定义 `users` 和 `knowledge_bases` 的 SQLAlchemy model
- `app/schemas.py`：定义知识库 API 请求和响应 schema
- `app/repositories.py`：封装数据库查询、创建、更新、软删除、分页统计能力
- `app/services.py`：处理知识库业务规则，例如归属、重名、软删除过滤、响应组装
- `app/routers.py`：提供 FastAPI 路由，并把业务错误映射为 HTTP 状态码
- `check_stage4.py`：主体实现基础检查脚本
- `check_stage4_detailed.py`：更细的业务边界检查脚本
- `lesson_04_document_metadata_design.py`：综合课后题，迁移到文档元数据设计场景

### 运行命令

```bash
cd /home/tkp666/FlowRAG/playground/04_mysql_sqlalchemy
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --reload
```

### 测试命令

```bash
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/check_stage4.py
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/check_stage4_detailed.py
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/homework/lesson_04_document_metadata_design.py
```

### 测试结果

- `check_stage4.py` 通过，输出：
  - `100分：阶段 4 主体实现检查全部通过`
- `check_stage4_detailed.py` 通过，输出：
  - `100分：阶段 4 详细检查全部通过`
- `lesson_04_document_metadata_design.py` 通过，输出：
  - `lesson 04 document metadata design homework looks good`

### 已知问题

- 当前教学实验主要用 SQLite 本地文件和内存库检查，还没有深入真实 MySQL 部署、迁移、备份和权限配置
- 当前没有引入 Alembic，后续正式主项目需要用迁移工具管理表结构变化
- 当前软删除后不能重建同名知识库，因为数据库存在 `(user_id, name)` 联合唯一约束；如果主项目希望“只禁止未删除知识库重名”，需要调整唯一约束策略
- 当前登录用户仍然是教学阶段模拟值，还没有接真实登录鉴权
- 当前没有展开复杂事务、并发写入冲突和数据库调优

### 用户需要回答的检查问题

用户已完成阶段 4 检查问题，本阶段通过。

复盘时需要记住的关键回答和纠偏：

1. `documents.kb_id` 应该是外键，因为每个文档必须属于真实存在的知识库；外键保证引用合法，普通 int 不会检查合法性。
2. `DocumentCreateSchema` 不应该让用户传 `id / kb_id / ingest_status / is_deleted`；这些字段应由数据库、路径参数、后端上下文或后端默认值控制。
3. `session.add()` 把对象加入会话，`commit()` 提交并持久化，`refresh()` 从数据库同步生成值或最新值。
4. 分页中 `items` 是当前页数据，`total` 是符合条件的全部数量，不能用 `len(items)` 代替。
5. 软删除后列表查询必须过滤 `is_deleted == False`，过滤条件应封装在 repository 的 active 查询中，由 service 决定业务上调用哪个查询。

### 下一阶段建议

- 用户已经询问是否可以进入下一阶段，可以进入阶段 5：Redis 基础
- 阶段 5 继续保持预备营小实验，不直接接入完整 FlowRAG 主项目
- 阶段 5 重点放在 Redis 的定位、`set/get`、过期时间、计数器、简单缓存、简单限流

## 2026-05-08 - 阶段 5：Redis 基础

### 阶段目标

- 理解 Redis 不是 MySQL 替代品，而是缓存、计数、限流、短期状态和 Celery broker
- 掌握 Redis key 设计、`set/get`、TTL、`expire`、`INCR`
- 能实现 Cache Aside 查询和 MySQL 更新后的缓存失效
- 能实现用户维度的简单固定窗口限流
- 能把 Redis 思路迁移到 FlowRAG 的文档入库任务进度场景

### 完成内容

- 完成小节 1：Redis 是什么，和 MySQL 的职责边界
  - 完成 `section_01_redis_mysql_boundary.py`
- 完成小节 2：key-value、`set/get`、`expire`、TTL
  - 完成 `section_02_key_ttl_design.py`
- 完成小节 3：`INCR` 原子计数器
  - 完成 `section_03_incr_counter.py`
- 完成小节 4：Cache Aside 简单缓存接口
  - 完成 `section_04_cache_aside.py`
- 完成小节 5：简单限流接口
  - 完成 `section_05_rate_limit_api.py`
- 完成阶段 5 主体实现
  - `GET /health`
  - `POST /dev/seed`
  - `GET /knowledge-bases/{kb_id}`
  - `PATCH /knowledge-bases/{kb_id}`
  - `POST /counter/{name}/incr`
  - `GET /limited-resource`
- 完成阶段 5 综合课后动手题
  - `lesson_05_document_task_progress.py`
  - 主题：文档入库任务的 Redis 过程进度和 MySQL 权威状态边界

### 新增 / 修改文件

- `playground/05_redis_basic/README.md`
- `playground/05_redis_basic/requirements.txt`
- `playground/05_redis_basic/.gitignore`
- `playground/05_redis_basic/app/__init__.py`
- `playground/05_redis_basic/app/db.py`
- `playground/05_redis_basic/app/models.py`
- `playground/05_redis_basic/app/schemas.py`
- `playground/05_redis_basic/app/repositories.py`
- `playground/05_redis_basic/app/services.py`
- `playground/05_redis_basic/app/redis_client.py`
- `playground/05_redis_basic/app/redis_services.py`
- `playground/05_redis_basic/app/main.py`
- `playground/05_redis_basic/check_stage5.py`
- `playground/05_redis_basic/homework/section_01_redis_mysql_boundary.py`
- `playground/05_redis_basic/homework/section_02_key_ttl_design.py`
- `playground/05_redis_basic/homework/section_03_incr_counter.py`
- `playground/05_redis_basic/homework/section_04_cache_aside.py`
- `playground/05_redis_basic/homework/section_05_rate_limit_api.py`
- `playground/05_redis_basic/homework/lesson_05_document_task_progress.py`
- `docs/LEARNING_LOG.md`
- `docs/STAGE_REPORT.md`

### 关键文件作用

- `app/db.py`：创建 SQLAlchemy engine、SessionLocal、初始化表结构
- `app/models.py`：定义知识库表模型
- `app/schemas.py`：定义健康检查、知识库详情、计数器、限流响应 schema
- `app/repositories.py`：封装 MySQL 查询、更新、演示数据写入
- `app/services.py`：编排 Cache Aside 查询和更新后删除缓存
- `app/redis_client.py`：创建 Redis 客户端
- `app/redis_services.py`：封装 Redis key、缓存读写、计数器、限流
- `app/main.py`：提供 FastAPI 路由入口
- `check_stage5.py`：阶段 5 主体实现一键检查脚本
- `lesson_05_document_task_progress.py`：综合课后题，迁移到文档入库任务进度场景

### 运行命令

```bash
redis-cli ping
```

```bash
cd /home/tkp666/FlowRAG/playground/05_redis_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --reload
```

### 测试命令

```bash
cd /home/tkp666/FlowRAG/playground/05_redis_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage5.py
```

综合课后题完成后运行：

```bash
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/05_redis_basic/homework/lesson_05_document_task_progress.py
```

### 测试结果

- `check_stage5.py` 已通过，输出：
  - `100分：阶段 5 主体实现检查全部通过`
- 真实 Redis 连接在当前沙箱中需要提升权限运行；用户本机直接运行时，先确保 `redis-cli ping` 返回 `PONG`
- `lesson_05_document_task_progress.py` 已通过，输出：
  - `lesson 05 document task progress homework looks good`

### 已知问题

- 当前主体实现使用 SQLite 文件 + SQLAlchemy 做教学实验，没有直接连接真实 MySQL
- 当前没有加入异步数据库读写；正式项目第一版数据库和 Redis 仍建议先用同步实现
- 当前没有学习 Celery，所以文档任务进度作业只模拟状态，不真正投递后台任务
- 当前使用固定窗口限流，未引入滑动窗口、令牌桶、Lua 脚本等复杂限流方案
- Redis 持久化、集群、哨兵暂时不展开

### 用户需要回答的检查问题

用户已完成阶段 5 检查问题，本阶段通过。

复盘时需要记住的关键回答和纠偏：

1. Redis 适合保存限流计数、验证码、上传/入库过程进度等短期状态；MySQL 适合保存知识库、用户、文档等长期权威数据。
2. Cache Aside 第一次查询 Redis miss 后回源 MySQL 并写缓存；第二次命中 Redis；MySQL 更新后删除对应 Redis 缓存。
3. 限流应使用 Redis `INCR`，因为它是原子计数操作；还要在 `count == 1` 时设置 TTL，避免每次请求刷新窗口。
4. 文档入库过程进度放 Redis，最终状态和失败原因放 MySQL，因为后两者需要长期追溯并作为权威事实。
5. Redis 进度丢失但 MySQL 仍是 `running` 时，接口应返回进度暂时缺失或 `missing`，不能直接误判任务失败。

### 下一阶段建议

- 用户明确同意后，进入阶段 6：Celery 异步任务
- 阶段 6 应继续保持预备营小实验，不直接开发完整 FlowRAG 主项目
- 阶段 6 重点讲清同步请求、后台任务、Redis broker、任务状态查询之间的边界

## 2026-05-12 - 阶段 6：Celery 异步任务

### 阶段目标

- 理解 Celery 的任务边界和角色模型
- 使用真实 Redis 作为 Celery broker 和 result backend
- 完成 FastAPI 投递后台任务并用 `task_id` 查询状态的最小实验
- 保持阶段 2 的 `router / schema / service / repository` 分层思路，不把 Celery 讲成新的业务层

### 完成内容

- 创建阶段 6 最小 Celery 实验目录
- 完成 `GET /health`
- 完成 `POST /tasks`：提交后台加法任务，立即返回 `task_id`
- 完成 `GET /tasks/{task_id}`：查询 Celery 任务状态、成功结果或失败原因
- 完成成功任务和失败任务两个分支
- 完成不依赖 Redis 的轻量检查脚本
- 使用真实 Redis、Celery worker 和 FastAPI 跑通成功 / 失败任务链路

### 新增 / 修改文件

- `playground/06_celery_basic/README.md`
- `playground/06_celery_basic/requirements.txt`
- `playground/06_celery_basic/.gitignore`
- `playground/06_celery_basic/app/__init__.py`
- `playground/06_celery_basic/app/main.py`
- `playground/06_celery_basic/app/celery_app.py`
- `playground/06_celery_basic/app/schemas.py`
- `playground/06_celery_basic/app/tasks.py`
- `playground/06_celery_basic/app/api/__init__.py`
- `playground/06_celery_basic/app/api/task_router.py`
- `playground/06_celery_basic/app/services/__init__.py`
- `playground/06_celery_basic/app/services/task_service.py`
- `playground/06_celery_basic/check_stage6.py`
- `playground/06_celery_basic/homework/lesson_06_document_ingest_design.py`
- `docs/LEARNING_LOG.md`
- `docs/STAGE_REPORT.md`

### 关键文件作用

- `app/celery_app.py`：创建 Celery app，配置 Redis broker、Redis result backend、任务模块导入和状态记录
- `app/tasks.py`：注册 worker 能执行的 Celery task，保持薄入口并调用 service 中的业务函数
- `app/services/task_service.py`：封装任务投递、状态查询和模拟耗时业务
- `app/api/task_router.py`：提供任务 HTTP 入口，只负责接收请求并调用 service
- `app/schemas.py`：定义健康检查、任务创建和任务状态响应结构
- `check_stage6.py`：不启动 Redis / worker 的轻量检查脚本
- `homework/lesson_06_document_ingest_design.py`：综合课后题参考答案，把 Celery 最小实验迁移到文档入库任务设计

### 运行命令

```bash
redis-cli ping
```

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/celery -A app.celery_app:celery_app worker --loglevel=info --pool=solo
```

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8006
```

### 测试命令

```bash
cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage6.py
/home/tkp666/miniconda3/envs/flowrag/bin/python homework/lesson_06_document_ingest_design.py
```

```bash
curl http://127.0.0.1:8006/health
curl -s -X POST http://127.0.0.1:8006/tasks -H 'Content-Type: application/json' -d '{"a":1,"b":2,"fail":false}'
curl -s http://127.0.0.1:8006/tasks/<task_id>
curl -s -X POST http://127.0.0.1:8006/tasks -H 'Content-Type: application/json' -d '{"a":1,"b":2,"fail":true}'
curl -s http://127.0.0.1:8006/tasks/<failed_task_id>
```

### 测试结果

- `check_stage6.py` 通过，输出：
  - `100分：阶段 6 主体实现轻量检查通过`
- `lesson_06_document_ingest_design.py` 通过，输出：
  - `lesson 06 document ingest design looks good`
- `redis-cli ping` 返回：
  - `PONG`
- `GET /health` 返回：
  - `{"status":"ok"}`
- 成功任务提交后立即返回 `task_id` 和 `queued`
- 成功任务最终查询返回：
  - `celery_state` 为 `SUCCESS`
  - `result` 为 `3`
- 失败任务最终查询返回：
  - `celery_state` 为 `FAILURE`
  - `error` 为 `simulated task failure`

### 已知问题

- 本阶段只用 Celery result backend 查询任务状态；正式 FlowRAG 应把最终任务状态、失败原因和文档状态写入 MySQL
- 当前任务只是 `slow_add` 教学任务，真实文档解析、切块、embedding、Qdrant 写入还未开始
- 当前没有展开 Celery retry、timeout、幂等、任务取消、队列拆分和监控
- 当前使用 `--pool=solo` 方便教学观察，不代表生产环境默认配置

### 用户需要回答的检查问题

本阶段已切换为模式 D，检查问题可以由 Codex 给参考答案，用户主要负责指出不懂或不同意的地方。

1. `.delay(...)` 和直接调用函数有什么区别？
2. broker、worker、result backend 分别负责什么？
3. 为什么不推荐把上传文件的完整字节流直接传给 Celery？
4. Celery 接入后，为什么仍然要坚持 router 调 service，而不是把 `.delay(...)` 到处写在 router 里？
5. `PENDING` 为什么不能直接等同于“任务正在排队”？

### 下一阶段建议

- 阶段 6 已完成主体实现、代码复盘和综合课后题参考答案
- 用户确认阶段 6 检查问题没有疑问后，才能进入阶段 7：Qdrant 基础

## 2026-06-04 - 阶段 7：Qdrant 最小向量检索

### 阶段目标

- 理解 embedding 向量、Qdrant collection、point、payload、top-k search 和 metadata filter
- 使用 `qdrant-client` 的本地嵌入式模式跑通最小向量检索实验
- 写入模拟 chunk 数据，每个 chunk 包含 `text / document_id / kb_id / chunk_index`
- 支持 top-k 检索和按 `kb_id` 限制检索范围
- 讲清 MySQL 和 Qdrant 在 FlowRAG 中的职责边界

### 完成内容

- 创建阶段 7 最小 Qdrant 实验目录
- 完成 mock embedding，把文本稳定转换成 6 维向量
- 完成 Qdrant collection 创建和重置
- 完成 6 条模拟 chunk point 写入
- 完成 `POST /search` top-k 检索
- 完成 `kb_id` filter 检索
- 完成不启动 FastAPI 的轻量检查脚本
- 完成综合课后题参考答案，覆盖 MySQL / Qdrant / retrieval service 的职责分工
- 使用真实 HTTP 请求跑通阶段 7 API
- 完成阶段 7 补充概念讲解、代码导读、运行命令导读和检查问题确认

### 新增 / 修改文件

- `playground/07_qdrant_basic/README.md`
- `playground/07_qdrant_basic/requirements.txt`
- `playground/07_qdrant_basic/.gitignore`
- `playground/07_qdrant_basic/app/__init__.py`
- `playground/07_qdrant_basic/app/main.py`
- `playground/07_qdrant_basic/app/mock_embedding.py`
- `playground/07_qdrant_basic/app/qdrant_client.py`
- `playground/07_qdrant_basic/app/schemas.py`
- `playground/07_qdrant_basic/check_stage7.py`
- `playground/07_qdrant_basic/homework/lesson_07_retrieval_boundary.py`
- `docs/LEARNING_LOG.md`
- `docs/STAGE_REPORT.md`

### 关键文件作用

- `app/mock_embedding.py`：教学用 mock embedding，把文本转成固定 6 维向量
- `app/qdrant_client.py`：封装 Qdrant client、collection 创建、upsert 和 top-k 查询
- `app/schemas.py`：定义健康检查、seed、search 请求与响应结构
- `app/main.py`：提供 `GET /health`、`POST /dev/reset`、`POST /search`
- `check_stage7.py`：轻量检查脚本，验证路由、embedding、schema、Qdrant 写入与查询
- `homework/lesson_07_retrieval_boundary.py`：综合课后题参考答案，训练 MySQL / Qdrant / service 职责判断

### 运行命令

```bash
cd /home/tkp666/FlowRAG/playground/07_qdrant_basic
/home/tkp666/miniconda3/envs/flowrag/bin/pip install -r requirements.txt
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8007 --reload
```

### 测试命令

```bash
cd /home/tkp666/FlowRAG/playground/07_qdrant_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage7.py
/home/tkp666/miniconda3/envs/flowrag/bin/python homework/lesson_07_retrieval_boundary.py
```

```bash
curl http://127.0.0.1:8007/health
curl -X POST http://127.0.0.1:8007/dev/reset
curl -s -X POST http://127.0.0.1:8007/search -H 'Content-Type: application/json' -d '{"query":"qdrant vector search payload","top_k":3}'
curl -s -X POST http://127.0.0.1:8007/search -H 'Content-Type: application/json' -d '{"query":"qdrant vector search payload","top_k":3,"kb_id":2}'
```

### 测试结果

- `check_stage7.py` 通过，输出：
  - `100分：阶段 7 主体实现轻量检查通过`
- `lesson_07_retrieval_boundary.py` 通过，输出：
  - `lesson 07 retrieval boundary looks good`
- `GET /health` 返回：
  - `{"status":"ok"}`
- `POST /dev/reset` 返回：
  - `{"collection_name":"flowrag_stage7_chunks","vector_size":6,"inserted_count":6}`
- 不带 `kb_id` 的 Qdrant 查询返回 top-k hits，其中最高分结果是 Qdrant 相关 chunk
- 带 `kb_id=2` 的查询只返回 2 号知识库中的 chunks，说明 metadata filter 生效

### 已知问题

- 本阶段使用 mock embedding，不具备真实语义理解能力
- 本阶段默认使用 qdrant-client 本地嵌入式模式，不要求启动独立 Qdrant 服务
- top-k 可能返回低分但仍在指定知识库内的结果，真实 FlowRAG 后续需要补 `score_threshold`、rerank 或更强 embedding
- 本阶段没有做文档上传、Celery 入库、真实 chunk 切分、真实 embedding 批处理

### 用户需要回答的检查问题

本阶段采用模式 D，下面先给参考答案；用户只需要指出哪里不懂或不同意。

用户已在 2026-06-10 确认阶段 7 检查问题没有不清楚的地方，本阶段通过。

1. Qdrant 里的 point、vector、payload 分别是什么？
   - point 是一条向量记录；vector 是用于相似度计算的数值向量；payload 是检索后回溯业务信息用的附加字段。
2. 为什么检索时要带 `kb_id` filter？
   - 因为同一个 Qdrant collection 里可能有多个知识库的 chunks，不加 filter 会跨知识库返回内容。
3. 为什么不能只用 MySQL 做语义检索？
   - MySQL 适合结构化查询和权威业务数据，不擅长根据语义相似度找文本；语义 top-k 更适合向量数据库。
4. `document_id` 和 `chunk_index` 对引用回溯有什么用？
   - 它们让系统知道答案引用来自哪篇文档、文档里的第几个 chunk，后续可展示出处或回查 MySQL 文档元数据。
5. 真实项目中 mock embedding 会替换成什么？
   - 会替换成 `EmbeddingProvider`，它封装真实 embedding 模型或第三方 embedding API。

### 下一阶段建议

- 用户明确同意后，可以进入阶段 8：流式接口
- 阶段 8 重点学习普通 JSON 响应和流式响应的区别、FastAPI `StreamingResponse` 最小实现，以及 FlowRAG 问答时如何边生成边返回

## 2026-06-11 - 阶段 8：Streaming 流式接口

### 阶段目标

- 理解普通 JSON 响应和流式响应的区别
- 理解 FastAPI `StreamingResponse`、生成器、异步生成器和 SSE 的最小用法
- 完成 FlowRAG 风格的最小流式问答实验
- 讲清检索、引用返回、LLM token 流式生成、错误事件和 Celery 边界

### 完成内容

- 完成阶段 8 概念块 A：普通响应 vs 流式响应、`yield`、HTTP 一个连接多次返回、超时和心跳边界
- 完成阶段 8 概念块 B：FastAPI `StreamingResponse`、`text/plain` 流、SSE 流和客户端消费
- 完成阶段 8 概念块 C：FlowRAG 流式问答边界、引用返回、检索先于生成、Celery / SSE / WebSocket 选型
- 完成 3 个小节动手题参考实现
- 完成阶段 8 主体实现，并把主体实现独立放入 `subject_impl/`
- 完成主体实现拆分：概念块演示入口保留在根目录 `main.py`，主体实现入口移动到 `subject_impl/main.py`
- 完成综合课后动手题参考实现

### 新增 / 修改文件

- `playground/08_streaming_basic/README.md`
- `playground/08_streaming_basic/requirements.txt`
- `playground/08_streaming_basic/main.py`
- `playground/08_streaming_basic/check_stage8.py`
- `playground/08_streaming_basic/subject_impl/__init__.py`
- `playground/08_streaming_basic/subject_impl/main.py`
- `playground/08_streaming_basic/subject_impl/schemas.py`
- `playground/08_streaming_basic/subject_impl/sse.py`
- `playground/08_streaming_basic/subject_impl/mock_rag.py`
- `playground/08_streaming_basic/subject_impl/check_subject.py`
- `playground/08_streaming_basic/homework/section_01_streaming_boundary.py`
- `playground/08_streaming_basic/homework/section_02_streaming_response_mechanics.py`
- `playground/08_streaming_basic/homework/section_03_flowrag_streaming_boundary.py`
- `playground/08_streaming_basic/homework/lesson_08_streaming_review.py`
- `docs/LEARNING_LOG.md`
- `docs/STAGE_REPORT.md`

### 关键文件作用

- `main.py`：阶段 8 概念块 B 的对照演示入口，包含普通响应、普通文本流和最小 SSE 流
- `check_stage8.py`：检查概念块 B 的演示接口和生成器行为
- `subject_impl/main.py`：阶段 8 主体实现入口，提供独立的 `POST /chat/stream`
- `subject_impl/schemas.py`：定义 `ChatStreamRequest`
- `subject_impl/sse.py`：封装 SSE 事件创建和检查脚本使用的解析逻辑
- `subject_impl/mock_rag.py`：模拟 FlowRAG 检索、引用返回、LLM token 流式生成和中途错误事件
- `subject_impl/check_subject.py`：检查主体实现路由、返回类型、事件顺序和错误分支
- `homework/lesson_08_streaming_review.py`：综合课后题参考实现，复盘 JSON / SSE / Celery / WebSocket 选型和流式错误边界

### 运行命令

```bash
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8008 --reload
```

```bash
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn subject_impl.main:app --host 127.0.0.1 --port 8009 --reload
```

### 测试命令

```bash
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage8.py
/home/tkp666/miniconda3/envs/flowrag/bin/python -m subject_impl.check_subject
/home/tkp666/miniconda3/envs/flowrag/bin/python homework/lesson_08_streaming_review.py
```

```bash
curl http://127.0.0.1:8008/health
curl http://127.0.0.1:8008/normal-answer
curl -N http://127.0.0.1:8008/stream-answer
curl -N http://127.0.0.1:8008/sse-answer
curl -N -X POST http://127.0.0.1:8009/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question":"FlowRAG 为什么要用流式问答？","kb_id":"kb-stage8"}'
```

### 测试结果

- `check_stage8.py` 通过，输出：
  - `阶段 8 概念块 B 检查通过：streaming response demo looks good`
- `subject_impl.check_subject` 通过，输出：
  - `阶段 8 主体实现检查通过：chat stream endpoint looks good`
- `lesson_08_streaming_review.py` 通过，输出：
  - `阶段 8 综合课后动手题通过：streaming review looks good`
- `/chat/stream` 正常事件顺序为：
  - `status -> references -> status -> token -> token -> token -> token -> done`
- 模拟检索失败时事件顺序为：
  - `status -> error`
- 模拟 LLM 中途失败时事件顺序为：
  - `status -> references -> status -> token -> token -> error`

### 已知问题

- 本阶段没有接真实 LLM 流式 API，使用 `MOCK_TOKENS` 模拟 token 生成
- 本阶段没有接真实 Qdrant 检索，使用 `MOCK_REFERENCES` 模拟引用结果
- 本阶段没有实现代理层心跳、断线重连、客户端取消和生产环境超时配置
- 本阶段没有把对话记录和引用记录写入 MySQL，正式主项目再做持久化

### 用户需要回答的检查问题

本阶段采用模式 D，下面先给参考答案；用户只需要指出哪里不懂或不同意。

1. 普通 JSON 响应和流式响应最大的区别是什么？
   - 普通 JSON 要等完整结果生成后一次性返回；流式响应可以在同一个 HTTP 连接里分多次返回，让客户端更早看到状态、引用和 token。
2. `StreamingResponse` 自己会生成内容吗？
   - 不会。它只是消费传入的可迭代对象或生成器；真正一段段产生内容的是生成器里的 `yield`。
3. 为什么 `/chat/stream` 里空问题和知识库不存在要在 `StreamingResponse` 前校验？
   - 因为这类错误属于请求开始前就能判断的不合法请求，可以直接返回 HTTP 400 / 404；一旦流式响应开始，通常就不能再随便改 HTTP 状态码。
4. 检索失败和 LLM 中途失败为什么要变成 SSE `error` 事件？
   - 因为此时流可能已经开始，客户端已经收到部分事件。后端不能收回已经发出的内容，只能继续在流里发送结构化错误事件，让前端停止等待并展示失败状态。
5. FlowRAG 为什么通常先检索再流式生成？
   - RAG 的回答需要基于检索出的上下文和引用。先检索可以保证 LLM 生成时有依据，也能先把 references 发给前端。
6. SSE、Celery、WebSocket 在 FlowRAG 里分别适合什么？
   - SSE 适合聊天答案从服务端单向流式返回；Celery 适合文档解析、切块、embedding、入库这类后台长任务；WebSocket 适合需要双向实时通信的场景。

### 下一阶段建议

- 预备营阶段 1-8 已完成
- 用户已确认阶段 8 检查问题没有疑问，可以开始讨论正式 FlowRAG 主项目第一版落地路线
- 正式主项目建议先做模块化单体，不要直接上微服务；优先落地知识库、文档、任务、检索和流式问答的最小闭环
