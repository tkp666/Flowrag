"""
阶段 8：流式接口
概念块 A 动手题：普通响应、流式响应、Celery、WebSocket 的边界判断

本文件是“修改已有骨架”的练习文件。

练习目标：
1. 判断不同 FlowRAG 场景应该使用 normal_json / streaming / celery / websocket。
2. 说明为什么 LLM 不支持上游流式时，FastAPI 不能凭空实现真实 token streaming。
3. 说明流式响应开始后，后续错误为什么不能再改 HTTP 状态码。
4. 设计一个最小的 chat/stream 事件顺序，用于后续概念块 B / C 的代码实现。

运行方式：
cd /home/tkp666/FlowRAG/playground/08_streaming_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python homework/section_01_streaming_boundary.py

要求：
- 只修改 TODO 区域。
- 不要引入 FastAPI、Celery、Qdrant、真实 LLM。
- 本题重点是边界判断，不是背概念。
"""

from __future__ import annotations


NORMAL_JSON = "normal_json"
STREAMING = "streaming"
CELERY = "celery"
WEBSOCKET = "websocket"


SCENARIOS = {
    "knowledge_base_detail": "用户打开知识库详情页，需要看到知识库名称、描述、文档数量。",
    "batch_document_ingest": "用户一次上传 200 篇文档，需要解析、切块、embedding、入库。",
    "chat_answer_tokens": "用户问一个问题，希望答案边生成边显示在页面上。",
    "collaborative_editor": "多个用户同时编辑同一份在线文档，需要双向实时同步光标和内容。",
    "task_status_polling": "前端拿着 task_id 查询文档入库任务当前状态。",
    "llm_non_streaming_provider": "外部 LLM API 只支持一次性返回完整答案，不支持 token 流。",
}


def choose_response_style(scenario_name: str) -> str:
    """根据场景选择最合适的响应/任务模式。

    可选返回值：
    - NORMAL_JSON
    - STREAMING
    - CELERY
    - WEBSOCKET
    """
    style_by_scenario = {
        "knowledge_base_detail": NORMAL_JSON,
        "batch_document_ingest": CELERY,
        "chat_answer_tokens": STREAMING,
        "collaborative_editor": WEBSOCKET,
        "task_status_polling": NORMAL_JSON,
        "llm_non_streaming_provider": NORMAL_JSON,
    }
    return style_by_scenario[scenario_name]


def explain_non_streaming_llm_limit() -> str:
    """解释：上游 LLM 不支持流式时，后端为什么不能实现真实 token streaming。

    返回一段中文解释，必须包含下面 3 个关键词：
    - 上游
    - 完整答案
    - token
    """
    return (
        "如果上游 LLM API 只支持一次性返回完整答案，FlowRAG 后端在完整答案返回前"
        "拿不到任何真实 token，所以不能凭空实现真正的 token streaming。"
        "这时后端最多可以先流式返回状态信息，等上游完整答案回来后再一次性发送答案。"
    )


def explain_stream_error_limit() -> str:
    """解释：流式响应开始后，为什么不能再把 HTTP 状态码改成 500。

    返回一段中文解释，必须包含下面 3 个关键词：
    - 响应头
    - 200
    - error 事件
    """
    return (
        "流式响应一旦开始，响应头通常已经发送给客户端，状态码也已经是 200。"
        "后续生成过程中如果失败，服务端不能再把这个响应改成 HTTP 500，"
        "只能在已经打开的流里发送 error 事件，让客户端按约定处理失败。"
    )


def design_chat_stream_events() -> list[str]:
    """设计 FlowRAG /chat/stream 的最小事件顺序。

    要求返回事件名列表。
    必须包含并按合理顺序排列：
    - status:retrieving
    - references
    - status:generating
    - token
    - done

    注意：
    - token 可以只出现一次，表示一类事件，不要求模拟多个 token。
    - references 放在 token 前或 done 前都可以，但你要在下面 explain_reference_timing 里解释理由。
    """
    return [
        "status:retrieving",
        "references",
        "status:generating",
        "token",
        "done",
    ]


def explain_reference_timing() -> str:
    """解释你为什么把 references 放在这个位置。

    返回一段中文解释，必须包含下面 2 个关键词：
    - 检索
    - 引用
    """
    return (
        "references 放在 token 前，是因为 FlowRAG 通常要先完成检索，拿到可引用的 chunks，"
        "再组织 prompt 进入生成阶段。提前发送引用可以让客户端先展示本次回答依据，"
        "也能避免模型已经开始输出后才发现没有可靠检索结果。"
    )


def _assert_contains(text: str, keywords: list[str]) -> None:
    missing = [keyword for keyword in keywords if keyword not in text]
    assert not missing, f"解释缺少关键词：{missing}；当前解释：{text}"


def run_checks() -> None:
    expected_styles = {
        "knowledge_base_detail": NORMAL_JSON,
        "batch_document_ingest": CELERY,
        "chat_answer_tokens": STREAMING,
        "collaborative_editor": WEBSOCKET,
        "task_status_polling": NORMAL_JSON,
        "llm_non_streaming_provider": NORMAL_JSON,
    }

    for scenario_name, expected_style in expected_styles.items():
        actual_style = choose_response_style(scenario_name)
        assert actual_style == expected_style, (
            f"{scenario_name} 判断错误：期望 {expected_style}，实际 {actual_style}。"
            f"场景说明：{SCENARIOS[scenario_name]}"
        )

    _assert_contains(explain_non_streaming_llm_limit(), ["上游", "完整答案", "token"])
    _assert_contains(explain_stream_error_limit(), ["响应头", "200", "error 事件"])

    events = design_chat_stream_events()
    required_events = [
        "status:retrieving",
        "references",
        "status:generating",
        "token",
        "done",
    ]
    for event in required_events:
        assert event in events, f"事件顺序缺少 {event}；当前 events={events}"

    assert events.index("status:retrieving") < events.index("status:generating"), (
        "应该先检索，再生成。"
    )
    assert events.index("status:generating") < events.index("token"), (
        "应该先进入生成阶段，再发送 token。"
    )
    assert events.index("token") < events.index("done"), "done 应该在 token 之后。"

    _assert_contains(explain_reference_timing(), ["检索", "引用"])

    print("阶段 8 概念块 A 动手题通过：streaming boundary looks good")


if __name__ == "__main__":
    run_checks()
