from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.mock_embedding import VECTOR_SIZE, embed_text
from app.schemas import SearchHit


COLLECTION_NAME = "flowrag_stage7_chunks"


@dataclass(frozen=True)
class DemoChunk:
    point_id: int
    text: str
    document_id: int
    kb_id: int
    chunk_index: int


DEMO_CHUNKS: tuple[DemoChunk, ...] = (
    DemoChunk(
        point_id=1,
        text="FastAPI router exposes HTTP API endpoints for FlowRAG.",
        document_id=101,
        kb_id=1,
        chunk_index=0,
    ),
    DemoChunk(
        point_id=2,
        text="Celery worker runs background document ingest tasks from a queue.",
        document_id=102,
        kb_id=1,
        chunk_index=0,
    ),
    DemoChunk(
        point_id=3,
        text="Qdrant collection stores vector points for similarity search.",
        document_id=103,
        kb_id=1,
        chunk_index=0,
    ),
    DemoChunk(
        point_id=4,
        text="Qdrant payload keeps document_id, kb_id and chunk_index for references.",
        document_id=103,
        kb_id=1,
        chunk_index=1,
    ),
    DemoChunk(
        point_id=5,
        text="Redis cache and rate limit data should stay short-lived.",
        document_id=201,
        kb_id=2,
        chunk_index=0,
    ),
    DemoChunk(
        point_id=6,
        text="MySQL database stores knowledge base metadata and document metadata.",
        document_id=202,
        kb_id=2,
        chunk_index=0,
    ),
)


def create_qdrant_client() -> QdrantClient:
    qdrant_url = os.getenv("FLOWRAG_STAGE7_QDRANT_URL")
    if qdrant_url:
        return QdrantClient(url=qdrant_url)
    return QdrantClient(":memory:")


client = create_qdrant_client()


def reset_collection(qdrant: QdrantClient = client) -> None:
    if qdrant.collection_exists(COLLECTION_NAME):
        qdrant.delete_collection(COLLECTION_NAME)

    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )


def seed_demo_chunks(qdrant: QdrantClient = client) -> int:
    if not qdrant.collection_exists(COLLECTION_NAME):
        reset_collection(qdrant)

    points = [
        PointStruct(
            id=chunk.point_id,
            vector=embed_text(chunk.text),
            payload={
                "text": chunk.text,
                "document_id": chunk.document_id,
                "kb_id": chunk.kb_id,
                "chunk_index": chunk.chunk_index,
            },
        )
        for chunk in DEMO_CHUNKS
    ]
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)


def reset_and_seed(qdrant: QdrantClient = client) -> int:
    reset_collection(qdrant)
    return seed_demo_chunks(qdrant)


def search_chunks(
    query: str,
    top_k: int = 3,
    kb_id: int | None = None,
    qdrant: QdrantClient = client,
) -> list[SearchHit]:
    if not qdrant.collection_exists(COLLECTION_NAME):
        reset_and_seed(qdrant)

    query_filter = _build_kb_filter(kb_id)
    scored_points = _query_points(
        qdrant=qdrant,
        query_vector=embed_text(query),
        top_k=top_k,
        query_filter=query_filter,
    )

    return [_to_search_hit(point) for point in scored_points]


def _build_kb_filter(kb_id: int | None) -> Filter | None:
    if kb_id is None:
        return None

    return Filter(
        must=[
            FieldCondition(
                key="kb_id",
                match=MatchValue(value=kb_id),
            )
        ]
    )


def _query_points(
    qdrant: QdrantClient,
    query_vector: list[float],
    top_k: int,
    query_filter: Filter | None,
) -> list[Any]:
    if hasattr(qdrant, "query_points"):
        result = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
        )
        return list(result.points)
    '''if hasattr(qdrant, "query_points"):
        ...
    return list(qdrant.search(...))

    这是为了兼容不同版本的 qdrant-client。

    有些版本推荐用：

    query_points(...)

    有些旧版本用：

    search(...)
    '''
    return list(
        qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
        )
    )


def _to_search_hit(point: Any) -> SearchHit:
    payload = point.payload or {}
    return SearchHit(
        point_id=int(point.id),
        score=round(float(point.score), 6),
        text=str(payload["text"]),
        document_id=int(payload["document_id"]),
        kb_id=int(payload["kb_id"]),
        chunk_index=int(payload["chunk_index"]),
    )

