"""
阶段 4 主体实现详细检查脚本。

这个脚本比 check_stage4.py 更细：
- 检查 model / schema / route 结构
- 直接检查 service + repository 业务流
- 直接调用 router 函数检查 HTTPException 状态码映射和响应体
- 额外探测软删除后的同名重建策略

运行方式：
cd /home/tkp666/FlowRAG/playground/04_mysql_sqlalchemy
/home/tkp666/miniconda3/envs/flowrag/bin/python check_stage4_detailed.py

通过时输出：
100分：阶段 4 详细检查全部通过
"""

from collections.abc import Callable, Generator
import sys
import traceback

from fastapi import HTTPException
from sqlalchemy import UniqueConstraint, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import models  # noqa: F401
from app.db import Base
from app.main import app
from app.models import KnowledgeBaseModel, UserModel
from app.routers import (
    create_kb as route_create_kb,
    create_user as route_create_user,
    delete_kb as route_delete_kb,
    get_kb as route_get_kb,
    list_kbs as route_list_kbs,
    update_kb as route_update_kb,
)
from app.schemas import KBCreate, KBPageResponse, KBResponse, KBUpdate, UserCreate, UserResponse
from app.services import (
    kb_service_create,
    kb_service_delete,
    kb_service_get,
    kb_service_list,
    kb_service_update,
    user_service_create,
)


class DetailedCheckError(AssertionError):
    pass


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise DetailedCheckError(message)


def assert_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise DetailedCheckError(f"{message}：实际={actual!r}，期望={expected!r}")


def assert_not_in(key: str, data: dict, message: str) -> None:
    if key in data:
        raise DetailedCheckError(f"{message}：不应该包含字段 {key!r}，实际响应={data!r}")


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return SessionLocal()


def expect_value_error(func: Callable[[], object], expected_message: str) -> None:
    try:
        func()
    except ValueError as exc:
        assert_equal(str(exc), expected_message, "ValueError 文案不正确")
        return
    raise DetailedCheckError(f"应该抛出 ValueError({expected_message!r})，但没有抛出")


def expect_http_error(func: Callable[[], object], expected_status_code: int, expected_detail: str) -> None:
    try:
        func()
    except HTTPException as exc:
        assert_equal(exc.status_code, expected_status_code, "HTTPException 状态码不正确")
        assert_equal(exc.detail, expected_detail, "HTTPException detail 不正确")
        return
    raise DetailedCheckError(f"应该抛出 HTTPException({expected_status_code}, {expected_detail!r})，但没有抛出")


def check_structure() -> None:
    paths = {route.path for route in app.routes}
    for path in ["/health", "/users", "/knowledge-bases", "/knowledge-bases/{kb_id}"]:
        assert_true(path in paths, f"缺少路由 {path}")

    user_table = UserModel.__table__
    kb_table = KnowledgeBaseModel.__table__

    assert_true(user_table.c.id.primary_key, "users.id 应该是主键")
    assert_true(user_table.c.email.unique is True, "users.email 应该唯一")
    assert_true(user_table.c.username.unique is True, "users.username 应该唯一")

    assert_true(kb_table.c.id.primary_key, "knowledge_bases.id 应该是主键")
    assert_true(kb_table.c.user_id.index is True, "knowledge_bases.user_id 应该建索引")
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
        "knowledge_bases 应该有 user_id + name 联合唯一约束",
    )


