"""
阶段 4 第 2 小节补充动手题：真正使用 SQLAlchemy model 区分数据库结构和 API schema。

这道题会用到 SQLAlchemy 2.x 的基础写法，但暂时不连接 MySQL。
你现在只需要定义“表结构映射”，并把内部 model 转成 API 响应 schema。

运行方式：
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/homework/section_02b_sqlalchemy_model_schema.py

目标输出：
section 02b sqlalchemy model schema homework looks good
"""

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    """
    TODO:
    这是 SQLAlchemy model，对应 users 表。

    要求：
    - 表名是 users
    - id 是主键
    - email 是字符串，最大长度 255，不能为空，并且唯一
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)


class KnowledgeBaseModel(Base):
    """
    TODO:
    这是 SQLAlchemy model，对应 knowledge_bases 表。

    要求：
    - 表名是 knowledge_bases
    - id 是主键
    - user_id 是外键，指向 users.id，不能为空，并且需要普通索引
    - name 是字符串，最大长度 100，不能为空
    - description 是字符串，最大长度 255，可以为空
    - is_deleted 是布尔值，不能为空，默认值是 False
    - 同一个 user_id 下 name 不能重复，所以要加联合唯一约束

    提示：
    - 外键写法：mapped_column(ForeignKey("users.id"), ...)
    - 普通索引写法：index=True
    - 联合唯一约束写在 __table_args__
    """

    __tablename__ = "knowledge_bases"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_kb_user_id_name"),
    )


class KBCreateSchema(BaseModel):
    """
    TODO:
    这是 API 请求 schema，不是数据库 model。

    创建知识库时，用户只允许传：
    - name
    - description

    注意：
    - 不要让用户传 id
    - 不要让用户传 user_id
    - 不要让用户传 is_deleted
    """
    name: str
    description: str | None = None
    


class KBResponseSchema(BaseModel):
    """
    TODO:
    这是 API 响应 schema，不是数据库 model。

    普通知识库详情响应只返回：
    - id
    - name
    - description

    注意：
    - 不要返回 user_id
    - 不要返回 is_deleted
    """
    id: int
    name: str
    description: str | None = None


def build_response_from_model(model: KnowledgeBaseModel) -> KBResponseSchema:
    """
    TODO:
    把 SQLAlchemy model 对象转成 API 响应 schema。

    要求：
    - 返回 KBResponseSchema
    - 只带 id、name、description
    - 不要暴露 user_id、is_deleted
    """
    return KBResponseSchema(
        id=model.id,
        name=model.name,
        description=model.description,
    )


def check_homework() -> None:
    user_table = UserModel.__table__
    kb_table = KnowledgeBaseModel.__table__

    assert UserModel.__tablename__ == "users", "UserModel 表名应该是 users"
    assert user_table.c.id.primary_key is True, "users.id 应该是主键"
    assert user_table.c.email.type.length == 255, "users.email 长度应该是 255"
    assert user_table.c.email.nullable is False, "users.email 不应该允许为空"
    assert user_table.c.email.unique is True, "users.email 应该唯一"

    assert KnowledgeBaseModel.__tablename__ == "knowledge_bases", "KnowledgeBaseModel 表名应该是 knowledge_bases"
    assert kb_table.c.id.primary_key is True, "knowledge_bases.id 应该是主键"
    assert kb_table.c.user_id.nullable is False, "knowledge_bases.user_id 不应该允许为空"
    assert kb_table.c.user_id.index is True, "knowledge_bases.user_id 应该建普通索引"

    foreign_keys = list(kb_table.c.user_id.foreign_keys)
    assert len(foreign_keys) == 1, "knowledge_bases.user_id 应该有一个外键"
    assert foreign_keys[0].target_fullname == "users.id", "knowledge_bases.user_id 应该指向 users.id"

    assert kb_table.c.name.type.length == 100, "knowledge_bases.name 长度应该是 100"
    assert kb_table.c.name.nullable is False, "knowledge_bases.name 不应该允许为空"
    assert kb_table.c.description.type.length == 255, "knowledge_bases.description 长度应该是 255"
    assert kb_table.c.description.nullable is True, "knowledge_bases.description 应该允许为空"
    assert kb_table.c.is_deleted.nullable is False, "knowledge_bases.is_deleted 不应该允许为空"
    assert kb_table.c.is_deleted.default.arg is False, "knowledge_bases.is_deleted 默认值应该是 False"

    unique_constraints = [
        constraint
        for constraint in kb_table.constraints
        if isinstance(constraint, UniqueConstraint)
    ]
    assert any(
        set(constraint.columns.keys()) == {"user_id", "name"}
        for constraint in unique_constraints
    ), "knowledge_bases 应该有 user_id + name 的联合唯一约束"

    payload = KBCreateSchema(name="paper-kb", description="论文知识库")
    assert payload.name == "paper-kb", "KBCreateSchema 应该接收 name"
    assert payload.description == "论文知识库", "KBCreateSchema 应该接收 description"
    assert not hasattr(payload, "user_id"), "KBCreateSchema 不应该包含 user_id"
    assert not hasattr(payload, "is_deleted"), "KBCreateSchema 不应该包含 is_deleted"

    model = KnowledgeBaseModel(
        id=1,
        user_id=1001,
        name=payload.name,
        description=payload.description,
        is_deleted=False,
    )
    response = build_response_from_model(model)

    assert isinstance(response, KBResponseSchema), "build_response_from_model 必须返回 KBResponseSchema"
    assert response.id == 1, "响应里应该有 id"
    assert response.name == "paper-kb", "响应里应该有 name"
    assert response.description == "论文知识库", "响应里应该有 description"
    assert not hasattr(response, "user_id"), "KBResponseSchema 不应该暴露 user_id"
    assert not hasattr(response, "is_deleted"), "KBResponseSchema 不应该暴露 is_deleted"

    print("section 02b sqlalchemy model schema homework looks good")


if __name__ == "__main__":
    check_homework()
