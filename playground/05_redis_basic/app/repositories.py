from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import KnowledgeBaseModel


def kb_repository_seed(session: Session) -> list[KnowledgeBaseModel]:
    """
    创建主体实现演示数据。

    这里为了方便重复运行 /dev/seed，先删除旧的演示数据。
    正式项目不会这样清表；正式项目会有正常创建接口和权限控制。
    """
    session.execute(delete(KnowledgeBaseModel))
    session.commit()

    records = [
        KnowledgeBaseModel(
            owner_id=1,
            name="paper-kb",
            description="论文阅读知识库",
            document_count=3,
        ),
        KnowledgeBaseModel(
            owner_id=1,
            name="interview-kb",
            description="后端面试知识库",
            document_count=5,
        ),
        KnowledgeBaseModel(
            owner_id=2,
            name="private-kb",
            description="另一个用户的知识库",
            document_count=1,
        ),
    ]
    session.add_all(records)
    session.commit()
    for record in records:
        session.refresh(record)
    return records


def kb_repository_get_active_by_id(
    session: Session,
    kb_id: int,
) -> KnowledgeBaseModel | None:
    """
    按 id 查询未删除知识库。

    要求：
    - 使用 select(KnowledgeBaseModel).where(...)
    - 条件包括 id == kb_id 和 is_deleted == False
    - 返回第一条或 None
    """
    stmt = select(KnowledgeBaseModel).where(
        KnowledgeBaseModel.id == kb_id,
        KnowledgeBaseModel.is_deleted == False,
    )
    return session.scalars(stmt).first()


def kb_repository_update(
    session: Session,
    kb: KnowledgeBaseModel,
    name: str | None,
    description: str | None,
) -> KnowledgeBaseModel:
    """
    更新知识库名称和描述。

    要求：
    - name 不是 None 时更新 kb.name
    - description 不是 None 时更新 kb.description
    - commit / refresh
    - return kb
    """
    if name is not None:
        kb.name = name
    if description is not None:
        kb.description = description
    session.commit()
    session.refresh(kb)
    return kb
    
