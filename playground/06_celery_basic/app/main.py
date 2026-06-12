from fastapi import FastAPI

from app.api.task_router import router as task_router
from app.schemas import HealthResponse


app = FastAPI(
    title="FlowRAG Stage 6 Celery Playground",
    version="0.1.0",
)

app.include_router(task_router)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
