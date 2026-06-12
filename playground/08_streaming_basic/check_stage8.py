import asyncio

from fastapi.responses import StreamingResponse

from main import (
    TOKENS,
    app,
    health,
    normal_answer,
    plain_token_stream,
    sse_answer,
    sse_token_stream,
    stream_answer,
)


async def collect_async_chunks(generator) -> list[str]:
    chunks: list[str] = []
    async for chunk in generator:
        chunks.append(chunk)
    return chunks


async def run_checks() -> None:
    route_paths = {route.path for route in app.routes}
    expected_paths = {
        "/health",
        "/normal-answer",
        "/stream-answer",
        "/sse-answer",
    }
    missing_paths = expected_paths - route_paths
    assert not missing_paths, f"缺少路由：{missing_paths}"

    health_response = await health()
    assert health_response == {"status": "ok"}

    normal_response = await normal_answer()
    assert normal_response == {"answer": "".join(TOKENS)}

    plain_chunks = await collect_async_chunks(plain_token_stream())
    assert plain_chunks == TOKENS

    plain_response = await stream_answer()
    assert isinstance(plain_response, StreamingResponse)
    assert plain_response.media_type == "text/plain; charset=utf-8"

    sse_chunks = await collect_async_chunks(sse_token_stream())
    assert sse_chunks[0] == 'event: status\ndata: {"stage":"generating"}\n\n'
    assert sse_chunks[-1] == "event: done\ndata: {}\n\n"
    assert all(chunk.endswith("\n\n") for chunk in sse_chunks)
    token_events = [chunk for chunk in sse_chunks if chunk.startswith("event: token\n")]
    assert len(token_events) == len(TOKENS)

    sse_response = await sse_answer()
    assert isinstance(sse_response, StreamingResponse)
    assert sse_response.media_type == "text/event-stream"

    print("阶段 8 概念块 B 检查通过：streaming response demo looks good")


if __name__ == "__main__":
    asyncio.run(run_checks())