def check_service_required_flow() -> None:
    with make_session() as session:
        user_a = user_service_create(session, UserCreate(email="a@example.com", username="alice"))
        user_b = user_service_create(session, UserCreate(email="b@example.com", username="bob"))

        assert_true(isinstance(user_a, UserResponse), "创建用户应该返回 UserResponse")
        assert_equal(user_a.username, "alice", "用户 username 不正确")

        kb_a1 = kb_service_create(session, KBCreate(name="paper-kb", description="论文知识库"), user_a.id)
        kb_a2 = kb_service_create(session, KBCreate(name="interview-kb", description=None), user_a.id)
        kb_b1 = kb_service_create(session, KBCreate(name="paper-kb", description="另一个用户同名"), user_b.id)

        assert_true(isinstance(kb_a1, KBResponse), "创建知识库应该返回 KBResponse")
        assert_equal(kb_a1.name, "paper-kb", "知识库名称不正确")
        expect_value_error(
            lambda: kb_service_create(session, KBCreate(name="paper-kb", description=None), user_a.id),
            "知识库名称已存在",
        )

        page_1 = kb_service_list(session, user_a.id, page=1, page_size=1)
        page_2 = kb_service_list(session, user_a.id, page=2, page_size=1)
        assert_true(isinstance(page_1, KBPageResponse), "列表应该返回 KBPageResponse")
        assert_equal(page_1.total, 2, "分页 total 不正确")
        assert_equal([item.name for item in page_1.items], ["paper-kb"], "第一页 items 不正确")
        assert_equal([item.name for item in page_2.items], ["interview-kb"], "第二页 items 不正确")

        fetched = kb_service_get(session, kb_a1.id, user_a.id)
        assert_equal(fetched.id, kb_a1.id, "详情 id 不正确")
        expect_value_error(lambda: kb_service_get(session, kb_b1.id, user_a.id), "不能访问别人的知识库")

        updated = kb_service_update(
            session,
            kb_a2.id,
            KBUpdate(name="job-kb", description="求职知识库"),
            user_a.id,
        )
        assert_equal(updated.id, kb_a2.id, "更新不应该改变 id")
        assert_equal(updated.name, "job-kb", "更新 name 不正确")
        assert_equal(updated.description, "求职知识库", "更新 description 不正确")

        desc_only = kb_service_create(session, KBCreate(name="empty-desc-kb", description=None), user_a.id)
        desc_updated = kb_service_update(
            session,
            desc_only.id,
            KBUpdate(name=None, description="补充描述"),
            user_a.id,
        )
        assert_equal(desc_updated.id, desc_only.id, "只更新 description 不应该改变 id")
        assert_equal(desc_updated.name, "empty-desc-kb", "只更新 description 不应该改变 name")
        assert_equal(desc_updated.description, "补充描述", "只更新 description 没有生效")

        same_name = kb_service_update(
            session,
            desc_only.id,
            KBUpdate(name="empty-desc-kb", description=None),
            user_a.id,
        )
        assert_equal(same_name.id, desc_only.id, "把知识库更新为自己的原名称不应该失败")
        assert_equal(same_name.name, "empty-desc-kb", "把知识库更新为自己的原名称后 name 不正确")

        expect_value_error(
            lambda: kb_service_update(session, desc_only.id, KBUpdate(name="paper-kb", description=None), user_a.id),
            "知识库名称已存在",
        )
        expect_value_error(
            lambda: kb_service_update(session, kb_b1.id, KBUpdate(name="wrong", description=None), user_a.id),
            "不能修改别人的知识库",
        )

        deleted = kb_service_delete(session, kb_a1.id, user_a.id)
        assert_equal(deleted, {"status": "deleted"}, "软删除返回值不正确")
        expect_value_error(lambda: kb_service_get(session, kb_a1.id, user_a.id), "知识库不存在")
        after_delete = kb_service_list(session, user_a.id, page=1, page_size=10)
        assert_equal([item.name for item in after_delete.items], ["job-kb", "empty-desc-kb"], "软删除后列表不正确")


