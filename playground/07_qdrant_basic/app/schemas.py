from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class SeedResponse(BaseModel):
    collection_name: str
    vector_size: int
    inserted_count: int


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)
    kb_id: int | None = Field(default=None, ge=1)


class SearchHit(BaseModel):
    point_id: int
    score: float
    text: str
    document_id: int
    kb_id: int
    chunk_index: int


class SearchResponse(BaseModel):
    collection_name: str
    query: str
    top_k: int
    kb_id: int | None
    hits: list[SearchHit]

