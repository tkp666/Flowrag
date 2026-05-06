"""
阶段 4 第 3 小节动手题：session 和最小 CRUD 流程。

这道题使用 SQLite 内存数据库来练 SQLAlchemy 的 session / add / commit / refresh / get / select。
当前重点是 CRUD 写法，不是数据库部署。

运行方式：
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/homework/section_03_session_crud.py

目标输出：
section 03 session crud homework looks good
"""

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


class KnowledgeBaseModel(Base):
    __tablename__ = "knowledge_bases"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_kb_user_id_name"),
    )


def create_user(session: Session, email: str, username: str) -> UserModel:
    """
    TODO:
    创建一个用户。

    要求：
    - 创建 UserModel 对象
    - email 和 username 都来自参数，不要写死
    - session.add(...)
    - session.commit()
    - session.refresh(...)
    - 返回 user 对象
    """
    user = UserModel(
        email=email,
        username=username,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user_username(
    session: Session,
    user_id: int,
    new_username: str,
) -> UserModel | None:
    """
    TODO:
    修改某个用户的用户名。

    要求：
    - 使用 session.get(UserModel, user_id) 按主键查用户
    - 如果用户不存在，返回 None
    - 修改 user.username
    - session.commit()
    - session.refresh(user)
    - 返回 user
    """
    user = session.get(UserModel, user_id)
    if user is None:
        return None
    user.username = new_username
    session.commit()
    session.refresh(user)
    return user


def create_kb(
    session: Session,
    user_id: int,
    name: str,
    description: str | None,
) -> KnowledgeBaseModel:
    """
    TODO:
    创建一个知识库。

    要求：
    - user_id 来自参数，不要写死
    - is_deleted 默认为 False
    - add / commit / refresh
    - 返回 kb 对象
    """
    kb = KnowledgeBaseModel(
        user_id=user_id,
        name=name,
        description=description,
    )
    session.add(kb)
    session.commit()
    session.refresh(kb)
    return kb


def get_kb_by_id(session: Session, kb_id: int) -> KnowledgeBaseModel | None:
    """
    TODO:
    按主键 id 查询知识库。

    要求：
    - 使用 session.get(...)
    """
    return session.get(KnowledgeBaseModel, kb_id)


def list_active_kbs_by_user(session: Session, user_id: int) -> list[KnowledgeBaseModel]:
    """
    TODO:
    查询某个用户未删除的知识库列表。

    要求：
    - 使用 select(KnowledgeBaseModel).where(...)
    - 条件包括：
      1. KnowledgeBaseModel.user_id == user_id
      2. KnowledgeBaseModel.is_deleted == False
    - 使用 session.scalars(stmt).all()
    """
    stmt = select(KnowledgeBaseModel).where(
        KnowledgeBaseModel.user_id == user_id,
        KnowledgeBaseModel.is_deleted == False,
    )
    return session.scalars(stmt).all()


def update_kb_name(
    session: Session,
    kb_id: int,
    current_user_id: int,
    new_name: str,
) -> KnowledgeBaseModel | None:
    """
    TODO:
    修改当前用户自己的知识库名称。

    要求：
    - 先按 id 查知识库
    - 如果不存在，返回 None
    - 如果 kb.user_id != current_user_id，抛出 ValueError("不能修改别人的知识库")
    - 修改 kb.name
    - commit / refresh
    - 返回 kb
    """
    kb = session.get(KnowledgeBaseModel, kb_id)
    if kb is None:
        return None
    if kb.user_id != current_user_id:
        raise ValueError("不能修改别人的知识库")
    kb.name = new_name
    session.commit()
    session.refresh(kb)
    return kb


def soft_delete_kb(
    session: Session,
    kb_id: int,
    current_user_id: int,
) -> KnowledgeBaseModel | None:
    """
    TODO:
    软删除当前用户自己的知识库。

    要求：
    - 先按 id 查知识库
    - 如果不存在，返回 None
    - 如果 kb.user_id != current_user_id，抛出 ValueError("不能删除别人的知识库")
    - 设置 kb.is_deleted = True
    - commit / refresh
    - 返回 kb
    """
    kb = session.get(KnowledgeBaseModel, kb_id)
    if kb is None:
        return None
    if kb.user_id != current_user_id:
        raise ValueError("不能删除别人的知识库")
    kb.is_deleted = True
    session.commit()
    session.refresh(kb)
    return kb


def check_homework() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        user_a = create_user(session, "a@example.com", "alice")
        user_b = create_user(session, "b@example.com", "bob")

        assert user_a.id is not None, "commit / refresh 后 user_a.id 应该存在"
        assert user_b.id is not None, "commit / refresh 后 user_b.id 应该存在"
        assert user_a.id != user_b.id, "两个用户的主键 id 不应该相同"
        assert user_a.username == "alice", "user_a.username 应该来自 create_user 参数"
        assert user_b.username == "bob", "user_b.username 应该来自 create_user 参数"

        updated_user = update_user_username(session, user_a.id, "alice_new")
        assert updated_user is not None, "更新存在的用户应该返回对象"
        assert updated_user.username == "alice_new", "用户名应该被更新"

        fetched_user = session.get(UserModel, user_a.id)
        assert fetched_user is not None, "更新后应该仍然能查到 user_a"
        assert fetched_user.username == "alice_new", "数据库里的用户名也应该更新"

        missing_user = update_user_username(session, 999999, "ghost")
        assert missing_user is None, "更新不存在的用户应该返回 None"

        kb_a1 = create_kb(session, user_a.id, "paper-kb", "论文知识库")
        kb_a2 = create_kb(session, user_a.id, "interview-kb", "面试知识库")
        kb_b1 = create_kb(session, user_b.id, "paper-kb", "另一个用户的同名知识库")

        assert kb_a1.id is not None, "commit / refresh 后 kb_a1.id 应该存在"
        assert kb_a1.user_id == user_a.id, "kb_a1 应该属于 user_a"
        assert kb_b1.user_id == user_b.id, "kb_b1 应该属于 user_b"
        assert kb_a1.is_deleted is False, "新建知识库默认不应该删除"

        fetched = get_kb_by_id(session, kb_a1.id)
        assert fetched is not None, "按 id 应该能查到 kb_a1"
        assert fetched.name == "paper-kb", "按 id 查询结果名称不正确"

        active_a = list_active_kbs_by_user(session, user_a.id)
        assert [item.name for item in active_a] == ["paper-kb", "interview-kb"], "user_a 应该有两个未删除知识库"

        updated = update_kb_name(session, kb_a2.id, user_a.id, "job-kb")
        assert updated is not None, "更新存在的知识库应该返回对象"
        assert updated.name == "job-kb", "知识库名称应该被更新"

        try:
            update_kb_name(session, kb_b1.id, user_a.id, "wrong-update")
        except ValueError as exc:
            assert str(exc) == "不能修改别人的知识库"
        else:
            raise AssertionError("不应该允许修改别人的知识库")

        deleted = soft_delete_kb(session, kb_a1.id, user_a.id)
        assert deleted is not None, "软删除存在的知识库应该返回对象"
        assert deleted.is_deleted is True, "软删除后 is_deleted 应该是 True"

        active_a_after_delete = list_active_kbs_by_user(session, user_a.id)
        assert [item.name for item in active_a_after_delete] == ["job-kb"], "软删除后列表不应该返回已删除知识库"

        try:
            soft_delete_kb(session, kb_b1.id, user_a.id)
        except ValueError as exc:
            assert str(exc) == "不能删除别人的知识库"
        else:
            raise AssertionError("不应该允许删除别人的知识库")

    print("section 03 session crud homework looks good")


if __name__ == "__main__":
    check_homework()
