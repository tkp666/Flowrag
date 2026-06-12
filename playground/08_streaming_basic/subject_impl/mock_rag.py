from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import HTTPException

from subject_impl.schemas import ChatStreamRequest
from subject_impl.sse import make_sse_event


VALID_KB_IDS = {"kb-stage8"}

MOCK_REFERENCES = [
    {
        "doc_id": "doc-celery-001",
        "chunk_id": "chunk-001",
        "score": 0.87,
        "text": "文档上传后，解析、切块、embedding 和写入 Qdrant 适合交给 Celery。",
    },
    {
        "doc_id": "doc-streaming-002",
        "chunk_id": "chunk-014",
        "score": 0.81,
        "text": "聊天接口可以先完成检索，再通过 SSE 持续返回 LLM token。",
    },
]

MOCK_TOKENS = ["FlowRAG", " 会先检索引用，", "再把答案 token", " 流式返回。"]


def validate_chat_stream_request(request: ChatStreamRequest) -> None:
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="question must not be empty")

    if request.kb_id not in VALID_KB_IDS:
        raise HTTPException(status_code=404, detail="knowledge base not found")


async def retrieve_references(request: ChatStreamRequest) -> list[dict[str, Any]]:
    await asyncio.sleep(0)

    if request.simulate_retrieval_error:
        raise RuntimeError("qdrant search timeout")

    return MOCK_REFERENCES


async def stream_llm_tokens(
    request: ChatStreamRequest,
    references: list[dict[str, Any]],
) -> AsyncGenerator[str, None]:
    for index, token in enumerate(MOCK_TOKENS):
        await asyncio.sleep(0)

        if request.simulate_llm_error and index >= 2:
            raise RuntimeError("llm provider timeout")

        yield token


async def chat_event_stream(
    request: ChatStreamRequest,
) -> AsyncGenerator[str, None]:
    yield make_sse_event("status", {"stage": "retrieving"})

    try:
        references = await retrieve_references(request)
        yield make_sse_event("references", references)
        yield make_sse_event("status", {"stage": "generating"})

        async for token in stream_llm_tokens(request, references):
            yield make_sse_event("token", token)

        yield make_sse_event("done", {"finish_reason": "stop"})
    except Exception as exc:
        yield make_sse_event("error", {"message": str(exc)})
