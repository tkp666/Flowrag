"""
阶段 5 第 5 小节动手题：使用真实 Redis 实现简单限流接口逻辑。

本题会连接本机 Redis：
- 默认地址：127.0.0.1
- 默认端口：6379
- 默认 DB：0

这次不启动 FastAPI 服务，而是先把“接口限流”的核心逻辑写成可测试函数。
等阶段主体实现时，再把这些能力合成真正的最小 Redis API 实验。

目标：
1. 为不同动作设计合理的限流 key
2. 使用 Redis INCR + 首次 EXPIRE 实现固定窗口限流
3. 超限时返回 429，不删除 Redis key
4. 返回结构中包含 allowed/status_code/count/limit/remaining/retry_after

运行前确认 Redis 可用：
    redis-cli ping

运行本题：
    cd /home/tkp666/FlowRAG
    /home/tkp666/miniconda3/envs/flowrag/bin/python playground/05_redis_basic/homework/section_05_rate_limit_api.py
"""

from __future__ import annotations

from dataclasses import dataclass

import redis


REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0


@dataclass
class RateLimitResponse:
    allowed: bool
    status_code: int
    action: str
    key: str
    count: int
    limit: int
    remaining: int
    retry_after: int


def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )


def build_user_action_rate_key(user_id: int, action: str) -> str:
    """
    为“某个用户的某个动作”构造限流 key。

    要求：
    - user_id=7, action="chat" 时返回 rate:user:7:chat
    - user_id=7, action="search" 时返回 rate:user:7:search
    - 不要把所有动作都混到同一个 key 里
    """
    return f"rate:user:{user_id}:{action}"


def incr_with_initial_ttl(
    client: redis.Redis,
    key: str,
    window_seconds: int,
) -> int:
    """
    对 key 做 INCR，并只在第一次计数时设置 TTL。

    要求：
    - 使用 client.incr(key)，不要自己 get -> +1 -> set
    - 当 count == 1 时设置 expire
    - 后续请求不要刷新 TTL，否则固定窗口会变成不断续期的窗口
    - 返回 incr 后的 count
    """
    count = client.incr(key)
    if count == 1:
        client.expire(
            key,
            window_seconds,
        )
    return count


def check_user_action_rate_limit(
    client: redis.Redis,
    user_id: int,
    action: str,
    limit: int,
    window_seconds: int,
) -> RateLimitResponse:
    """
    检查某个用户对某个动作是否超过限流。

    要求：
    1. 使用 build_user_action_rate_key(user_id, action) 构造 key
    2. 使用 incr_with_initial_ttl(...) 得到当前窗口 count
    3. 如果 count <= limit：
       - allowed=True
       - status_code=200
       - remaining=limit-count
       - retry_after=0
    4. 如果 count > limit：
       - allowed=False
       - status_code=429
       - remaining=0
       - retry_after=当前 key 的 ttl
       - 不要删除 Redis key
    5. 如果 ttl 返回 -1，说明 key 没有过期时间：
       - 本题中可以立刻补 expire(window_seconds)
       - retry_after 使用补完后的 ttl
    """
    key = build_user_action_rate_key(user_id, action)
    count = incr_with_initial_ttl(client, key, window_seconds)
    if count <= limit:
        return RateLimitResponse(
            allowed=True,
            status_code=200,
            action=action,
            key=key,
            count=count,
            limit=limit,
            remaining=limit - count,
            retry_after=0,
        )
    ttl = client.ttl(key)
    if ttl == -1:
        client.expire(key, window_seconds)
    ttl = client.ttl(key)
    return RateLimitResponse(
        allowed=False,
        status_code=429,
        action=action,
        key=key,
        count=count,
        limit=limit,
        remaining=0,
        retry_after=ttl,
    )


def reset_homework_keys(client: redis.Redis) -> None:
    keys = [
        build_user_action_rate_key(7, "chat"),
        build_user_action_rate_key(7, "search"),
        build_user_action_rate_key(8, "chat"),
    ]
    client.delete(*keys)


def self_check() -> None:
    client = get_redis_client()
    assert client.ping() is True, "Redis 连接失败，请先确认 redis-cli ping 能返回 PONG"

    reset_homework_keys(client)

    chat_key = build_user_action_rate_key(7, "chat")
    search_key = build_user_action_rate_key(7, "search")
    other_user_chat_key = build_user_action_rate_key(8, "chat")

    assert chat_key == "rate:user:7:chat", "chat 限流 key 不符合要求"
    assert search_key == "rate:user:7:search", "不同 action 必须使用不同 key"
    assert other_user_chat_key == "rate:user:8:chat", "不同 user 必须使用不同 key"

    first = check_user_action_rate_limit(
        client,
        user_id=7,
        action="chat",
        limit=3,
        window_seconds=60,
    )
    second = check_user_action_rate_limit(
        client,
        user_id=7,
        action="chat",
        limit=3,
        window_seconds=60,
    )
    third = check_user_action_rate_limit(
        client,
        user_id=7,
        action="chat",
        limit=3,
        window_seconds=60,
    )
    fourth = check_user_action_rate_limit(
        client,
        user_id=7,
        action="chat",
        limit=3,
        window_seconds=60,
    )

    assert first.allowed is True and first.status_code == 200
    assert first.count == 1 and first.remaining == 2 and first.retry_after == 0
    assert second.allowed is True and second.count == 2 and second.remaining == 1
    assert third.allowed is True and third.count == 3 and third.remaining == 0
    assert fourth.allowed is False and fourth.status_code == 429
    assert fourth.count == 4 and fourth.remaining == 0
    assert fourth.retry_after > 0, "超限时必须告诉调用方多久后可以重试"
    assert client.exists(chat_key) == 1, "超限后不能删除 key，否则用户可以绕过限流"

    ttl_before = client.ttl(chat_key)
    check_user_action_rate_limit(
        client,
        user_id=7,
        action="chat",
        limit=3,
        window_seconds=60,
    )
    ttl_after = client.ttl(chat_key)
    assert ttl_after <= ttl_before, "后续请求不应该刷新 TTL"

    search_first = check_user_action_rate_limit(
        client,
        user_id=7,
        action="search",
        limit=2,
        window_seconds=60,
    )
    assert search_first.allowed is True
    assert search_first.count == 1, "chat 和 search 应该是两个独立计数器"

    other_user_first = check_user_action_rate_limit(
        client,
        user_id=8,
        action="chat",
        limit=3,
        window_seconds=60,
    )
    assert other_user_first.allowed is True
    assert other_user_first.count == 1, "不同用户的 chat 限流应该互不影响"

    client.set(chat_key, "10")
    client.persist(chat_key)
    no_ttl = check_user_action_rate_limit(
        client,
        user_id=7,
        action="chat",
        limit=3,
        window_seconds=60,
    )
    assert no_ttl.allowed is False
    assert no_ttl.status_code == 429
    assert no_ttl.retry_after > 0, "发现 ttl=-1 后应该补上过期时间"

    reset_homework_keys(client)
    print("section 05 rate limit api homework looks good")


if __name__ == "__main__":
    self_check()
