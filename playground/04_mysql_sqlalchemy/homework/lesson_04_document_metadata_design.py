"""
阶段 4 综合课后动手题：文档元数据表的最小设计。

背景：
FlowRAG 后面会有“上传文档 -> 异步入库 -> 检索问答”的流程。
但在真正进入 Celery / Qdrant 前，文档的业务元数据应该先进入 MySQL。

这道题不是让你重复写 knowledge_base CRUD。
它重点考察：
- 文档属于哪个知识库
- 文档表为什么要有外键和索引
- API schema 为什么不能等于数据库 model
- 列表为什么要分页
- 软删除后列表为什么要过滤

运行方式：
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/homework/lesson_04_document_metadata_design.py

目标输出：
lesson 04 document metadata design homework looks good
"""

from sqlalchemy import Boolean, ForeignKey, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from pydantic import BaseModel, Field


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)


class KnowledgeBaseModel(Base):
    __tablename__ = "knowledge_bases"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class DocumentModel(Base):
    """
    TODO:
    定义 documents 表。

    要求：
    - 表名：documents
    - id：主键
    - kb_id：外键，指向 knowledge_bases.id，不能为空，并且需要普通索引
    - filename：字符串，最大长度 255，不能为空
    - title：字符串，最大长度 100，可以为空
    - ingest_status：字符串，最大长度 30，不能为空，默认值是 "pending"
    - is_deleted：布尔值，不能为空，默认值是 False
    """
    __tablename__ = "documents"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    kb_id: Mapped[int] = mapped_column(ForeignKey("knowledge_bases.id"), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ingest_status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    


class DocumentCreateSchema(BaseModel):
    """
    TODO:
    API 请求 schema。

    用户创建文档元数据时，只允许传：
    - filename
    - title

    注意：
    - 不允许用户在请求体里传 id
    - 不允许用户在请求体里传 kb_id
    - 不允许用户在请求体里传 ingest_status
    - 不允许用户在请求体里传 is_deleted
    """
    filename: str = Field(min_length=1, max_length=255)
    title:str | None = Field(default=None, max_length=100)


class DocumentListItemSchema(BaseModel):
    """
    TODO:
    API 列表项响应 schema。

    列表项只返回：
    - id
    - filename
    - title
    - ingest_status

    注意：
    - 不返回 kb_id
    - 不返回 is_deleted
    """
    id: int 
    filename: str = Field(min_length=1, max_length=255)
    title: str | None = None
    ingest_status: str = Field(min_length=1, max_length=30, default="pending")


def create_kb(session: Session, user_id: int, name: str) -> KnowledgeBaseModel:
    kb = KnowledgeBaseModel(user_id=user_id, name=name, is_deleted=False)
    session.add(kb)
    session.commit()
    session.refresh(kb)
    return kb


def create_document(
    session: Session,
    kb_id: int,
    payload: DocumentCreateSchema,
) -> DocumentModel:
    """
    TODO:
    创建文档元数据。

    要求：
    - 先用 session.get(KnowledgeBaseModel, kb_id) 查询知识库
    - 如果知识库不存在或已软删除，raise ValueError("知识库不存在")
    - DocumentModel.kb_id 来自函数参数，不来自 payload
    - filename/title 来自 payload
    - ingest_status 默认 "pending"
    - is_deleted 默认 False
    - add / commit / refresh
    - 返回 DocumentModel
    """
    record = session.get(KnowledgeBaseModel, kb_id)
    if record is None or record.is_deleted is True:
        raise ValueError("知识库不存在")
    doc = DocumentModel(
        kb_id=kb_id,
        filename=payload.filename,
        title=payload.title,
    )
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc
    


def list_documents_page(
    session: Session,
    kb_id: int,
    page: int,
    page_size: int,
) -> dict:
    """
    TODO:
    分页查询某个知识库下未删除的文档元数据。

    要求：
    - 如果知识库不存在或已软删除，raise ValueError("知识库不存在")
    - 只查 DocumentModel.kb_id == kb_id
    - 只查 DocumentModel.is_deleted == False
    - 按 DocumentModel.id 升序排序
    - 使用 offset / limit
    - total 单独用 select(func.count()).select_from(DocumentModel).where(...)
    - items 转成 DocumentListItemSchema 列表
    - 返回结构：
      {
          "items": items,
          "page": page,
          "page_size": page_size,
          "total": total,
      }
    """
    record = session.get(KnowledgeBaseModel, kb_id)
    if record is None or record.is_deleted == True:
        raise ValueError("知识库不存在")
    stmt_docs = (
        select(DocumentModel)
        .where(
            DocumentModel.kb_id == kb_id,
            DocumentModel.is_deleted == False,
        )
        .order_by(DocumentModel.id.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    stmt_total = select(func.count()).select_from(DocumentModel).where(
        DocumentModel.kb_id == kb_id,
        DocumentModel.is_deleted == False,
    )
    docs = session.scalars(stmt_docs).all()
    total = session.scalar(stmt_total)
    items = [
        DocumentListItemSchema(
            id=doc.id,
            filename=doc.filename,
            title=doc.title,
            ingest_status=doc.ingest_status,
        )
        for doc in docs
    ]
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }
    
        


def soft_delete_document(session: Session, document_id: int) -> DocumentModel | None:
    """
    TODO:
    软删除文档元数据。

    要求：
    - 使用 session.get(DocumentModel, document_id)
    - 如果不存在，返回 None
    - 设置 is_deleted = True
    - commit / refresh
    - 返回 DocumentModel
    """
    record = session.get(DocumentModel, document_id)
    if record is None:
        return None
    record.is_deleted = True
    session.commit()
    session.refresh(record)
    return record


def check_homework() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    doc_table = DocumentModel.__table__
    kb_table = KnowledgeBaseModel.__table__

    kb_foreign_keys = list(kb_table.c.user_id.foreign_keys)
    assert len(kb_foreign_keys) == 1, "knowledge_bases.user_id 应该有一个外键"
    assert kb_foreign_keys[0].target_fullname == "users.id", "knowledge_bases.user_id 应该指向 users.id"

    assert doc_table.c.id.primary_key is True, "documents.id 应该是主键"
    assert doc_table.c.kb_id.nullable is False, "documents.kb_id 不应该允许为空"
    assert doc_table.c.kb_id.index is True, "documents.kb_id 应该建索引"
    foreign_keys = list(doc_table.c.kb_id.foreign_keys)
    assert len(foreign_keys) == 1, "documents.kb_id 应该有一个外键"
    assert foreign_keys[0].target_fullname == "knowledge_bases.id", "documents.kb_id 应该指向 knowledge_bases.id"
    assert doc_table.c.filename.type.length == 255, "documents.filename 长度应该是 255"
    assert doc_table.c.filename.nullable is False, "documents.filename 不应该允许为空"
    assert doc_table.c.title.type.length == 100, "documents.title 长度应该是 100"
    assert doc_table.c.title.nullable is True, "documents.title 应该允许为空"
    assert doc_table.c.ingest_status.default.arg == "pending", "documents.ingest_status 默认值应该是 pending"
    assert doc_table.c.is_deleted.default.arg is False, "documents.is_deleted 默认值应该是 False"

    with SessionLocal() as session:
        user = UserModel(email="a@example.com")
        session.add(user)
        session.commit()
        session.refresh(user)

        kb = create_kb(session, user_id=user.id, name="paper-kb")
        deleted_kb = create_kb(session, user_id=user.id, name="deleted-kb")
        deleted_kb.is_deleted = True
        session.commit()

        doc_1 = create_document(
            session,
            kb.id,
            DocumentCreateSchema(filename="paper-1.pdf", title="第一篇论文"),
        )
        doc_2 = create_document(
            session,
            kb.id,
            DocumentCreateSchema(filename="paper-2.pdf", title=None),
        )
        doc_3 = create_document(
            session,
            kb.id,
            DocumentCreateSchema(filename="paper-3.pdf", title="第三篇论文"),
        )

        assert doc_1.id is not None, "文档插入后应该有 id"
        assert doc_1.kb_id == kb.id, "DocumentModel.kb_id 应该来自函数参数"
        assert doc_1.filename == "paper-1.pdf"
        assert doc_1.title == "第一篇论文"
        assert doc_1.ingest_status == "pending"
        assert doc_1.is_deleted is False

        assert not hasattr(DocumentCreateSchema(filename="x.pdf", title=None), "kb_id"), "DocumentCreateSchema 不应该包含 kb_id"
        assert not hasattr(DocumentCreateSchema(filename="x.pdf", title=None), "ingest_status"), "DocumentCreateSchema 不应该包含 ingest_status"

        page_1 = list_documents_page(session, kb.id, page=1, page_size=2)
        assert page_1["page"] == 1
        assert page_1["page_size"] == 2
        assert page_1["total"] == 3
        assert [item.filename for item in page_1["items"]] == ["paper-1.pdf", "paper-2.pdf"]
        assert all(isinstance(item, DocumentListItemSchema) for item in page_1["items"])
        assert not hasattr(page_1["items"][0], "kb_id"), "DocumentListItemSchema 不应该暴露 kb_id"
        assert not hasattr(page_1["items"][0], "is_deleted"), "DocumentListItemSchema 不应该暴露 is_deleted"

        page_2 = list_documents_page(session, kb.id, page=2, page_size=2)
        assert page_2["total"] == 3
        assert [item.filename for item in page_2["items"]] == ["paper-3.pdf"]

        deleted_doc = soft_delete_document(session, doc_2.id)
        assert deleted_doc is not None
        assert deleted_doc.is_deleted is True

        page_after_delete = list_documents_page(session, kb.id, page=1, page_size=10)
        assert page_after_delete["total"] == 2
        assert [item.filename for item in page_after_delete["items"]] == ["paper-1.pdf", "paper-3.pdf"]

        missing_doc = soft_delete_document(session, 999999)
        assert missing_doc is None

        try:
            create_document(
                session,
                deleted_kb.id,
                DocumentCreateSchema(filename="bad.pdf", title=None),
            )
        except ValueError as exc:
            assert str(exc) == "知识库不存在"
        else:
            raise AssertionError("不应该允许给已删除知识库创建文档")

        try:
            list_documents_page(session, 999999, page=1, page_size=10)
        except ValueError as exc:
            assert str(exc) == "知识库不存在"
        else:
            raise AssertionError("不存在的知识库不应该能查询文档列表")

    print("lesson 04 document metadata design homework looks good")


if __name__ == "__main__":
    check_homework()
