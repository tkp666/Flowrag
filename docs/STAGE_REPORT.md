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
- 预备营阶段规划已更新：在原阶段 2 后新增“阶段 3：FastAPI 异步入门”，后续 MySQL / Redis / Celery / Qdrant / Streaming 阶段顺延。
- 阶段 3 补充专题“并发选型与线程/进程最小模板”已完成；下一步应等待用户明确同意后进入阶段 4：MySQL + SQLAlchemy 基础。
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
