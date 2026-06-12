from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from subject_impl.mock_rag import chat_event_stream, validate_chat_stream_request
from subject_impl.schemas import ChatStreamRequest


app = FastAPI(title="FlowRAG Stage 8 Subject Streaming Demo")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "app": "stage8-subject"}


@app.post("/chat/stream")
async def chat_stream(request: ChatStreamRequest) -> StreamingResponse:
    validate_chat_stream_request(request)

    return StreamingResponse(
        chat_event_stream(request),
        media_type="text/event-stream",
    )
