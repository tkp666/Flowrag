import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI(title="FlowRAG Stage 8 Streaming Demo")

TOKENS = ["FlowRAG", " 可以", " 流式", " 返回", " 答案。"]


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/normal-answer")
async def normal_answer() -> dict[str, str]:
    answer = ""

    for token in TOKENS:
        await asyncio.sleep(0.5)
        answer += token

    return {"answer": answer}


async def plain_token_stream():
    for token in TOKENS:
        await asyncio.sleep(0.5)
        yield token


@app.get("/stream-answer")
async def stream_answer() -> StreamingResponse:
    return StreamingResponse(
        plain_token_stream(),
        media_type="text/plain; charset=utf-8",
    )


async def sse_token_stream():
    yield 'event: status\ndata: {"stage":"generating"}\n\n'

    for token in TOKENS:
        await asyncio.sleep(0.5)
        yield f"event: token\ndata: {token}\n\n"

    yield "event: done\ndata: {}\n\n"


@app.get("/sse-answer")
async def sse_answer() -> StreamingResponse:
    return StreamingResponse(
        sse_token_stream(),
        media_type="text/event-stream",
    )
