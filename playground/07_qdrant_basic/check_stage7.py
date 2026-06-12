from __future__ import annotations

from app.main import app
from app.mock_embedding import VECTOR_SIZE, embed_text
from app.qdrant_client import COLLECTION_NAME, reset_and_seed, search_chunks
from app.schemas import SearchRequest


def check_routes() -> None:
    routes = {route.path for route in app.routes}
    assert "/health" in routes
    assert "/dev/reset" in routes
    assert "/search" in routes


def check_embedding() -> None:
    vector = embed_text("qdrant vector search payload")
    assert len(vector) == VECTOR_SIZE
    assert any(value > 0 for value in vector)
    assert embed_text("qdrant vector search payload") == vector


def check_schemas() -> None:
    request = SearchRequest(query="qdrant vector search", top_k=2, kb_id=1)
    assert request.query == "qdrant vector search"
    assert request.top_k == 2
    assert request.kb_id == 1


def check_qdrant_flow() -> None:
    inserted_count = reset_and_seed()
    assert inserted_count == 6

    hits = search_chunks("qdrant vector search payload", top_k=3)
    assert len(hits) == 3
    assert hits[0].kb_id == 1
    assert "Qdrant" in hits[0].text

    kb1_hits = search_chunks("qdrant vector search payload", top_k=5, kb_id=1)
    assert len(kb1_hits) > 0
    assert all(hit.kb_id == 1 for hit in kb1_hits)

    kb2_hits = search_chunks("qdrant vector search payload", top_k=5, kb_id=2)
    assert len(kb2_hits) > 0
    assert all(hit.kb_id == 2 for hit in kb2_hits)
    assert {hit.document_id for hit in kb2_hits}.issubset({201, 202})


def main() -> None:
    check_routes()
    check_embedding()
    check_schemas()
    check_qdrant_flow()
    print("100分：阶段 7 主体实现轻量检查通过")


if __name__ == "__main__":
    main()

