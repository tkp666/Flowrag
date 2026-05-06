from sqlalchemy.orm import Session

from app.repositories import (
    kb_repository_count_active_by_user,
    kb_repository_find_active_by_name,
    kb_repository_get,
    kb_repository_insert,
    kb_repository_list_active_by_user,
    kb_repository_soft_delete,
    kb_repository_update,
    user_repository_create,
    user_repository_get,
)
from app.schemas import KBCreate, KBPageResponse, KBResponse, KBUpdate, UserCreate, UserResponse


def user_service_create(session: Session, payload: UserCreate) -> UserResponse:
    """
    TODO:
    创建用户。

    这里先不做完整注册系统，只调用 repository 创建用户。
    返回 UserResponse。
    """
    record = user_repository_create(session, payload.email, payload.username)
    return UserResponse(
        id=record.id,
        email=record.email,
        username=record.username,
    )


def kb_service_create(
    session: Session,
    payload: KBCreate,
    current_user_id: int,
) -> KBResponse:
    """
    TODO:
    创建知识库。

    业务规则：
    - current_user_id 必须能查到用户，否则 raise ValueError("用户不存在")
    - 同一用户下不能创建同名未删除知识库，否则 raise ValueError("知识库名称已存在")
    - 调 kb_repository_insert(...)
    - 返回 KBResponse
    """
    if user_repository_get(session, current_user_id) is None:
        raise ValueError("用户不存在")
    if kb_repository_find_active_by_name(session, current_user_id, payload.name) is not None:
        raise ValueError("知识库名称已存在")
    record = kb_repository_insert(session, current_user_id, payload.name, payload.description)
    return KBResponse(
        id=record.id,
        name=record.name,
        description=record.description,
    )
        


def kb_service_get(
    session: Session,
    kb_id: int,
    current_user_id: int,
) -> KBResponse:
    """
    TODO:
    查询知识库详情。

    业务规则：
    - 不存在：raise ValueError("知识库不存在")
    - 已软删除：raise ValueError("知识库不存在")
    - 不属于当前用户：raise ValueError("不能访问别人的知识库")
    - 返回 KBResponse
    """
    record = kb_repository_get(session, kb_id)
    if record is None or record.is_deleted == True :
        raise ValueError("知识库不存在")
    if record.user_id != current_user_id:
        raise ValueError("不能访问别人的知识库")
    return KBResponse(
        id=record.id,
        name=record.name,
        description=record.description,
    )


def kb_service_list(
    session: Session,
    current_user_id: int,
    page: int,
    page_size: int,
) -> KBPageResponse:
    """
    TODO:
    分页查询当前用户的未删除知识库。

    要求：
    - 调 kb_repository_list_active_by_user(...)
    - 调 kb_repository_count_active_by_user(...)
    - 返回 KBPageResponse
    """
    items = kb_repository_list_active_by_user(session, current_user_id, page, page_size)
    total = kb_repository_count_active_by_user(session, current_user_id)
    return KBPageResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
    )
    


def kb_service_update(
    session: Session,
    kb_id: int,
    payload: KBUpdate,
    current_user_id: int,
) -> KBResponse:
    """
    TODO:
    更新当前用户自己的知识库。

    业务规则：
    - 不存在或已删除：raise ValueError("知识库不存在")
    - 不属于当前用户：raise ValueError("不能修改别人的知识库")
    - 如果 payload.name 不是 None，且同名未删除知识库已存在，需要 raise ValueError("知识库名称已存在")
    - 调 kb_repository_update(...)
    - 返回 KBResponse
    """
    kb = kb_repository_get(session, kb_id)
    if kb is None or kb.is_deleted == True:
        raise ValueError("知识库不存在")
    if kb.user_id != current_user_id:
        raise ValueError("不能修改别人的知识库")
    # if payload.name is not None and kb_repository_find_active_by_name(session, current_user_id, payload.name) is not None:
    #     raise ValueError("知识库名称已存在")
    if payload.name is not None:
        existing = kb_repository_find_active_by_name(session, current_user_id, payload.name)
        if existing is not None and existing.id != kb.id:
            raise ValueError("知识库名称已存在")
    record = kb_repository_update(session, kb, payload.name, payload.description)
    return KBResponse(
        id=record.id,
        name=record.name,
        description=record.description,
    )
        
    


def kb_service_delete(
    session: Session,
    kb_id: int,
    current_user_id: int,
) -> dict:
    """
    TODO:
    软删除当前用户自己的知识库。

    业务规则：
    - 不存在或已删除：raise ValueError("知识库不存在")
    - 不属于当前用户：raise ValueError("不能删除别人的知识库")
    - 调 kb_repository_soft_delete(...)
    - 返回 {"status": "deleted"}
    """
    kb = kb_repository_get(session, kb_id)
    if kb is None or kb.is_deleted == True:
        raise ValueError("知识库不存在")
    if kb.user_id != current_user_id:
        raise ValueError("不能删除别人的知识库")
    kb_repository_soft_delete(session, kb)
    return {"status": "deleted"}
