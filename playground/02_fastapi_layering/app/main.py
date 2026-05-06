from fastapi import FastAPI

from app.api.kb_router import router as kb_router


app = FastAPI(
    title="FastAPI Layering Demo",
    description="阶段 2：FastAPI 分层结构最小实验",
    version="0.1.0",
)


app.include_router(kb_router)
