from __future__ import annotations

import math


VECTOR_SIZE = 6


KEYWORD_GROUPS: tuple[tuple[str, ...], ...] = (
    ("fastapi", "api", "http", "router", "接口", "路由"),
    ("celery", "worker", "task", "background", "queue", "async", "后台", "任务"),
    ("qdrant", "vector", "embedding", "search", "similarity", "top-k", "collection", "point", "payload", "向量", "检索"),
    ("redis", "cache", "rate", "limit", "broker", "缓存", "限流"),
    ("mysql", "sql", "database", "metadata", "table", "数据库", "元数据"),
    ("document", "chunk", "kb", "knowledge", "reference", "文档", "知识库", "引用"),
)


def embed_text(text: str) -> list[float]:
    """Return a deterministic teaching vector for text.

    This is not a real embedding model. It only makes similar demo texts land
    near each other so the Qdrant workflow can be learned without an API key.
    """
    normalized = text.lower()
    vector = [0.0 for _ in range(VECTOR_SIZE)]

    for index, keywords in enumerate(KEYWORD_GROUPS):
        for keyword in keywords:
            if keyword in normalized:
                vector[index] += 1.0

    if not any(vector):
        for index, char in enumerate(normalized.encode("utf-8")):
            vector[index % VECTOR_SIZE] += (char % 13) / 13.0

    length = math.sqrt(sum(value * value for value in vector))
    if length == 0:
        return [0.0 for _ in range(VECTOR_SIZE)]

    return [round(value / length, 6) for value in vector]

