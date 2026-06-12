"""
阶段 6 综合课后题：把 Celery 最小实验迁移到 FlowRAG 文档入库场景。

当前课堂已切换为模式 D：Codex 主讲主写，用户主理解提问。
所以本文件不是要求你从零补完代码，而是把阶段 6 必须掌握的设计判断
用一份可运行的参考答案固定下来。

运行方式：

cd /home/tkp666/FlowRAG/playground/06_celery_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python homework/lesson_06_document_ingest_design.py

预期输出：

lesson 06 document ingest design looks good
"""

from dataclasses import dataclass


@dataclass
class IngestSubmitPlan:
    api_endpoint: str
    router_responsibility: str
    service_responsibility: str
    task_responsibility: str
    broker_payload: dict
    immediate_response: dict


@dataclass
class IngestStatusPlan:
    query_endpoint: str
    mysql_role: str
    redis_role: str
    celery_backend_role: str
    pending_warning: str


def build_document_ingest_submit_plan(document_id: int, task_id: str) -> IngestSubmitPlan:
    """
    设计文档入库任务的提交链路。

    关键判断：
    1. API 不等待解析、切块、embedding、Qdrant 写入全部完成。
    2. Celery 消息里不要放文件字节流，只放轻量标识。
    3. router 不直接散落 .delay(...)，任务投递由 service 封装。
    """
    return IngestSubmitPlan(
        api_endpoint=f"POST /documents/{document_id}/ingest",
        router_responsibility="接收 document_id，调用 service，不直接写 .delay(...)",
        service_responsibility="校验文档存在和权限，创建任务记录，投递 Celery 任务，返回 task_id",
        task_responsibility="worker 后台执行解析、切块、embedding、Qdrant 写入，并更新状态",
        broker_payload={
            "task_name": "app.tasks.ingest_document_task",
            "document_id": document_id,
            "task_id": task_id,
        },
        immediate_response={
            "task_id": task_id,
            "state": "queued",
            "message": "文档入库任务已提交，后台处理中",
        },
    )


def build_document_ingest_status_plan(task_id: str) -> IngestStatusPlan:
    """
    设计文档入库任务的状态查询链路。

    关键判断：
    1. MySQL 保存最终、权威、可追溯状态。
    2. Redis 适合保存短期过程进度。
    3. Celery result backend 可以辅助查询 worker 执行状态，但不应是唯一业务事实来源。
    """
    return IngestStatusPlan(
        query_endpoint=f"GET /tasks/{task_id}",
        mysql_role="保存任务是否存在、属于谁、最终状态、失败原因、关联 document_id",
        redis_role="保存短期进度，例如 parsing / embedding / writing_vector 和百分比",
        celery_backend_role="辅助查看 Celery 的 PENDING / STARTED / SUCCESS / FAILURE，不应是唯一业务事实来源",
        pending_warning="PENDING 可能是排队中，也可能是 task_id 不存在、结果过期或 backend 查不到",
    )


def explain_why_not_send_file_bytes_to_celery() -> list[str]:
    """
    解释为什么 Celery 消息里不建议直接传文件字节流。
    """
    return [
        "broker 会承受大消息压力，Redis 内存成本和网络传输成本都会上升",
        "任务消息应该轻量，适合传 document_id、task_id、file_path 或 object_key",
        "大文件更适合放磁盘、对象存储或专门文件服务，再让 worker 按路径或 key 读取",
        "消息过大时，失败重试、序列化、反序列化和排查日志都会变得更难",
    ]


def check_submit_plan() -> None:
    plan = build_document_ingest_submit_plan(document_id=101, task_id="task-abc")

    assert plan.api_endpoint == "POST /documents/101/ingest"
    assert ".delay" in plan.router_responsibility
    assert "不直接" in plan.router_responsibility
    assert "创建任务记录" in plan.service_responsibility
    assert "投递 Celery" in plan.service_responsibility
    assert "worker 后台执行" in plan.task_responsibility
    assert plan.broker_payload == {
        "task_name": "app.tasks.ingest_document_task",
        "document_id": 101,
        "task_id": "task-abc",
    }
    assert plan.immediate_response["state"] == "queued"


def check_status_plan() -> None:
    plan = build_document_ingest_status_plan(task_id="task-abc")

    assert plan.query_endpoint == "GET /tasks/task-abc"
    assert "最终状态" in plan.mysql_role
    assert "失败原因" in plan.mysql_role
    assert "短期进度" in plan.redis_role
    assert "PENDING" in plan.celery_backend_role
    assert "不应是唯一" in plan.celery_backend_role
    assert "结果过期" in plan.pending_warning


def check_file_bytes_explanation() -> None:
    reasons = explain_why_not_send_file_bytes_to_celery()

    assert len(reasons) >= 4
    assert any("Redis 内存成本" in reason for reason in reasons)
    assert any("document_id" in reason for reason in reasons)
    assert any("file_path" in reason or "object_key" in reason for reason in reasons)


def main() -> None:
    check_submit_plan()
    check_status_plan()
    check_file_bytes_explanation()
    print("lesson 06 document ingest design looks good")


if __name__ == "__main__":
    main()
