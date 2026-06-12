# 阶段 8：流式接口

本目录用于学习 FastAPI `StreamingResponse`、SSE 事件格式，以及 FlowRAG
流式问答的最小接口边界。

## 概念块演示接口

- `GET /health`：健康检查。
- `GET /normal-answer`：普通 JSON 响应，等待所有 token 拼完后一次性返回。
- `GET /stream-answer`：普通文本流式响应，每隔一小段时间返回一个 token。
- `GET /sse-answer`：SSE 流式响应，按 `event/data` 格式返回状态、token 和结束事件。

## 主体实现接口

- `POST /chat/stream`：模拟 FlowRAG 流式问答，按 `status -> references -> status -> token -> done/error` 返回。

主体实现代码集中在 `subject_impl/` 目录，入口是 `subject_impl/main.py`。

## 运行概念块演示

```bash
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8008 --reload
```

## 运行主体实现

```bash
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python -m uvicorn subject_impl.main:app --host 127.0.0.1 --port 8009 --reload
```

## 测试概念块演示

普通响应：

```bash
curl http://127.0.0.1:8008/normal-answer
```

文本流式响应：

```bash
curl -N http://127.0.0.1:8008/stream-answer
```

SSE 流式响应：

```bash
curl -N http://127.0.0.1:8008/sse-answer
```

## 测试主体实现

FlowRAG 流式问答：

```bash
curl -N -X POST http://127.0.0.1:8009/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question":"FlowRAG 为什么要用流式问答？","kb_id":"kb-stage8"}'
```

模拟检索阶段错误：

```bash
curl -N -X POST http://127.0.0.1:8009/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question":"FlowRAG 为什么要用流式问答？","kb_id":"kb-stage8","simulate_retrieval_error":true}'
```

模拟 LLM 生成阶段错误：

```bash
curl -N -X POST http://127.0.0.1:8009/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"question":"FlowRAG 为什么要用流式问答？","kb_id":"kb-stage8","simulate_llm_error":true}'
```

轻量检查：

```bash
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage8.py
/home/tkp666/miniconda3/envs/flowrag/bin/python -m subject_impl.check_subject
```
