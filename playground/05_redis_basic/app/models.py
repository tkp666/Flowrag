from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class KnowledgeBaseModel(Base):
    __tablename__ = "knowledge_bases"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    document_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
