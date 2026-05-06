"""
阶段 4 主体实现一键检查脚本。

用途：
- 不启动 uvicorn
- 不要求本机 MySQL
- 使用 SQLite 内存数据库检查阶段 4 的核心 repository / service 逻辑

运行方式：
cd /home/tkp666/FlowRAG/playground/04_mysql_sqlalchemy
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage4.py

通过时输出：
100分：阶段 4 主体实现检查全部通过

失败时会输出具体失败在哪个检查项。
"""

from collections.abc import Callable
import sys
import traceback

from sqlalchemy import UniqueConstraint, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import models  # noqa: F401
from app.db import Base
from app.main import app, health
from app.models import KnowledgeBaseModel, UserModel
from app.schemas import KBCreate, KBPageResponse, KBResponse, KBUpdate, UserCreate, UserResponse
from app.services import (
    kb_service_create,
    kb_service_delete,
    kb_service_get,
    kb_service_list,
    kb_service_update,
    user_service_create,
)


class Stage4CheckError(AssertionError):
    pass


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise Stage4CheckError(message)


def assert_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise Stage4CheckError(f"{message}：实际={actual!r}，期望={expected!r}")


def expect_value_error(func: Callable[[], object], expected_message: str) -> None:
    try:
        func()
    except ValueError as exc:
        assert_equal(str(exc), expected_message, "ValueError 文案不正确")
        return
    raise Stage4CheckError(f"应该抛出 ValueError({expected_message!r})，但没有抛出")


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return SessionLocal()


def check_routes_and_health() -> None:
    assert_equal(health(), {"status": "ok"}, "/health 逻辑返回不正确")
    paths = {route.path for route in app.routes}
    expected_paths = {
        "/health",
        "/users",
        "/knowledge-bases",
        "/knowledge-bases/{kb_id}",
    }
    missing = expected_paths - paths
    assert_true(not missing, f"FastAPI 路由缺失：{sorted(missing)}")


def check_models() -> None:
    user_table = UserModel.__table__
    kb_table = KnowledgeBaseModel.__table__

    assert_true(user_table.c.id.primary_key, "users.id 应该是主键")
    assert_equal(user_table.c.email.type.length, 255, "users.email 长度不正确")
    assert_true(user_table.c.email.unique is True, "users.email 应该唯一")
    assert_equal(user_table.c.username.type.length, 50, "users.username 长度不正确")
    assert_true(user_table.c.username.unique is True, "users.username 应该唯一")

    assert_true(kb_table.c.id.primary_key, "knowledge_bases.id 应该是主键")
    assert_true(kb_table.c.user_id.index is True, "knowledge_bases.user_id 应该建普通索引")
    foreign_keys = list(kb_table.c.user_id.foreign_keys)
    assert_equal(len(foreign_keys), 1, "knowledge_bases.user_id 外键数量不正确")
    assert_equal(foreign_keys[0].target_fullname, "users.id", "knowledge_bases.user_id 应该指向 users.id")

    unique_constraints = [
        constraint
        for constraint in kb_table.constraints
        if isinstance(constraint, UniqueConstraint)
    ]
    assert_true(
        any(set(constraint.columns.keys()) == {"user_id", "name"} for constraint in unique_constraints),
        "knowledge_bases 应该有 user_id + name 的联合唯一约束",
    )


def check_user_create(session: Session) -> tuple[UserResponse, UserResponse]:
    user_a = user_service_create(session, UserCreate(email="a@example.com", username="alice"))
    user_b = user_service_create(session, UserCreate(email="b@example.com", username="bob"))

    assert_true(isinstance(user_a, UserResponse), "user_service_create 应该返回 UserResponse")
    assert_true(isinstance(user_b, UserResponse), "user_service_create 应该返回 UserResponse")
    assert_true(user_a.id != user_b.id, "两个用户的 id 不应该相同")
    assert_equal(user_a.email, "a@example.com", "user_a.email 不正确")
    assert_equal(user_a.username, "alice", "user_a.username 不正确")
    return user_a, user_b


def check_kb_create_and_duplicate(session: Session, user_a: UserResponse, user_b: UserResponse) -> tuple[KBResponse, KBResponse, KBResponse]:
    kb_a1 = kb_service_create(
        session,
        KBCreate(name="paper-kb", description="论文知识库"),
        current_user_id=user_a.id,
    )
    kb_a2 = kb_service_create(
        session,
        KBCreate(name="interview-kb", description="面试知识库"),
        current_user_id=user_a.id,
    )
    kb_b1 = kb_service_create(
        session,
        KBCreate(name="paper-kb", description="另一个用户的同名知识库"),
        current_user_id=user_b.id,
    )

    assert_true(isinstance(kb_a1, KBResponse), "kb_service_create 应该返回 KBResponse")
    assert_equal(kb_a1.name, "paper-kb", "kb_a1.name 不正确")
    assert_equal(kb_a2.name, "interview-kb", "kb_a2.name 不正确")
    assert_equal(kb_b1.name, "paper-kb", "不同用户应该允许同名知识库")

    expect_value_error(
        lambda: kb_service_create(
            session,
            KBCreate(name="paper-kb", description="重复知识库"),
            current_user_id=user_a.id,
        ),
        "知识库名称已存在",
    )
    expect_value_error(
        lambda: kb_service_create(
            session,
            KBCreate(name="ghost-kb", description=None),
            current_user_id=999999,
        ),
        "用户不存在",
    )
    return kb_a1, kb_a2, kb_b1


