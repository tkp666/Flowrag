from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import KnowledgeBaseModel, UserModel


def user_repository_create(session: Session, email: str, username: str) -> UserModel:
    """
    TODO:
    创建用户并返回 UserModel。

    要求：
    - 创建 UserModel(email=email, username=username)
    - session.add(...)
    - session.commit()
    - session.refresh(...)
    - return user
    """
    user = UserModel(email=email, username=username)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def user_repository_get(session: Session, user_id: int) -> UserModel | None:
    """
    TODO:
    按主键查询用户。

    要求：
    - 使用 session.get(UserModel, user_id)
    """
    return session.get(UserModel, user_id)


def kb_repository_find_active_by_name(
    session: Session,
    user_id: int,
    name: str,
) -> KnowledgeBaseModel | None:
    """
    TODO:
    查询某个用户下同名、未删除的知识库。

    要求：
    - select(KnowledgeBaseModel).where(...)
    - 条件包括 user_id、name、is_deleted == False
    - 返回第一条或 None
    """
    stmt = select(KnowledgeBaseModel).where(
        KnowledgeBaseModel.user_id == user_id,
        KnowledgeBaseModel.name == name,
        KnowledgeBaseModel.is_deleted == False,
    )
    return session.scalars(stmt).first()


def kb_repository_insert(
    session: Session,
    user_id: int,
    name: str,
    description: str | None,
) -> KnowledgeBaseModel:
    """
    TODO:
    创建知识库并返回 KnowledgeBaseModel。

    要求：
    - user_id 来自参数
    - is_deleted 默认 False
    - add / commit / refresh
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


def kb_repository_get(session: Session, kb_id: int) -> KnowledgeBaseModel | None:
    """
    TODO:
    按主键查询知识库。

    要求：
    - 使用 session.get(KnowledgeBaseModel, kb_id)
    """
    return session.get(KnowledgeBaseModel, kb_id)


def kb_repository_list_active_by_user(
    session: Session,
    user_id: int,
    page: int,
    page_size: int,
) -> list[KnowledgeBaseModel]:
    """
    TODO:
    分页查询某个用户未删除知识库。

    要求：
    - offset = (page - 1) * page_size
    - 过滤 user_id 和 is_deleted == False
    - 按 id 升序排序
    - offset / limit
    - session.scalars(stmt).all()
    """
    stmt = (
        select(KnowledgeBaseModel)
        .where(
            KnowledgeBaseModel.user_id == user_id,
            KnowledgeBaseModel.is_deleted == False,
        )
        .order_by(KnowledgeBaseModel.id.asc())
        .offset((page-1) * page_size)
        .limit(page_size)
    )
    return session.scalars(stmt).all()
    
    


def kb_repository_count_active_by_user(session: Session, user_id: int) -> int:
    """
    TODO:
    统计某个用户未删除知识库数量。

    要求：
    - select(func.count()).select_from(KnowledgeBaseModel).where(...)
    - 使用 session.scalar(...)
    - 返回 int
    """
    stmt = (
        select(func.count())
        .select_from(KnowledgeBaseModel)
        .where(
            KnowledgeBaseModel.user_id == user_id,
            KnowledgeBaseModel.is_deleted == False,
        )
    )
    return session.scalar(stmt)


def kb_repository_update(
    session: Session,
    kb: KnowledgeBaseModel,
    name: str | None,
    description: str | None,
) -> KnowledgeBaseModel:
    """
    TODO:
    更新知识库名称和描述。

    要求：
    - name 不是 None 时更新 kb.name
    - description 不是 None 时更新 kb.description
    - commit / refresh
    - return kb
    """
    if name is None and description is None:
        return kb
    if name is not None:
        kb.name = name
    if description is not None:
        kb.description = description
    session.commit()
    session.refresh(kb)
    return kb
    


def kb_repository_soft_delete(session: Session, kb: KnowledgeBaseModel) -> KnowledgeBaseModel:
    """
    TODO:
    软删除知识库。

    要求：
    - 设置 kb.is_deleted = True
    - commit / refresh
    - return kb
    """
    kb.is_deleted = True
    session.commit()
    session.refresh(kb)
    return kb
