"""
阶段 8：流式接口
概念块 B 动手题参考实现：StreamingResponse 与 SSE 事件格式

本文件是 Codex 主讲主写模式下的参考答案。

练习目标：
1. 用函数生成合法 SSE 事件字符串。
2. 用异步生成器模拟 status -> token -> done 的流式输出。
3. 用代码检查每条 SSE 事件都以空行结束。
4. 创建 StreamingResponse，并确认 media_type 正确。
5. 说明 curl -N 和 SSE 空行的作用。

运行方式：
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python homework/section_02_streaming_response_mechanics.py
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi.responses import StreamingResponse


TOKENS = ["FlowRAG", " 可以", " 使用", " SSE", " 返回结构化事件。"]


def make_sse_event(event: str, data: dict | str) -> str:
    """把事件名和数据转换成 SSE 文本格式。

    SSE 的最小格式是：

    event: token
    data: xxx

    最后一行必须是空行，所以字符串必须以两个换行符结尾。
    """
    if isinstance(data, str):
        payload = data
    else:
        payload = json.dumps(data, ensure_ascii=False)

    return f"event: {event}\ndata: {payload}\n\n"


async def answer_event_stream() -> AsyncGenerator[str, None]:
    """模拟一个最小 SSE 问答流。

    当前只覆盖概念块 B：
    - status 表示后端进入生成阶段；
    - token 表示答案片段；
    - done 表示流结束。

    FlowRAG 真实 references / retrieving / error 会在概念块 C 继续讲。
    """
    yield make_sse_event("status", {"stage": "generating"})

    for token in TOKENS:
        await asyncio.sleep(0)
        yield make_sse_event("token", token)

    yield make_sse_event("done", {})


async def collect_stream_chunks() -> list[str]:
    chunks: list[str] = []
    async for chunk in answer_event_stream():
        chunks.append(chunk)
    return chunks


def create_sse_response() -> StreamingResponse:
    return StreamingResponse(
        answer_event_stream(),
        media_type="text/event-stream",
    )


def explain_curl_no_buffer() -> str:
    return (
        "curl -N 的作用是关闭 curl 客户端缓冲，让终端尽量在收到每个 chunk 后立刻显示。"
        "否则后端已经 yield 了多段内容，客户端仍可能攒到一起再展示，导致误判流式响应没有生效。"
    )


def explain_sse_blank_line() -> str:
    return (
        "SSE 使用空行表示一条事件结束，所以每条事件必须以两个换行符结尾。"
        "如果缺少这个空行，客户端可能认为事件还没结束，从而迟迟不触发对应的 message 或自定义事件。"
    )


async def run_checks() -> None:
    event = make_sse_event("token", "FlowRAG")
    assert event == "event: token\ndata: FlowRAG\n\n"

    json_event = make_sse_event("status", {"stage": "generating"})
    assert json_event == 'event: status\ndata: {"stage": "generating"}\n\n'

    chunks = await collect_stream_chunks()
    assert chunks[0].startswith("event: status\n")
    assert chunks[-1] == "event: done\ndata: {}\n\n"
    assert all(chunk.endswith("\n\n") for chunk in chunks)

    token_chunks = [chunk for chunk in chunks if chunk.startswith("event: token\n")]
    assert len(token_chunks) == len(TOKENS)

    response = create_sse_response()
    assert isinstance(response, StreamingResponse)
    assert response.media_type == "text/event-stream"

    assert "缓冲" in explain_curl_no_buffer()
    assert "空行" in explain_sse_blank_line()

    print("阶段 8 概念块 B 动手题通过：streaming response mechanics looks good")


if __name__ == "__main__":
    asyncio.run(run_checks())
