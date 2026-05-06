"""
阶段 3 补充专题 · 综合课后动手题：FlowRAG 并发工具选型与响应方案

作业目标：
1. 综合判断 async / 线程池 / 进程池 / Celery 的适用边界。
2. 区分“当前请求必须等结果”和“后台任务慢慢跑”。
3. 根据选型设计最小响应结构，而不是只写一个工具名字。

这不是让你重复实现前面的线程池或进程池模板。
这道题更接近真实后端设计：拿到一个业务场景，判断它应该怎么执行、接口应该怎么返回。
"""

ASYNC_IO = "async_io"
THREAD_POOL = "thread_pool"
PROCESS_POOL = "process_pool"
CELERY_BACKGROUND = "celery_background"


def choose_strategy(scene: dict) -> dict:
    """
    TODO:
    根据 scene 里的信息返回并发工具选型。

    scene 字段说明：
    - name: 场景名
    - must_return_now: 当前 HTTP 请求是否必须等结果
    - is_cpu_heavy: 是否 CPU 密集
    - uses_sync_blocking_sdk: 是否使用同步阻塞 SDK
    - uses_async_io: 是否主要是异步 I/O 等待
    - independent_subtasks: 是否存在多个互不依赖的子任务

    返回结构必须是：

    {
        "name": scene["name"],
        "strategy": "...",
        "wait_for_result": True 或 False,
        "reason": "用中文写一句原因",
    }

    选型优先级：
    1. 如果 must_return_now 是 False，优先 CELERY_BACKGROUND。
    2. 如果当前请求必须等结果，并且 is_cpu_heavy 是 True，选 PROCESS_POOL。
    3. 如果当前请求必须等结果，并且 uses_sync_blocking_sdk 是 True，选 THREAD_POOL。
    4. 如果当前请求必须等结果，并且 uses_async_io 是 True，选 ASYNC_IO。

    注意：
    - 不要只根据 name 硬编码。
    - reason 不需要很长，但必须体现判断依据。
    """
    # 在这里完成你的代码
    if scene["must_return_now"] is False:
        return {
            "name": scene["name"],
            "strategy": "celery_background",
            "wait_for_result": False,
            "reason": "并非需要立即得到结果，可以放后台跑，所以用Celery",
    }
    if scene["is_cpu_heavy"] is True:
        return {
            "name": scene["name"],
            "strategy": "process_pool",
            "wait_for_result": True,
            "reason": "CPU密集需要用进程池",
    }
    if scene["uses_sync_blocking_sdk"] is True:
        return {
            "name": scene["name"],
            "strategy": "thread_pool",
            "wait_for_result": True,
            "reason": "会被同步阻塞的需要用线程池",
    }
    if scene["uses_async_io"] is True:
        return {
            "name": scene["name"],
            "strategy": "async_io",
            "wait_for_result": True,
            "reason": "如果是等待异步IO任务的要用async_io",
    }
    


def build_response_contract(decision: dict) -> dict:
    """
    TODO:
    根据 choose_strategy(...) 的结果，设计最小接口响应方案。

    如果 strategy 是 CELERY_BACKGROUND：
    - HTTP 状态码用 202
    - response 里应该有 task_id 和 status

    其他 strategy：
    - HTTP 状态码用 200
    - response 里应该有 status 和 strategy

    返回结构必须是：

    {
        "http_status": 200 或 202,
        "response": {...},
    }
    """
    # 在这里完成你的代码
    if decision["strategy"] == "celery_background":
        return {
        "http_status": 202,
        "response": {"task_id": 1, "status": "queued"},
    }
    else :
        return {
        "http_status": 200,
        "response": {"status": "done", "strategy": decision["strategy"]},
    }
        


def build_scene_plan(scene: dict) -> dict:
    """
    TODO:
    组合 choose_strategy(...) 和 build_response_contract(...)。

    返回结构必须是：

    {
        "decision": {...},
        "contract": {...},
    }
    """
    # 在这里完成你的代码
    decision = choose_strategy(scene)
    contract = build_response_contract(decision)
    return {
        "decision": decision,
        "contract": contract,
    }


def self_check() -> None:
    scenes = [
        {
            "name": "chat_waiting_for_external_llm",
            "must_return_now": True,
            "is_cpu_heavy": False,
            "uses_sync_blocking_sdk": False,
            "uses_async_io": True,
            "independent_subtasks": False,
        },
        {
            "name": "pdf_first_page_preview_now",
            "must_return_now": True,
            "is_cpu_heavy": False,
            "uses_sync_blocking_sdk": True,
            "uses_async_io": False,
            "independent_subtasks": False,
        },
        {
            "name": "chunk_quality_scan_now",
            "must_return_now": True,
            "is_cpu_heavy": True,
            "uses_sync_blocking_sdk": False,
            "uses_async_io": False,
            "independent_subtasks": True,
        },
        {
            "name": "upload_200_documents_ingestion",
            "must_return_now": False,
            "is_cpu_heavy": True,
            "uses_sync_blocking_sdk": True,
            "uses_async_io": False,
            "independent_subtasks": True,
        },
        {
            "name": "dashboard_three_independent_panels",
            "must_return_now": True,
            "is_cpu_heavy": False,
            "uses_sync_blocking_sdk": False,
            "uses_async_io": True,
            "independent_subtasks": True,
        },
    ]

    plans = [build_scene_plan(scene) for scene in scenes]

    decisions = {plan["decision"]["name"]: plan["decision"] for plan in plans}
    contracts = {plan["decision"]["name"]: plan["contract"] for plan in plans}

    assert decisions["chat_waiting_for_external_llm"]["strategy"] == ASYNC_IO
    assert decisions["chat_waiting_for_external_llm"]["wait_for_result"] is True
    assert contracts["chat_waiting_for_external_llm"]["http_status"] == 200

    assert decisions["pdf_first_page_preview_now"]["strategy"] == THREAD_POOL
    assert decisions["pdf_first_page_preview_now"]["wait_for_result"] is True
    assert contracts["pdf_first_page_preview_now"]["http_status"] == 200

    assert decisions["chunk_quality_scan_now"]["strategy"] == PROCESS_POOL
    assert decisions["chunk_quality_scan_now"]["wait_for_result"] is True
    assert contracts["chunk_quality_scan_now"]["http_status"] == 200

    assert decisions["upload_200_documents_ingestion"]["strategy"] == CELERY_BACKGROUND
    assert decisions["upload_200_documents_ingestion"]["wait_for_result"] is False
    assert contracts["upload_200_documents_ingestion"]["http_status"] == 202
    assert "task_id" in contracts["upload_200_documents_ingestion"]["response"]

    assert decisions["dashboard_three_independent_panels"]["strategy"] == ASYNC_IO
    assert decisions["dashboard_three_independent_panels"]["wait_for_result"] is True
    assert contracts["dashboard_three_independent_panels"]["http_status"] == 200

    for plan in plans:
        reason = plan["decision"]["reason"]
        assert isinstance(reason, str)
        assert len(reason.strip()) >= 8

    print("concurrency decision plan homework looks good")


if __name__ == "__main__":
    self_check()
