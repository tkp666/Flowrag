"""
阶段 8：流式接口
概念块 C 动手题参考实现：FlowRAG 流式问答边界

本文件是 Codex 主讲主写模式下的参考答案。

练习目标：
1. 模拟 FlowRAG 的 RAG 问答流：retrieving -> references -> generating -> token -> done。
2. 区分“流开始前错误”和“流开始后错误”。
3. 演示 references 为什么应作为独立 SSE 事件返回。
4. 演示 StreamingResponse 只负责发送，业务事件顺序由生成器决定。

运行方式：
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python homework/section_03_flowrag_streaming_boundary.py
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import HTTPException
from fastapi.responses import StreamingResponse


VALID_KB_ID = "kb-stage8"

REFERENCES = [
    {
        "doc_id": "doc-001",
        "chunk_id": "chunk-001",
        "score": 0.86,
        "text": "文档上传后，解析、切块、embedding 和入库适合交给 Celery 后台任务。",
    },
    {
        "doc_id": "doc-002",
        "chunk_id": "chunk-017",
        "score": 0.79,
        "text": "聊天接口等待 Qdrant 和 LLM API 时可以使用 async，LLM token 适合用 SSE 流式返回。",
    },
]

ANSWER_TOKENS = ["FlowRAG", " 会先检索引用，", "再把 LLM token", " 通过 SSE 返回。"]


def make_sse_event(event: str, data: Any) -> str:
    """把事件名和数据转换成 SSE 文本格式。"""
    if isinstance(data, str):
        payload = data
    else:
        payload = json.dumps(data, ensure_ascii=False)

    return f"event: {event}\ndata: {payload}\n\n"


def parse_sse_event(chunk: str) -> dict[str, Any]:
    """把本练习生成的简单 SSE 字符串解析回结构，方便检查事件顺序。"""
    lines = chunk.rstrip("\n").split("\n")
    event = lines[0].removeprefix("event: ")
    raw_data = lines[1].removeprefix("data: ")

    try:
        data: Any = json.loads(raw_data)
    except json.JSONDecodeError:
        data = raw_data

    return {"event": event, "data": data}


def validate_chat_request(question: str, kb_id: str) -> None:
    """流开始前的校验：这里仍然可以返回真正的 HTTP 4xx。"""
    if not question.strip():
        raise HTTPException(status_code=400, detail="question must not be empty")

    if kb_id != VALID_KB_ID:
        raise HTTPException(status_code=404, detail="knowledge base not found")


async def retrieve_references(question: str) -> list[dict[str, Any]]:
    """模拟 Qdrant top-k 检索。真实项目里这里会调用 RetrievalService。"""
    await asyncio.sleep(0)
    return REFERENCES


async def stream_llm_tokens(
    question: str,
    references: list[dict[str, Any]],
    *,
    fail_after_tokens: int | None = None,
) -> AsyncGenerator[str, None]:
    """模拟 LLMProvider 的 streaming API。"""
    for index, token in enumerate(ANSWER_TOKENS):
        await asyncio.sleep(0)

        if fail_after_tokens is not None and index >= fail_after_tokens:
            raise RuntimeError("llm provider timeout")

        yield token


async def rag_chat_stream(
    question: str,
    kb_id: str,
    *,
    simulate_retrieval_error: bool = False,
    simulate_llm_error: bool = False,
) -> AsyncGenerator[str, None]:
    """模拟 FlowRAG 的流式问答事件顺序。

    注意：这个函数假设前置参数校验已经完成。
    一旦这里 yield 了第一条事件，HTTP 响应通常就已经开始，
    后续错误应该转换成 SSE error 事件，而不是再抛 HTTPException。
    """
    yield make_sse_event("status", {"stage": "retrieving"})

    try:
        if simulate_retrieval_error:
            raise RuntimeError("qdrant search timeout")

        references = await retrieve_references(question)
        yield make_sse_event("references", references)
        yield make_sse_event("status", {"stage": "generating"})

        fail_after_tokens = 2 if simulate_llm_error else None
        async for token in stream_llm_tokens(
            question,
            references,
            fail_after_tokens=fail_after_tokens,
        ):
            yield make_sse_event("token", token)

        yield make_sse_event("done", {"finish_reason": "stop"})
    except Exception as exc:
        yield make_sse_event("error", {"message": str(exc)})


def create_chat_stream_response(
    question: str,
    kb_id: str,
    *,
    simulate_retrieval_error: bool = False,
    simulate_llm_error: bool = False,
) -> StreamingResponse:
    """真实接口里 router/service 可以先校验，再创建 StreamingResponse。"""
    validate_chat_request(question, kb_id)

    return StreamingResponse(
        rag_chat_stream(
            question,
            kb_id,
            simulate_retrieval_error=simulate_retrieval_error,
            simulate_llm_error=simulate_llm_error,
        ),
        media_type="text/event-stream",
    )


async def collect_stream_events(
    question: str,
    kb_id: str,
    *,
    simulate_retrieval_error: bool = False,
    simulate_llm_error: bool = False,
) -> list[dict[str, Any]]:
    """测试用消费者：不走 HTTP，也能检查生成器产出的事件。"""
    events: list[dict[str, Any]] = []

    async for chunk in rag_chat_stream(
        question,
        kb_id,
        simulate_retrieval_error=simulate_retrieval_error,
        simulate_llm_error=simulate_llm_error,
    ):
        assert chunk.endswith("\n\n")
        events.append(parse_sse_event(chunk))

    return events


async def run_checks() -> None:
    response = create_chat_stream_response("为什么文档入库要用 Celery？", VALID_KB_ID)
    assert isinstance(response, StreamingResponse)
    assert response.media_type == "text/event-stream"

    try:
        create_chat_stream_response("   ", VALID_KB_ID)
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("empty question should fail before stream starts")

    try:
        create_chat_stream_response("hello", "missing-kb")
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("missing kb should fail before stream starts")

    normal_events = await collect_stream_events("为什么文档入库要用 Celery？", VALID_KB_ID)
    normal_names = [event["event"] for event in normal_events]
    assert normal_names == [
        "status",
        "references",
        "status",
        "token",
        "token",
        "token",
        "token",
        "done",
    ]
    assert normal_events[0]["data"] == {"stage": "retrieving"}
    assert normal_events[1]["data"][0]["chunk_id"] == "chunk-001"
    assert normal_events[2]["data"] == {"stage": "generating"}
    assert normal_events[-1]["data"] == {"finish_reason": "stop"}

    answer = "".join(
        event["data"] for event in normal_events if event["event"] == "token"
    )
    assert "LLM token" in answer
    assert "SSE" in answer

    retrieval_error_events = await collect_stream_events(
        "为什么文档入库要用 Celery？",
        VALID_KB_ID,
        simulate_retrieval_error=True,
    )
    assert [event["event"] for event in retrieval_error_events] == ["status", "error"]
    assert "qdrant" in retrieval_error_events[-1]["data"]["message"]

    llm_error_events = await collect_stream_events(
        "为什么文档入库要用 Celery？",
        VALID_KB_ID,
        simulate_llm_error=True,
    )
    llm_error_names = [event["event"] for event in llm_error_events]
    assert llm_error_names == [
        "status",
        "references",
        "status",
        "token",
        "token",
        "error",
    ]
    assert "llm provider timeout" in llm_error_events[-1]["data"]["message"]

    print("阶段 8 概念块 C 动手题通过：flowrag streaming boundary looks good")


if __name__ == "__main__":
    asyncio.run(run_checks())
