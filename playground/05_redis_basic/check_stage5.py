"""
阶段 5 主体实现一键检查脚本。

用途：
- 不启动 uvicorn；
- 使用 SQLite 内存数据库检查 SQLAlchemy 逻辑；
- 使用真实 Redis 检查缓存、计数器和限流；
- 检查阶段 5 主体实现的关键行为，而不是只看函数能不能跑。

运行方式：
cd /home/tkp666/FlowRAG/playground/05_redis_basic
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage5.py

通过时输出：
100分：阶段 5 主体实现检查全部通过
"""

from collections.abc import Callable
import sys
import traceback

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import models  # noqa: F401
from app.db import Base
from app.main import app, health
from app.models import KnowledgeBaseModel
from app.redis_client import get_redis_client
from app.redis_services import (
    build_counter_key,
    build_kb_detail_cache_key,
    build_rate_limit_key,
    check_rate_limit,
    incr_counter,
)
from app.repositories import kb_repository_seed
from app.schemas import HealthResponse, KnowledgeBaseDetailResponse, KnowledgeBaseUpdate
from app.services import (
    kb_service_get_detail_with_cache,
    kb_service_update_and_invalidate_cache,
)


class Stage5CheckError(AssertionError):
    pass


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise Stage5CheckError(message)


def assert_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise Stage5CheckError(f"{message}：实际={actual!r}，期望={expected!r}")


def expect_value_error(func: Callable[[], object], expected_message: str) -> None:
    try:
        func()
    except ValueError as exc:
        assert_equal(str(exc), expected_message, "ValueError 文案不正确")
        return
    raise Stage5CheckError(f"应该抛出 ValueError({expected_message!r})，但没有抛出")


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return SessionLocal()


def make_redis_client() -> redis.Redis:
    client = get_redis_client()
    try:
        assert_true(client.ping() is True, "Redis 连接失败，请先确认 redis-cli ping 能返回 PONG")
    except Exception as exc:
        raise Stage5CheckError(f"Redis 连接失败：{exc}") from exc
    return client


def cleanup_stage5_keys(client: redis.Redis) -> None:
    patterns = [
        "cache:kb:*:detail",
        "counter:stage5:*",
        "rate:user:*:stage5-*",
    ]
    for pattern in patterns:
        keys = list(client.scan_iter(pattern))
        if keys:
            client.delete(*keys)


def check_routes_and_health() -> None:
    result = health()
    assert_true(isinstance(result, HealthResponse), "/health 应该返回 HealthResponse")
    assert_equal(result.status, "ok", "/health status 不正确")

    paths = {route.path for route in app.routes}
    expected_paths = {
        "/health",
        "/dev/seed",
        "/knowledge-bases/{kb_id}",
        "/counter/{name}/incr",
        "/limited-resource",
    }
    missing = expected_paths - paths
    assert_true(not missing, f"FastAPI 路由缺失：{sorted(missing)}")


def check_model_shape() -> None:
    table = KnowledgeBaseModel.__table__
    assert_true(table.c.id.primary_key, "knowledge_bases.id 应该是主键")
    assert_true(table.c.owner_id.index is True, "knowledge_bases.owner_id 应该建普通索引")
    assert_equal(table.c.name.type.length, 100, "knowledge_bases.name 长度不正确")
    assert_equal(table.c.description.type.length, 255, "knowledge_bases.description 长度不正确")
    assert_equal(table.c.document_count.default.arg, 0, "document_count 默认值应该是 0")
    assert_equal(table.c.is_deleted.default.arg, False, "is_deleted 默认值应该是 False")


def check_cache_aside(session: Session, client: redis.Redis) -> None:
    records = kb_repository_seed(session)
    kb_id = records[0].id
    cache_key = build_kb_detail_cache_key(kb_id)

    assert_true(client.delete(cache_key) in {0, 1}, "删除旧缓存失败")

    first = kb_service_get_detail_with_cache(session, client, kb_id)
    assert_true(isinstance(first, KnowledgeBaseDetailResponse), "查询详情应该返回 KnowledgeBaseDetailResponse")
    assert_equal(first.source, "mysql", "第一次查询应该回源 MySQL")
    assert_equal(first.data.name, "paper-kb", "第一次查询数据不正确")
    assert_true(client.exists(cache_key) == 1, "第一次 MySQL 回源后应该写入 Redis 缓存")
    assert_true(client.ttl(cache_key) > 0, "知识库详情缓存应该有 TTL")

    second = kb_service_get_detail_with_cache(session, client, kb_id)
    assert_equal(second.source, "redis", "第二次查询应该命中 Redis")
    assert_equal(second.data.name, "paper-kb", "Redis 缓存数据不正确")

    updated = kb_service_update_and_invalidate_cache(
        session,
        client,
        kb_id,
        KnowledgeBaseUpdate(name="paper-kb-v2", description="更新后的论文知识库"),
    )
    assert_equal(updated.source, "mysql", "更新接口应该返回 MySQL 权威数据")
    assert_equal(updated.data.name, "paper-kb-v2", "更新后的 name 不正确")
    assert_equal(client.exists(cache_key), 0, "更新 MySQL 后应该删除旧缓存")

    third = kb_service_get_detail_with_cache(session, client, kb_id)
    assert_equal(third.source, "mysql", "删缓存后第一次查询应该重新回源 MySQL")
    assert_equal(third.data.name, "paper-kb-v2", "重新回源后应该看到新名称")

    fourth = kb_service_get_detail_with_cache(session, client, kb_id)
    assert_equal(fourth.source, "redis", "重新写缓存后下一次应该命中 Redis")
    assert_equal(fourth.data.name, "paper-kb-v2", "新缓存不应该还是旧名称")

    expect_value_error(
        lambda: kb_service_get_detail_with_cache(session, client, 999999),
        "知识库不存在",
    )
    expect_value_error(
        lambda: kb_service_update_and_invalidate_cache(
            session,
            client,
            999999,
            KnowledgeBaseUpdate(name="missing", description=None),
        ),
        "知识库不存在",
    )


