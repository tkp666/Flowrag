import redis
from sqlalchemy.orm import Session

from app.repositories import kb_repository_get_active_by_id, kb_repository_update
from app.schemas import KnowledgeBaseDetailResponse, KnowledgeBaseUpdate
from app.redis_services import (
    delete_kb_detail_cache,
    get_kb_detail_cache,
    set_kb_detail_cache,
)


def kb_service_get_detail_with_cache(
    session: Session,
    redis_client: redis.Redis,
    kb_id: int,
) -> KnowledgeBaseDetailResponse:
    """
    Cache Aside 查询知识库详情。

    业务流程：
    1. 先查 Redis 缓存；
    2. 命中则返回 KnowledgeBaseDetailResponse(source="redis", data=cached_data)；
    3. 未命中则查 MySQL；
    4. MySQL 也没有时 raise ValueError("知识库不存在")；
    5. MySQL 查到后写入 Redis；
    6. 返回 KnowledgeBaseDetailResponse(source="mysql", data=...)。
    """
    cached_data = get_kb_detail_cache(redis_client, kb_id)
    if cached_data is not None:
        return KnowledgeBaseDetailResponse(source="redis", data=cached_data)
    sql_data = kb_repository_get_active_by_id(session, kb_id)
    if sql_data is None:
        raise ValueError("知识库不存在")
    set_kb_detail_cache(redis_client, sql_data)
    return KnowledgeBaseDetailResponse(
        source="mysql",
        data=sql_data,
    )
    


def kb_service_update_and_invalidate_cache(
    session: Session,
    redis_client: redis.Redis,
    kb_id: int,
    payload: KnowledgeBaseUpdate,
) -> KnowledgeBaseDetailResponse:
    """
    更新 MySQL，并删除 Redis 缓存。

    业务流程：
    1. 查 MySQL 中未删除的知识库；
    2. 不存在则 raise ValueError("知识库不存在")；
    3. 更新 MySQL；
    4. 删除 Redis 里的详情缓存；
    5. 返回 KnowledgeBaseDetailResponse(source="mysql", data=...)。

    注意：
    - 这里是“先更新 MySQL，再删缓存”。
    - 不要更新 Redis 里的旧缓存；删除后让下一次查询回源 MySQL。
    """
    record = kb_repository_get_active_by_id(session, kb_id)
    if record is None:
        raise ValueError("知识库不存在")
    record = kb_repository_update(session, record, payload.name, payload.description)
    delete_kb_detail_cache(redis_client, record.id)
    return KnowledgeBaseDetailResponse(source="mysql", data=record)
