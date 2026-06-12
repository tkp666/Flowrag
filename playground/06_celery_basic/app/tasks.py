from app.celery_app import celery_app
from app.services.task_service import run_slow_add


@celery_app.task(name="app.tasks.slow_add_task")
def slow_add_task(a: int, b: int, fail: bool = False) -> int:
    """
    Celery worker 入口。

    这里保持很薄，只把任务交给 service 中的业务函数。
    """
    return run_slow_add(a, b, fail)
