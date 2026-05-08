from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str


class SeedResponse(BaseModel):
    created_count: int
    kb_ids: list[int]


class KnowledgeBaseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class KnowledgeBaseData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    name: str
    description: str | None = None
    document_count: int


class KnowledgeBaseDetailResponse(BaseModel):
    source: str
    data: KnowledgeBaseData


class CounterResponse(BaseModel):
    key: str
    count: int
    ttl: int


class RateLimitResponse(BaseModel):
    allowed: bool
    status_code: int
    key: str
    count: int
    limit: int
    ttl: int
    retry_after: int
