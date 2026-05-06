"""
阶段 4 第 4 小节动手题：分页查询 limit / offset / order_by / total。

这道题继续使用 SQLite 内存数据库来练 SQLAlchemy 分页查询。
重点：
- page / page_size 转 offset
- order_by 保证分页顺序稳定
- items 查询当前页数据
- total 查询符合条件的总数

运行方式：
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/homework/section_04_pagination.py

目标输出：
section 04 pagination homework looks good
"""

from sqlalchemy import Boolean, ForeignKey, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class KnowledgeBaseModel(Base):
    __tablename__ = "knowledge_bases"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)


def seed_data(session: Session) -> tuple[int, int]:
    user_a = UserModel(email="a@example.com")
    user_b = UserModel(email="b@example.com")
    session.add(user_a)
    session.add(user_b)
    session.commit()
    session.refresh(user_a)
    session.refresh(user_b)

    for index in range(1, 8):
        session.add(
            KnowledgeBaseModel(
                user_id=user_a.id,
                name=f"user-a-kb-{index}",
                description=f"user a kb {index}",
                is_deleted=(index == 3),
            )
        )

    for index in range(1, 4):
        session.add(
            KnowledgeBaseModel(
                user_id=user_b.id,
                name=f"user-b-kb-{index}",
                description=f"user b kb {index}",
                is_deleted=False,
            )
        )

    session.commit()
    return user_a.id, user_b.id


def calculate_offset(page: int, page_size: int) -> int:
    """
    TODO:
    根据 page 和 page_size 计算 offset。

    要求：
    - page 从 1 开始
    - page=1,page_size=2 -> offset=0
    - page=2,page_size=2 -> offset=2
    - page=3,page_size=2 -> offset=4
    """
    return (page - 1) * page_size


def list_kbs_page(
    session: Session,
    user_id: int,
    page: int,
    page_size: int,
) -> dict:
    """
    TODO:
    查询某个用户未删除知识库的分页结果。

    要求：
    - 只查 KnowledgeBaseModel.user_id == user_id
    - 只查 KnowledgeBaseModel.is_deleted == False
    - items 按 KnowledgeBaseModel.id 升序排序
    - items 使用 offset / limit
    - total 用 select(func.count()).select_from(KnowledgeBaseModel).where(...)
    - 返回 dict，结构如下：
      {
          "items": items,
          "page": page,
          "page_size": page_size,
          "total": total,
      }
    """
    stmt_items = (
        select(KnowledgeBaseModel)
        .where(
            KnowledgeBaseModel.user_id == user_id,
            KnowledgeBaseModel.is_deleted == False,
        )
        .order_by(KnowledgeBaseModel.id.asc())
        .offset(calculate_offset(page, page_size))
        .limit(page_size)
    )
    
    stmt_total = select(func.count()).select_from(KnowledgeBaseModel).where(
        KnowledgeBaseModel.user_id == user_id,
        KnowledgeBaseModel.is_deleted == False,
    )
    total = session.scalar(stmt_total)
    items = session.scalars(stmt_items).all()
    return {
          "items": items,
          "page": page,
          "page_size": page_size,
          "total": total,
      }
    


def check_homework() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        user_a_id, user_b_id = seed_data(session)

        assert calculate_offset(page=1, page_size=2) == 0
        assert calculate_offset(page=2, page_size=2) == 2
        assert calculate_offset(page=3, page_size=2) == 4

        page_1 = list_kbs_page(session, user_a_id, page=1, page_size=2)
        assert page_1["page"] == 1
        assert page_1["page_size"] == 2
        assert page_1["total"] == 6, "user_a 有 7 个知识库，但第 3 个被软删除，所以 total 应该是 6"
        assert [item.name for item in page_1["items"]] == ["user-a-kb-1", "user-a-kb-2"]

        page_2 = list_kbs_page(session, user_a_id, page=2, page_size=2)
        assert page_2["total"] == 6
        assert [item.name for item in page_2["items"]] == ["user-a-kb-4", "user-a-kb-5"]

        page_3 = list_kbs_page(session, user_a_id, page=3, page_size=2)
        assert page_3["total"] == 6
        assert [item.name for item in page_3["items"]] == ["user-a-kb-6", "user-a-kb-7"]

        page_empty = list_kbs_page(session, user_a_id, page=4, page_size=2)
        assert page_empty["total"] == 6
        assert page_empty["items"] == []

        user_b_page = list_kbs_page(session, user_b_id, page=1, page_size=10)
        assert user_b_page["total"] == 3
        assert [item.name for item in user_b_page["items"]] == [
            "user-b-kb-1",
            "user-b-kb-2",
            "user-b-kb-3",
        ]

    print("section 04 pagination homework looks good")


if __name__ == "__main__":
    check_homework()
