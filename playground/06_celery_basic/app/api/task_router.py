from fastapi import APIRouter

from app.schemas import TaskCreateRequest, TaskCreateResponse, TaskStatusResponse
from app.services.task_service import get_task_status, submit_add_task


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskCreateResponse)
def create_task(payload: TaskCreateRequest) -> TaskCreateResponse:
    return submit_add_task(
        a=payload.a,
        b=payload.b,
        fail=payload.fail,
    )


@router.get("/{task_id}", response_model=TaskStatusResponse)
def read_task_status(task_id: str) -> TaskStatusResponse:
    return get_task_status(task_id)
