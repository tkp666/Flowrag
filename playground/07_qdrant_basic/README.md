# Stage 7: Qdrant Basic

本阶段是 Qdrant 最小向量检索实验。

核心目标：

- 用 mock embedding 把文本转换成固定维度向量
- 创建 Qdrant collection
- 写入模拟 chunk points
- 执行 top-k 向量检索
- 使用 `kb_id` filter 限制检索范围
- 理解 MySQL 和 Qdrant 在 FlowRAG 中的职责边界

## 文件职责

```text
app/main.py
  创建 FastAPI app，提供健康检查、重置数据、检索接口。

app/mock_embedding.py
  教学用 mock embedding，把文本稳定转换成 6 维向量。

app/qdrant_client.py
  封装 Qdrant client、collection 创建、chunk 写入和 top-k 查询。

app/schemas.py
  定义请求体和响应体。

check_stage7.py
  不启动 FastAPI 的轻量检查脚本。

homework/lesson_07_retrieval_boundary.py
  综合课后题参考答案：判断 MySQL / Qdrant / service 的职责分工。
```

## 为什么本阶段用 mock embedding

真实 FlowRAG 会调用 `EmbeddingProvider`，把 chunk 文本转换成语义向量。

本阶段先不用真实 embedding 模型，原因是：

- 当前目标是学 Qdrant 的基本数据模型，不是学模型 API；
- mock embedding 可以稳定复现结果，方便检查；
- 等 Qdrant 查询链路跑通后，再替换为真实 embedding provider。

## 安装依赖

```bash
cd /home/tkp666/FlowRAG/playground/07_qdrant_basic
/home/tkp666/miniconda3/envs/flowrag/bin/pip install -r requirements.txt
```

## 轻量检查

```bash
cd /home/tkp666/FlowRAG/playground/07_qdrant_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage7.py
```

通过时输出：

```text
100分：阶段 7 主体实现轻量检查通过
```

## 启动 API

```bash
cd /home/tkp666/FlowRAG/playground/07_qdrant_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8007 --reload
```

## 测试接口

健康检查：

```bash
curl http://127.0.0.1:8007/health
```

重置并写入演示 chunks：

```bash
curl -X POST http://127.0.0.1:8007/dev/reset
```

检索 Qdrant 相关内容：

```bash
curl -s -X POST http://127.0.0.1:8007/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"qdrant vector search payload","top_k":3}'
```

只在 `kb_id=1` 的知识库里检索：

```bash
curl -s -X POST http://127.0.0.1:8007/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"qdrant vector search payload","top_k":3,"kb_id":1}'
```

只在 `kb_id=2` 的知识库里检索：

```bash
curl -s -X POST http://127.0.0.1:8007/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"qdrant vector search payload","top_k":3,"kb_id":2}'
```

## 本阶段必须理解

- `collection` 类似 Qdrant 里的向量集合，要求向量维度一致；
- `point` 是 Qdrant 里的一条向量记录，通常包含 `id`、`vector`、`payload`；
- `payload` 保存检索后需要回溯的业务信息，例如 `text`、`document_id`、`kb_id`、`chunk_index`；
- `top-k` 是返回最相似的前 k 条结果，不是返回全部；
- `kb_id filter` 用来避免跨知识库检索到别人的内容；
- MySQL 保存权威业务数据，Qdrant 保存 chunk 向量和检索必要 payload。

