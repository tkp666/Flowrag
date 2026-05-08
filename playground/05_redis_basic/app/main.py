from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator, Generator

import redis
from fastapi import Depends, FastAPI, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.db import get_db, init_db
from app.redis_client import get_redis_client
from app.redis_services import check_rate_limit, incr_counter
from app.repositories import kb_repository_seed
from app.schemas import (
    CounterResponse,
    HealthResponse,
    KnowledgeBaseDetailResponse,
    KnowledgeBaseUpdate,
    RateLimitResponse,
    SeedResponse,
)
from app.services import (
    kb_service_get_detail_with_cache,
    kb_service_update_and_invalidate_cache,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    yield


app = FastAPI(
    title="FlowRAG Stage 5 Redis Playground",
    version="0.1.0",
    lifespan=lifespan,
)


def get_redis() -> Generator[redis.Redis, None, None]:
    client = get_redis_client()
    try:
        yield client
    finally:
        client.close()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/dev/seed", response_model=SeedResponse)
def seed_demo_data(
    session: Session = Depends(get_db),
) -> SeedResponse:
    records = kb_repository_seed(session)
    return SeedResponse(
        created_count=len(records),
        kb_ids=[record.id for record in records],
    )


@app.get("/knowledge-bases/{kb_id}", response_model=KnowledgeBaseDetailResponse)
def get_knowledge_base_detail(
    kb_id: int,
    session: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> KnowledgeBaseDetailResponse:
    try:
        return kb_service_get_detail_with_cache(session, redis_client, kb_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.patch("/knowledge-bases/{kb_id}", response_model=KnowledgeBaseDetailResponse)
def update_knowledge_base(
    kb_id: int,
    payload: KnowledgeBaseUpdate,
    session: Session = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
) -> KnowledgeBaseDetailResponse:
    try:
        return kb_service_update_and_invalidate_cache(session, redis_client, kb_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/counter/{name}/incr", response_model=CounterResponse)
def increase_counter(
    name: str,
    redis_client: redis.Redis = Depends(get_redis),
) -> CounterResponse:
    key, count, ttl = incr_counter(redis_client, name)
    return CounterResponse(key=key, count=count, ttl=ttl)


@app.get("/limited-resource", response_model=RateLimitResponse)
def limited_resource(
    response: Response,
    user_id: int = Query(default=1, ge=1),
    action: str = Query(default="chat", min_length=1, max_length=50),
    redis_client: redis.Redis = Depends(get_redis),
) -> RateLimitResponse:
    result = check_rate_limit(redis_client, user_id=user_id, action=action)
    response.status_code = result.status_code
    return result
