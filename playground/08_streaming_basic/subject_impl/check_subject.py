from __future__ import annotations

import asyncio

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from subject_impl.main import app, chat_stream
from subject_impl.mock_rag import chat_event_stream
from subject_impl.schemas import ChatStreamRequest
from subject_impl.sse import parse_sse_event


async def collect_events(request: ChatStreamRequest) -> list[dict]:
    events: list[dict] = []

    async for chunk in chat_event_stream(request):
        assert chunk.endswith("\n\n")
        events.append(parse_sse_event(chunk))

    return events


async def run_checks() -> None:
    route_paths = {route.path for route in app.routes}
    assert "/chat/stream" in route_paths

    response = await chat_stream(
        ChatStreamRequest(question="FlowRAG 为什么要用流式问答？")
    )
    assert isinstance(response, StreamingResponse)
    assert response.media_type == "text/event-stream"

    try:
        await chat_stream(ChatStreamRequest(question="   "))
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("empty question should fail before stream starts")

    try:
        await chat_stream(
            ChatStreamRequest(question="hello", kb_id="missing-kb")
        )
    except HTTPException as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("missing kb should fail before stream starts")

    normal_events = await collect_events(
        ChatStreamRequest(question="FlowRAG 为什么要用流式问答？")
    )
    assert [event["event"] for event in normal_events] == [
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

    retrieval_error_events = await collect_events(
        ChatStreamRequest(
            question="FlowRAG 为什么要用流式问答？",
            simulate_retrieval_error=True,
        )
    )
    assert [event["event"] for event in retrieval_error_events] == [
        "status",
        "error",
    ]
    assert "qdrant" in retrieval_error_events[-1]["data"]["message"]

    llm_error_events = await collect_events(
        ChatStreamRequest(
            question="FlowRAG 为什么要用流式问答？",
            simulate_llm_error=True,
        )
    )
    assert [event["event"] for event in llm_error_events] == [
        "status",
        "references",
        "status",
        "token",
        "token",
        "error",
    ]
    assert "llm provider timeout" in llm_error_events[-1]["data"]["message"]

    print("阶段 8 主体实现检查通过：chat stream endpoint looks good")


if __name__ == "__main__":
    asyncio.run(run_checks())
