import json

import redis

from app.models import KnowledgeBaseModel
from app.schemas import KnowledgeBaseData, RateLimitResponse


KB_DETAIL_CACHE_TTL_SECONDS = 300
COUNTER_TTL_SECONDS = 600
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 3


def build_kb_detail_cache_key(kb_id: int) -> str:
    return f"cache:kb:{kb_id}:detail"


def build_counter_key(name: str) -> str:
    return f"counter:{name}"


def build_rate_limit_key(user_id: int, action: str) -> str:
    return f"rate:user:{user_id}:{action}"


def kb_model_to_cache_dict(kb: KnowledgeBaseModel) -> dict:
    return {
        "id": kb.id,
        "owner_id": kb.owner_id,
        "name": kb.name,
        "description": kb.description,
        "document_count": kb.document_count,
    }


def get_kb_detail_cache(
    client: redis.Redis,
    kb_id: int,
) -> KnowledgeBaseData | None:
    """
    从 Redis 读取知识库详情缓存。

    要求：
    - key 必须使用 build_kb_detail_cache_key(kb_id)
    - client.get(key) 没取到时返回 None
    - 取到 JSON 字符串后，用 json.loads 还原成 dict
    - 返回 KnowledgeBaseData(**data)
    """
    key = build_kb_detail_cache_key(kb_id)
    kb_redis = client.get(key)
    if kb_redis is None:
        return None
    kb_redis = json.loads(kb_redis)
    return KnowledgeBaseData(**kb_redis)

def set_kb_detail_cache(
    client: redis.Redis,
    kb: KnowledgeBaseModel,
    ttl_seconds: int = KB_DETAIL_CACHE_TTL_SECONDS,
) -> None:
    """
    把 MySQL 查到的知识库详情写入 Redis。

    要求：
    - key 必须使用 build_kb_detail_cache_key(kb.id)
    - value 使用 json.dumps(kb_model_to_cache_dict(kb), ensure_ascii=False)
    - 使用 setex(key, ttl_seconds, value)，保证写 value 和设置 TTL 是一个 Redis 命令
    """
    key = build_kb_detail_cache_key(kb.id)
    client.setex(
        key,
        ttl_seconds,
        json.dumps(kb_model_to_cache_dict(kb), ensure_ascii=False),
    )


def delete_kb_detail_cache(client: redis.Redis, kb_id: int) -> None:
    """
    删除知识库详情缓存。

    要求：
    - key 必须使用 build_kb_detail_cache_key(kb_id)
    - 调 client.delete(key)
    """
    key = build_kb_detail_cache_key(kb_id)
    client.delete(key)


def incr_counter(
    client: redis.Redis,
    name: str,
    ttl_seconds: int = COUNTER_TTL_SECONDS,
) -> tuple[str, int, int]:
    """
    通用计数器。

    要求：
    - key 使用 build_counter_key(name)
    - 使用 client.incr(key)
    - 只有 count == 1 时设置 expire(key, ttl_seconds)
    - 如果 ttl(key) 返回 -1，说明 key 没有过期时间，需要补 expire
    - 返回 (key, count, ttl)
    """
    key = build_counter_key(name)
    count = client.incr(key)
    if count == 1:
        client.expire(key, ttl_seconds)
    ttl = client.ttl(key)
    if ttl == -1:
        client.expire(key, ttl_seconds)
    ttl = client.ttl(key)
    return (
        key,
        count,
        ttl,
    )


def check_rate_limit(
    client: redis.Redis,
    user_id: int,
    action: str,
    limit: int = RATE_LIMIT_MAX_REQUESTS,
    window_seconds: int = RATE_LIMIT_WINDOW_SECONDS,
) -> RateLimitResponse:
    """
    用户维度限流。

    要求：
    - key 使用 build_rate_limit_key(user_id, action)
    - 使用 client.incr(key)
    - 只有 count == 1 时设置 expire(key, window_seconds)
    - 如果 ttl(key) 返回 -1，需要补 expire
    - count <= limit 时 allowed=True, status_code=200, retry_after=0
    - count > limit 时 allowed=False, status_code=429, retry_after=ttl
    """
    key = build_rate_limit_key(user_id, action)
    count = client.incr(key)
    if count == 1:
        client.expire(key, window_seconds)
    ttl = client.ttl(key)
    if ttl == -1:
        client.expire(key, window_seconds)
    ttl = client.ttl(key)
    if count <= limit:
        return RateLimitResponse(
            allowed=True,
            status_code=200,
            key=key,
            count=count,
            limit=limit,
            ttl=ttl,
            retry_after=0,
        )
    return RateLimitResponse(
        allowed=False,
        status_code=429,
        key=key,
        count=count,
        limit=limit,
        ttl=ttl,
        retry_after=ttl,
    )
