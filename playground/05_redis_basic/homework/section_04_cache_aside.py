"""
阶段 5 第 4 小节动手题：使用真实 Redis 实现 Cache Aside 简单缓存。

本题会连接本机 Redis：
- 默认地址：127.0.0.1
- 默认端口：6379
- 默认 DB：0

这次不连接真实 MySQL，而是用 FAKE_MYSQL_KB_TABLE 模拟 MySQL。
你要练习的是缓存流程，不是 SQLAlchemy。

目标：
1. 查询知识库详情时，先查 Redis 缓存
2. 缓存未命中时，回源 FAKE_MYSQL_KB_TABLE，再写入 Redis
3. 写入 Redis 时使用 JSON 字符串，并设置 TTL
4. 更新知识库名称时，先更新 MySQL 模拟表，再删除对应 Redis 缓存

运行前确认 Redis 可用：
    redis-cli ping

运行本题：
    cd /home/tkp666/FlowRAG
    /home/tkp666/miniconda3/envs/flowrag/bin/python playground/05_redis_basic/homework/section_04_cache_aside.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import redis


REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
CACHE_TTL_SECONDS = 300


FAKE_MYSQL_KB_TABLE: dict[int, dict[str, object]] = {
    1: {
        "id": 1,
        "name": "paper-kb",
        "description": "论文知识库",
        "doc_count": 18,
    },
    2: {
        "id": 2,
        "name": "backend-notes",
        "description": "后端学习笔记",
        "doc_count": 6,
    },
}


@dataclass
class CacheResult:
    source: str
    data: dict[str, object]


def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )


def build_kb_detail_cache_key(kb_id: int) -> str:
    """
    返回知识库详情缓存 key。

    要求：
    - kb_id=1 时，返回 cache:kb:1:detail
    """
    return f"cache:kb:{kb_id}:detail"


def query_kb_detail_from_mysql(kb_id: int) -> dict[str, object] | None:
    """
    模拟从 MySQL 查询知识库详情。

    要求：
    - 如果 FAKE_MYSQL_KB_TABLE 中不存在 kb_id，返回 None
    - 如果存在，返回这条记录的浅拷贝，避免调用方直接修改模拟表
    """
    record = FAKE_MYSQL_KB_TABLE.get(kb_id)
    if record is None:
        return None
    return record.copy()


def get_kb_detail_with_cache(
    client: redis.Redis,
    kb_id: int,
    ttl_seconds: int = CACHE_TTL_SECONDS,
) -> CacheResult:
    """
    使用 Cache Aside 模式查询知识库详情。

    要求：
    1. 先根据 kb_id 构造 Redis key
    2. 先查 Redis
       - 如果命中，使用 json.loads 还原数据，并返回 CacheResult(source="redis", data=...)
    3. 如果 Redis 未命中，再调用 query_kb_detail_from_mysql(kb_id)
       - 如果 MySQL 模拟表也查不到，抛出 ValueError("knowledge base not found")
    4. MySQL 查到后，把数据 json.dumps 成字符串写入 Redis
       - 必须设置 TTL
       - 推荐使用 client.set(key, value, ex=ttl_seconds)
    5. 最后返回 CacheResult(source="mysql", data=...)
    """
    Redis_key = build_kb_detail_cache_key(kb_id)
    Redis_data = client.get(Redis_key)
    if Redis_data is not None:
        data = json.loads(Redis_data)
        return CacheResult(
            source="redis",
            data=data,
        )
    else:
        sql_data = query_kb_detail_from_mysql(kb_id)
        if sql_data is None:
            raise ValueError("knowledge base not found")
        else:
            client.set(
                Redis_key,
                json.dumps(sql_data, ensure_ascii=False),
                ex=ttl_seconds,
            )
            return CacheResult(
                source="mysql",
                data=sql_data,
            )
        
        
    


def update_kb_name_and_invalidate_cache(
    client: redis.Redis,
    kb_id: int,
    new_name: str,
) -> dict[str, object]:
    """
    更新知识库名称，并删除对应详情缓存。

    要求：
    1. 如果 kb_id 不存在，抛出 ValueError("knowledge base not found")
    2. 先更新 FAKE_MYSQL_KB_TABLE 中的 name
    3. 再删除 Redis 中的 cache:kb:{kb_id}:detail
    4. 返回更新后的知识库详情浅拷贝
    """
    kb_sql = query_kb_detail_from_mysql(kb_id)
    if kb_sql is None:
        raise ValueError("knowledge base not found")
    FAKE_MYSQL_KB_TABLE[kb_id]["name"] = new_name
    client.delete(build_kb_detail_cache_key(kb_id))
    return FAKE_MYSQL_KB_TABLE[kb_id].copy()


def reset_homework_keys(client: redis.Redis) -> None:
    keys = [
        build_kb_detail_cache_key(1),
        build_kb_detail_cache_key(2),
        build_kb_detail_cache_key(999),
    ]
    client.delete(*keys)


def reset_fake_mysql_table() -> None:
    FAKE_MYSQL_KB_TABLE.clear()
    FAKE_MYSQL_KB_TABLE.update(
        {
            1: {
                "id": 1,
                "name": "paper-kb",
                "description": "论文知识库",
                "doc_count": 18,
            },
            2: {
                "id": 2,
                "name": "backend-notes",
                "description": "后端学习笔记",
                "doc_count": 6,
            },
        }
    )


def self_check() -> None:
    client = get_redis_client()
    assert client.ping() is True, "Redis 连接失败，请先确认 redis-cli ping 能返回 PONG"

    reset_fake_mysql_table()
    reset_homework_keys(client)

    key = build_kb_detail_cache_key(1)
    assert key == "cache:kb:1:detail", "缓存 key 命名不符合要求"

    first = get_kb_detail_with_cache(client, kb_id=1, ttl_seconds=60)
    assert first.source == "mysql", "第一次查询应该缓存未命中，回源 MySQL"
    assert first.data["name"] == "paper-kb"
    assert client.exists(key) == 1, "回源 MySQL 后应该写入 Redis 缓存"
    assert client.ttl(key) > 0, "缓存必须设置 TTL"

    second = get_kb_detail_with_cache(client, kb_id=1, ttl_seconds=60)
    assert second.source == "redis", "第二次查询应该命中 Redis 缓存"
    assert second.data == first.data, "Redis 还原后的数据应该和 MySQL 查询结果一致"

    updated = update_kb_name_and_invalidate_cache(client, kb_id=1, new_name="rag-notes")
    assert updated["name"] == "rag-notes", "应该更新模拟 MySQL 中的知识库名称"
    assert client.exists(key) == 0, "更新 MySQL 后必须删除旧 Redis 缓存"

    third = get_kb_detail_with_cache(client, kb_id=1, ttl_seconds=60)
    assert third.source == "mysql", "缓存删除后，下一次查询应该重新回源 MySQL"
    assert third.data["name"] == "rag-notes", "重新回源后应该拿到 MySQL 中的新名称"

    try:
        get_kb_detail_with_cache(client, kb_id=999, ttl_seconds=60)
    except ValueError as exc:
        assert str(exc) == "knowledge base not found"
    else:
        raise AssertionError("不存在的知识库应该抛出 ValueError")

    reset_homework_keys(client)
    reset_fake_mysql_table()
    print("section 04 cache aside homework looks good")


if __name__ == "__main__":
    self_check()
