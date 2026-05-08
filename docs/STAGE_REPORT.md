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
- 当前尚未进入阶段 6；需要用户明确同意后，才能开始阶段 6：Celery 异步任务。
- 用户已明确反馈：此前综合动手题和口头问题同质化严重。后续出题必须减少重复模板，改为考察边界判断、错误识别、设计取舍、FlowRAG 真实业务迁移；不要把刚写过的代码换名后再次布置。

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
