import time

from celery.result import AsyncResult

from app.celery_app import celery_app
from app.schemas import TaskCreateResponse, TaskStatusResponse


def run_slow_add(a: int, b: int, fail: bool = False) -> int:
    """
    模拟后台耗时业务。

    真实 FlowRAG 中，这里会替换成文档解析、切块、embedding、入库等流程。
    """
    time.sleep(5)
    if fail:
        raise RuntimeError("simulated task failure")
    return a + b


def submit_add_task(a: int, b: int, fail: bool = False) -> TaskCreateResponse:
    """
    提交后台任务。

    注意：Celery task 的导入放在函数内部，避免 app.tasks 和 service 互相在模块加载期循环导入。
    """
    from app.tasks import slow_add_task

    async_result = slow_add_task.delay(a, b, fail)
    return TaskCreateResponse(
        task_id=async_result.id,
        state="queued",
        message="任务已投递到 broker，等待 worker 执行",
    )


def get_task_status(task_id: str) -> TaskStatusResponse:
    """
    查询 Celery 任务状态。

    本阶段只查 Celery result backend。正式 FlowRAG 里应先查 MySQL 任务表，
    再结合 Celery 状态和 Redis 过程进度。
    """
    async_result = AsyncResult(task_id, app=celery_app)

    warning = None
    if async_result.state == "PENDING":
        warning = "PENDING 可能表示任务仍在排队，也可能表示 result backend 查不到这个 task_id"

    if async_result.successful():
        return TaskStatusResponse(
            task_id=task_id,
            celery_state=async_result.state,
            result=async_result.result,
            error=None,
            warning=warning,
        )

    if async_result.failed():
        return TaskStatusResponse(
            task_id=task_id,
            celery_state=async_result.state,
            result=None,
            error=str(async_result.result),
            warning=warning,
        )

    return TaskStatusResponse(
        task_id=task_id,
        celery_state=async_result.state,
        result=None,
        error=None,
        warning=warning,
    )