def check_router_flow() -> None:
    with make_session() as session:
        user_a = route_create_user(UserCreate(email="a@example.com", username="alice"), db=session)
        user_b = route_create_user(UserCreate(email="b@example.com", username="bob"), db=session)
        assert_true(isinstance(user_a, UserResponse), "POST /users 应该返回 UserResponse")
        assert_not_in("password_hash", user_a.model_dump(), "用户响应不应该暴露密码字段")

        expect_http_error(
            lambda: route_create_kb(KBCreate(name="ghost-kb", description=None), current_user_id=999999, db=session),
            404,
            "用户不存在",
        )

        kb_a1 = route_create_kb(
            KBCreate(name="paper-kb", description="论文知识库"),
            current_user_id=user_a.id,
            db=session,
        )
        kb_a2 = route_create_kb(
            KBCreate(name="interview-kb", description="面试知识库"),
            current_user_id=user_a.id,
            db=session,
        )
        kb_b1 = route_create_kb(
            KBCreate(name="paper-kb", description="另一个用户同名"),
            current_user_id=user_b.id,
            db=session,
        )
        assert_true(isinstance(kb_a1, KBResponse), "POST /knowledge-bases 应该返回 KBResponse")
        assert_not_in("user_id", kb_a1.model_dump(), "知识库响应不应该暴露 user_id")
        assert_not_in("is_deleted", kb_a1.model_dump(), "知识库响应不应该暴露 is_deleted")

        expect_http_error(
            lambda: route_create_kb(KBCreate(name="paper-kb", description="重复"), current_user_id=user_a.id, db=session),
            400,
            "知识库名称已存在",
        )

        page = route_list_kbs(current_user_id=user_a.id, page=1, page_size=1, db=session)
        assert_equal(page.total, 2, "GET /knowledge-bases total 不正确")
        assert_equal([item.name for item in page.items], ["paper-kb"], "GET /knowledge-bases items 不正确")

        detail = route_get_kb(kb_a1.id, current_user_id=user_a.id, db=session)
        assert_equal(detail.id, kb_a1.id, "GET /knowledge-bases/{kb_id} id 不正确")
        expect_http_error(
            lambda: route_get_kb(kb_b1.id, current_user_id=user_a.id, db=session),
            403,
            "不能访问别人的知识库",
        )

        updated = route_update_kb(
            kb_a2.id,
            KBUpdate(name="job-kb", description="求职知识库"),
            current_user_id=user_a.id,
            db=session,
        )
        assert_equal(updated.id, kb_a2.id, "PATCH /knowledge-bases/{kb_id} 不应该改变 id")
        assert_equal(updated.name, "job-kb", "PATCH /knowledge-bases/{kb_id} name 不正确")

        same_name = route_update_kb(
            kb_a2.id,
            KBUpdate(name="job-kb", description=None),
            current_user_id=user_a.id,
            db=session,
        )
        assert_equal(same_name.id, kb_a2.id, "把知识库更新为自己的原名称不应该失败")

        expect_http_error(
            lambda: route_update_kb(kb_b1.id, KBUpdate(name="wrong", description=None), current_user_id=user_a.id, db=session),
            403,
            "不能修改别人的知识库",
        )

        deleted = route_delete_kb(kb_a1.id, current_user_id=user_a.id, db=session)
        assert_equal(deleted, {"status": "deleted"}, "DELETE /knowledge-bases/{kb_id} 响应不正确")
        expect_http_error(
            lambda: route_get_kb(kb_a1.id, current_user_id=user_a.id, db=session),
            404,
            "知识库不存在",
        )


def probe_soft_delete_name_reuse() -> str:
    """
    探测当前产品策略：
    - 如果软删除后允许重建同名知识库，这里应该成功。
    - 如果名称被历史记录永久占用，这里可以失败。

    当前脚本只给出提示，不把它作为 100 分阻断项。
    """
    with make_session() as session:
        user = user_service_create(session, UserCreate(email="reuse@example.com", username="reuse_user"))
        kb = kb_service_create(session, KBCreate(name="reuse-kb", description=None), user.id)
        kb_service_delete(session, kb.id, user.id)
        try:
            recreated = kb_service_create(session, KBCreate(name="reuse-kb", description="重建"), user.id)
        except Exception as exc:
            return (
                "策略提醒：当前软删除后不能重建同名知识库。"
                f"如果你希望只禁止未删除知识库重名，需要调整数据库唯一约束和 service 规则。实际异常：{type(exc).__name__}: {exc}"
            )
        return f"策略提醒：当前软删除后允许重建同名知识库，新 id={recreated.id}"


def run_check(name: str, func: Callable[[], None], failures: list[str]) -> None:
    print(f"检查：{name}")
    try:
        func()
    except Exception as exc:
        print(f"失败：{name}")
        print(f"错误类型：{type(exc).__name__}")
        print(f"错误信息：{exc}")
        print("traceback：")
        traceback.print_exc(file=sys.stdout)
        failures.append(name)
        return
    print(f"通过：{name}")


def main() -> None:
    failures: list[str] = []
    checks: list[tuple[str, Callable[[], None]]] = [
        ("结构检查", check_structure),
        ("service/repository 细粒度业务流", check_service_required_flow),
        ("router 状态码映射和响应体", check_router_flow),
    ]

    for name, func in checks:
        run_check(name, func, failures)

    print("")
    print(probe_soft_delete_name_reuse())

    if failures:
        print("")
        print(f"阶段 4 详细检查未通过，失败项：{failures}")
        raise SystemExit(1)

    print("")
    print("100分：阶段 4 详细检查全部通过")


if __name__ == "__main__":
    main()
