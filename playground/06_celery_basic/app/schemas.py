from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class TaskCreateRequest(BaseModel):
    a: int = Field(..., description="第一个加数")
    b: int = Field(..., description="第二个加数")
    fail: bool = Field(default=False, description="是否模拟任务失败")


class TaskCreateResponse(BaseModel):
    task_id: str
    state: str
    message: str


class TaskStatusResponse(BaseModel):
    task_id: str
    celery_state: str
    result: int | None
    error: str | None
    warning: str | None