def check_counter(client: redis.Redis) -> None:
    name = "stage5:demo-counter"
    key = build_counter_key(name)
    client.delete(key)

    first_key, first_count, first_ttl = incr_counter(client, name, ttl_seconds=60)
    assert_equal(first_key, key, "计数器返回 key 不正确")
    assert_equal(first_count, 1, "第一次 INCR 后 count 应该是 1")
    assert_true(0 < first_ttl <= 60, "第一次 INCR 后应该有 TTL")

    second_key, second_count, second_ttl = incr_counter(client, name, ttl_seconds=60)
    assert_equal(second_key, key, "第二次计数器 key 不正确")
    assert_equal(second_count, 2, "第二次 INCR 后 count 应该是 2")
    assert_true(0 < second_ttl <= first_ttl, "第二次 INCR 不应该刷新出更长窗口")

    client.persist(key)
    assert_equal(client.ttl(key), -1, "测试准备失败：key 应该被移除 TTL")
    _, third_count, third_ttl = incr_counter(client, name, ttl_seconds=60)
    assert_equal(third_count, 3, "补 TTL 时也应该正常 INCR")
    assert_true(0 < third_ttl <= 60, "ttl=-1 时应该补过期时间")


def check_rate_limit_behavior(client: redis.Redis) -> None:
    user_id = 9001
    action = "stage5-chat"
    key = build_rate_limit_key(user_id, action)
    client.delete(key)

    first = check_rate_limit(client, user_id, action, limit=3, window_seconds=60)
    second = check_rate_limit(client, user_id, action, limit=3, window_seconds=60)
    third = check_rate_limit(client, user_id, action, limit=3, window_seconds=60)
    fourth = check_rate_limit(client, user_id, action, limit=3, window_seconds=60)

    assert_true(first.allowed is True, "第 1 次请求应该允许")
    assert_true(second.allowed is True, "第 2 次请求应该允许")
    assert_true(third.allowed is True, "第 3 次请求应该允许")
    assert_true(fourth.allowed is False, "第 4 次请求应该被限流")
    assert_equal(fourth.status_code, 429, "限流时 status_code 应该是 429")
    assert_equal(fourth.key, key, "限流 key 不正确")
    assert_equal(fourth.count, 4, "第 4 次请求 count 应该是 4")
    assert_true(0 < fourth.ttl <= 60, "限流 key 应该有 TTL")
    assert_equal(fourth.retry_after, fourth.ttl, "超限时 retry_after 应该等于 ttl")

    client.persist(key)
    assert_equal(client.ttl(key), -1, "测试准备失败：限流 key 应该被移除 TTL")
    repaired = check_rate_limit(client, user_id, action, limit=10, window_seconds=60)
    assert_true(repaired.ttl > 0, "ttl=-1 的限流 key 应该被修复")


def main() -> int:
    session = make_session()
    client = make_redis_client()
    cleanup_stage5_keys(client)
    checks = [
        ("路由和健康检查", lambda: check_routes_and_health()),
        ("SQLAlchemy model 结构", lambda: check_model_shape()),
        ("Cache Aside 查询和更新失效", lambda: check_cache_aside(session, client)),
        ("Redis INCR 计数器", lambda: check_counter(client)),
        ("Redis 用户维度限流", lambda: check_rate_limit_behavior(client)),
    ]

    try:
        for name, check in checks:
            check()
            print(f"通过：{name}")
    except Exception:
        print("阶段 5 主体实现检查失败：")
        traceback.print_exc()
        return 1
    finally:
        cleanup_stage5_keys(client)
        client.close()
        session.close()

    print("100分：阶段 5 主体实现检查全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
