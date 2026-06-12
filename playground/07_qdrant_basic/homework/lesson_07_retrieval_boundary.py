from __future__ import annotations


def choose_storage_for_field(field_name: str) -> str:
    """Return the right storage owner for a FlowRAG retrieval field.

    This is the stage 7 comprehensive homework reference answer. The goal is
    to separate authoritative business data from vector-search data.
    """
    mysql_fields = {
        "user_id",
        "kb_name",
        "document_filename",
        "document_ingest_status",
        "document_created_at",
    }
    qdrant_payload_fields = {
        "chunk_text",
        "chunk_vector",
        "document_id",
        "kb_id",
        "chunk_index",
    }
    service_fields = {
        "top_k",
        "query_text",
        "score_threshold",
    }

    if field_name in mysql_fields:
        return "mysql"
    if field_name in qdrant_payload_fields:
        return "qdrant"
    if field_name in service_fields:
        return "retrieval_service"
    return "unknown"


def should_use_kb_filter(user_query: str, kb_id: int | None) -> bool:
    """Decide whether Qdrant search must include a knowledge-base filter."""
    return bool(user_query.strip()) and kb_id is not None


def build_reference_text(document_id: int, chunk_index: int, text: str) -> str:
    """Build a minimal citation string from Qdrant payload fields."""
    return f"document_id={document_id}, chunk_index={chunk_index}: {text}"


def main() -> None:
    assert choose_storage_for_field("kb_name") == "mysql"
    assert choose_storage_for_field("chunk_vector") == "qdrant"
    assert choose_storage_for_field("top_k") == "retrieval_service"
    assert should_use_kb_filter("qdrant search", kb_id=1) is True
    assert should_use_kb_filter("qdrant search", kb_id=None) is False
    assert build_reference_text(10, 2, "demo") == "document_id=10, chunk_index=2: demo"
    print("lesson 07 retrieval boundary looks good")


if __name__ == "__main__":
    main()

