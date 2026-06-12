from __future__ import annotations

from unittest.mock import patch

from celery.result import AsyncResult

from app.celery_app import celery_app
from app.main import app
from app.schemas import TaskCreateRequest, TaskCreateResponse, TaskStatusResponse
from app.services.task_service import get_task_status, run_slow_add
from app.tasks import slow_add_task


class FakeAsyncResult:
    def __init__(self, task_id: str, app=None) -> None:
        self.id = task_id
        self.state = "PENDING"
        self.result = None

    def successful(self) -> bool:
        return False

    def failed(self) -> bool:
        return False


def check_celery_config() -> None:
    assert celery_app.main == "flowrag_stage6"
    assert celery_app.conf.broker_url == "redis://127.0.0.1:6379/0"
    assert celery_app.conf.result_backend == "redis://127.0.0.1:6379/1"
    assert celery_app.conf.task_track_started is True
    assert "app.tasks" in celery_app.conf.include


def check_routes() -> None:
    routes = {route.path for route in app.routes}
    assert "/health" in routes
    assert "/tasks" in routes
    assert "/tasks/{task_id}" in routes


def check_schemas() -> None:
    request = TaskCreateRequest(a=1, b=2)
    assert request.a == 1
    assert request.b == 2
    assert request.fail is False

    created = TaskCreateResponse(
        task_id="task-001",
        state="queued",
        message="任务已投递到 broker，等待 worker 执行",
    )
    assert created.state == "queued"

    status = TaskStatusResponse(
        task_id="task-001",
        celery_state="PENDING",
        result=None,
        error=None,
        warning="demo",
    )
    assert status.result is None


def check_service_logic() -> None:
    with patch("app.services.task_service.time.sleep", return_value=None):
        assert run_slow_add(1, 2, fail=False) == 3
        try:
            run_slow_add(1, 2, fail=True)
        except RuntimeError as exc:
            assert str(exc) == "simulated task failure"
        else:
            raise AssertionError("run_slow_add should raise RuntimeError when fail=True")

    with patch("app.services.task_service.AsyncResult", FakeAsyncResult):
        pending = get_task_status("not-a-real-task-id")
    assert pending.task_id == "not-a-real-task-id"
    assert pending.celery_state == "PENDING"
    assert pending.result is None
    assert pending.error is None
    assert pending.warning == "PENDING 可能表示任务仍在排队，也可能表示 result backend 查不到这个 task_id"


def check_task_registration() -> None:
    assert slow_add_task.name == "app.tasks.slow_add_task"
    assert isinstance(AsyncResult("demo", app=celery_app), AsyncResult)


def main() -> None:
    check_celery_config()
    check_routes()
    check_schemas()
    check_service_logic()
    check_task_registration()
    print("100分：阶段 6 主体实现轻量检查通过")


if __name__ == "__main__":
    main()
