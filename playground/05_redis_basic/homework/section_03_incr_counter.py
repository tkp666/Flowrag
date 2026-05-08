"""
阶段 5 第 3 小节动手题：使用真实 Redis 实现 INCR 计数器。

本题会连接本机 Redis：
- 默认地址：127.0.0.1
- 默认端口：6379
- 默认 DB：0

目标：
1. 实现 INCR + 首次设置 TTL 的最小模板
2. 实现一个简单 chat 接口限流判断
3. 理解为什么不能用 get -> +1 -> set 代替 incr

运行前确认 Redis 可用：
    redis-cli ping

运行本题：
    cd /home/tkp666/FlowRAG
    /home/tkp666/miniconda3/envs/flowrag/bin/python playground/05_redis_basic/homework/section_03_incr_counter.py
"""

from __future__ import annotations

from dataclasses import dataclass

import redis


REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0


@dataclass
class RateLimitResult:
    allowed: bool
    count: int
    remaining: int
    ttl: int


def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )


def incr_with_ttl(client: redis.Redis, key: str, ttl_seconds: int) -> int:
    """
    对 key 做 INCR。

    要求：
    - 使用 Redis 的 incr，不要自己 get -> +1 -> set
    - 只有当 count == 1 时，才设置 expire
    - 返回 incr 后的 count
    """
    count = client.incr(key)
    if count == 1:
        client.expire(key, ttl_seconds)
    return count


def check_chat_rate_limit(
    client: redis.Redis,
    user_id: int,
    limit: int = 3,
    window_seconds: int = 60,
) -> RateLimitResult:
    """
    判断用户在一个时间窗口内是否还能调用 chat。

    key 设计：
    - 使用 rate:user:{user_id}:chat

    返回：
    - allowed: count <= limit 时为 True，否则 False
    - count: 当前窗口内已经调用的次数
    - remaining: 还剩多少次可用，不能小于 0
    - ttl: 当前 key 剩余过期时间
    """
    key = f"rate:user:{user_id}:chat"
    count = incr_with_ttl(client, key, window_seconds)
    return RateLimitResult(
        allowed=count <= limit,
        count=count,
        remaining=max(limit - count, 0),
        ttl=client.ttl(key),
    )
    


def reset_homework_keys(client: redis.Redis) -> None:
    keys = [
        "homework:section03:counter",
        "rate:user:7:chat",
    ]
    if keys:
        client.delete(*keys)


def self_check() -> None:
    client = get_redis_client()
    assert client.ping() is True, "Redis 连接失败，请先确认 redis-cli ping 能返回 PONG"

    reset_homework_keys(client)

    counter_key = "homework:section03:counter"
    count1 = incr_with_ttl(client, counter_key, ttl_seconds=30)
    ttl1 = client.ttl(counter_key)
    count2 = incr_with_ttl(client, counter_key, ttl_seconds=30)
    ttl2 = client.ttl(counter_key)

    assert count1 == 1, "第一次 incr 后应该返回 1"
    assert count2 == 2, "第二次 incr 后应该返回 2"
    assert ttl1 > 0, "第一次 incr 后必须设置 TTL"
    assert ttl2 > 0, "第二次 incr 后 TTL 应该仍然存在"
    assert ttl2 <= ttl1, "后续 incr 不应该刷新 TTL，否则窗口会被不断延长"

    first = check_chat_rate_limit(client, user_id=7, limit=3, window_seconds=60)
    second = check_chat_rate_limit(client, user_id=7, limit=3, window_seconds=60)
    third = check_chat_rate_limit(client, user_id=7, limit=3, window_seconds=60)
    fourth = check_chat_rate_limit(client, user_id=7, limit=3, window_seconds=60)

    assert first.allowed is True and first.count == 1 and first.remaining == 2
    assert second.allowed is True and second.count == 2 and second.remaining == 1
    assert third.allowed is True and third.count == 3 and third.remaining == 0
    assert fourth.allowed is False and fourth.count == 4 and fourth.remaining == 0
    assert fourth.ttl > 0, "限流 key 必须有 TTL"

    reset_homework_keys(client)
    print("section 03 incr counter homework looks good")


if __name__ == "__main__":
    self_check()
