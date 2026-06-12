"""
阶段 8 综合课后动手题：流式问答边界设计（参考实现版）

作业位置：
    playground/08_streaming_basic/homework/lesson_08_streaming_review.py

文件作用：
    这不是再复制一遍 `/chat/stream`，而是用可运行代码复盘阶段 8 的核心判断：
    1. 什么场景用普通 JSON / SSE / Celery / WebSocket；
    2. 哪些错误应该在流开始前变成 HTTP 错误；
    3. 哪些错误只能在流开始后变成 SSE error 事件；
    4. FlowRAG 流式问答应该按什么事件顺序返回。

运行方式：
    cd /home/tkp666/FlowRAG/playground/08_streaming_basic
    /home/tkp666/miniconda3/envs/flowrag/bin/python homework/lesson_08_streaming_review.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RequestCase:
    question: str
    kb_exists: bool
    retrieval_ok: bool
    llm_ok: bool


def choose_backend_tool(scene: str) -> str:
    """根据业务场景选择后端工具。"""
    choices = {
        "health_check": "json",
        "chat_answer_stream": "sse",
        "document_ingest": "celery",
        "realtime_collaboration": "websocket",
    }

    return choices[scene]


def pre_stream_validation(case: RequestCase) -> tuple[bool, str]:
    """判断请求是否能开始流式响应。"""
    if not case.question.strip():
        return False, "HTTP 400: question must not be empty"

    if not case.kb_exists:
        return False, "HTTP 404: knowledge base not found"

    return True, "ok"


def build_flowrag_event_plan(case: RequestCase) -> list[str]:
    """设计 FlowRAG 流式问答的事件顺序。"""
    can_start_stream, error = pre_stream_validation(case)
    if not can_start_stream:
        return [error]

    events = ["status:retrieving"]

    if not case.retrieval_ok:
        events.append("error:qdrant search failed")
        return events

    events.extend(["references", "status:generating"])

    if not case.llm_ok:
        events.extend(["token", "token", "error:llm provider failed"])
        return events

    events.extend(["token", "token", "token", "done"])
    return events


def explain_client_action(event: str) -> str:
    """说明前端收到不同 SSE 事件时应该做什么。"""
    if event.startswith("status:"):
        return "更新页面状态提示"
    if event == "references":
        return "保存并展示引用来源"
    if event == "token":
        return "追加到当前答案文本"
    if event.startswith("error:"):
        return "停止等待并展示错误状态"
    if event == "done":
        return "标记本次回答完成"

    raise ValueError(f"unknown event: {event}")


def run_checks() -> None:
    assert choose_backend_tool("health_check") == "json"
    assert choose_backend_tool("chat_answer_stream") == "sse"
    assert choose_backend_tool("document_ingest") == "celery"
    assert choose_backend_tool("realtime_collaboration") == "websocket"

    assert build_flowrag_event_plan(
        RequestCase(
            question="   ",
            kb_exists=True,
            retrieval_ok=True,
            llm_ok=True,
        )
    ) == ["HTTP 400: question must not be empty"]

    assert build_flowrag_event_plan(
        RequestCase(
            question="hello",
            kb_exists=False,
            retrieval_ok=True,
            llm_ok=True,
        )
    ) == ["HTTP 404: knowledge base not found"]

    assert build_flowrag_event_plan(
        RequestCase(
            question="FlowRAG 为什么要用流式问答？",
            kb_exists=True,
            retrieval_ok=False,
            llm_ok=True,
        )
    ) == ["status:retrieving", "error:qdrant search failed"]

    assert build_flowrag_event_plan(
        RequestCase(
            question="FlowRAG 为什么要用流式问答？",
            kb_exists=True,
            retrieval_ok=True,
            llm_ok=False,
        )
    ) == [
        "status:retrieving",
        "references",
        "status:generating",
        "token",
        "token",
        "error:llm provider failed",
    ]

    assert build_flowrag_event_plan(
        RequestCase(
            question="FlowRAG 为什么要用流式问答？",
            kb_exists=True,
            retrieval_ok=True,
            llm_ok=True,
        )
    ) == [
        "status:retrieving",
        "references",
        "status:generating",
        "token",
        "token",
        "token",
        "done",
    ]

    assert explain_client_action("status:retrieving") == "更新页面状态提示"
    assert explain_client_action("references") == "保存并展示引用来源"
    assert explain_client_action("token") == "追加到当前答案文本"
    assert explain_client_action("error:llm provider failed") == "停止等待并展示错误状态"
    assert explain_client_action("done") == "标记本次回答完成"

    print("阶段 8 综合课后动手题通过：streaming review looks good")


if __name__ == "__main__":
    run_checks()
