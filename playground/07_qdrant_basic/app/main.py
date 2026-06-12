from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.qdrant_client import COLLECTION_NAME, reset_and_seed, search_chunks
from app.mock_embedding import VECTOR_SIZE
from app.schemas import HealthResponse, SearchRequest, SearchResponse, SeedResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    reset_and_seed()
    yield


app = FastAPI(
    title="FlowRAG Stage 7 Qdrant Playground",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/dev/reset", response_model=SeedResponse)
def reset_demo_data() -> SeedResponse:
    inserted_count = reset_and_seed()
    return SeedResponse(
        collection_name=COLLECTION_NAME,
        vector_size=VECTOR_SIZE,
        inserted_count=inserted_count,
    )


@app.post("/search", response_model=SearchResponse)
def search(payload: SearchRequest) -> SearchResponse:
    hits = search_chunks(
        query=payload.query,
        top_k=payload.top_k,
        kb_id=payload.kb_id,
    )
    return SearchResponse(
        collection_name=COLLECTION_NAME,
        query=payload.query,
        top_k=payload.top_k,
        kb_id=payload.kb_id,
        hits=hits,
    )