def check_kb_list(session: Session, user_a: UserResponse, user_b: UserResponse) -> None:
    page_1 = kb_service_list(session, current_user_id=user_a.id, page=1, page_size=1)
    page_2 = kb_service_list(session, current_user_id=user_a.id, page=2, page_size=1)
    user_b_page = kb_service_list(session, current_user_id=user_b.id, page=1, page_size=10)

    assert_true(isinstance(page_1, KBPageResponse), "kb_service_list 应该返回 KBPageResponse")
    assert_equal(page_1.total, 2, "user_a 未删除知识库 total 不正确")
    assert_equal(page_1.page, 1, "page_1.page 不正确")
    assert_equal(page_1.page_size, 1, "page_1.page_size 不正确")
    assert_equal([item.name for item in page_1.items], ["paper-kb"], "user_a 第 1 页 items 不正确")
    assert_equal([item.name for item in page_2.items], ["interview-kb"], "user_a 第 2 页 items 不正确")
    assert_equal(user_b_page.total, 1, "user_b total 不正确")
    assert_equal([item.name for item in user_b_page.items], ["paper-kb"], "user_b items 不正确")


def check_kb_get_update_delete(
    session: Session,
    user_a: UserResponse,
    user_b: UserResponse,
    kb_a1: KBResponse,
    kb_a2: KBResponse,
    kb_b1: KBResponse,
) -> None:
    own_kb = kb_service_get(session, kb_a1.id, current_user_id=user_a.id)
    assert_equal(own_kb.name, "paper-kb", "查询自己的知识库详情不正确")

    expect_value_error(
        lambda: kb_service_get(session, kb_b1.id, current_user_id=user_a.id),
        "不能访问别人的知识库",
    )

    updated = kb_service_update(
        session,
        kb_a2.id,
        KBUpdate(name="job-kb", description="求职知识库"),
        current_user_id=user_a.id,
    )
    assert_equal(updated.name, "job-kb", "更新知识库 name 不正确")
    assert_equal(updated.description, "求职知识库", "更新知识库 description 不正确")

    desc_only = kb_service_create(
        session,
        KBCreate(name="empty-desc-kb", description=None),
        current_user_id=user_a.id,
    )
    desc_only_updated = kb_service_update(
        session,
        desc_only.id,
        KBUpdate(name=None, description="补充描述"),
        current_user_id=user_a.id,
    )
    assert_equal(desc_only_updated.id, desc_only.id, "更新 description 不应该改变知识库 id")
    assert_equal(desc_only_updated.name, "empty-desc-kb", "只更新 description 时不应该改变 name")
    assert_equal(desc_only_updated.description, "补充描述", "只更新 description 时应该成功写入新描述")

    expect_value_error(
        lambda: kb_service_update(
            session,
            kb_a2.id,
            KBUpdate(name="paper-kb", description=None),
            current_user_id=user_a.id,
        ),
        "知识库名称已存在",
    )
    expect_value_error(
        lambda: kb_service_update(
            session,
            kb_b1.id,
            KBUpdate(name="wrong-update", description=None),
            current_user_id=user_a.id,
        ),
        "不能修改别人的知识库",
    )

    deleted = kb_service_delete(session, kb_a1.id, current_user_id=user_a.id)
    assert_equal(deleted, {"status": "deleted"}, "软删除返回值不正确")

    expect_value_error(
        lambda: kb_service_get(session, kb_a1.id, current_user_id=user_a.id),
        "知识库不存在",
    )

    after_delete_page = kb_service_list(session, current_user_id=user_a.id, page=1, page_size=10)
    assert_equal(after_delete_page.total, 2, "软删除后 total 应该减少")
    assert_equal(
        [item.name for item in after_delete_page.items],
        ["job-kb", "empty-desc-kb"],
        "软删除后列表不应该包含已删除知识库",
    )

    expect_value_error(
        lambda: kb_service_delete(session, kb_b1.id, current_user_id=user_a.id),
        "不能删除别人的知识库",
    )


def check_service_flow() -> None:
    with make_session() as session:
        user_a, user_b = check_user_create(session)
        kb_a1, kb_a2, kb_b1 = check_kb_create_and_duplicate(session, user_a, user_b)
        check_kb_list(session, user_a, user_b)
        check_kb_get_update_delete(session, user_a, user_b, kb_a1, kb_a2, kb_b1)


def run_named_check(name: str, func: Callable[[], None]) -> None:
    print(f"检查：{name}")
    try:
        func()
    except NotImplementedError:
        print(f"未完成：{name}")
        print("原因：还有函数保留了 raise NotImplementedError")
        raise
    except Exception:
        print(f"失败：{name}")
        raise
    print(f"通过：{name}")


def main() -> None:
    checks: list[tuple[str, Callable[[], None]]] = [
        ("路由和 health", check_routes_and_health),
        ("SQLAlchemy model 结构", check_models),
        ("service + repository 核心业务流", check_service_flow),
    ]

    try:
        for name, func in checks:
            run_named_check(name, func)
    except Exception as exc:
        print("")
        print("阶段 4 主体实现检查未通过")
        print(f"错误类型：{type(exc).__name__}")
        print(f"错误信息：{exc}")
        print("")
        print("详细 traceback：")
        traceback.print_exc(file=sys.stdout)
        raise SystemExit(1) from exc

    print("")
    print("100分：阶段 4 主体实现检查全部通过")


if __name__ == "__main__":
    main()
