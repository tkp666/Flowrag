from app.repositories.kb_repository import (
    kb_repository_find_by_name,
    kb_repository_get,
    kb_repository_insert,
    kb_repository_list,
    kb_repository_soft_delete,
    next_kb_id_ref,
)
from app.schemas.kb import KBCreate, KBListItem, KBResponse


def kb_service_create(payload: KBCreate) -> KBResponse:
    """
    这是 service 层：
    - 做重名检查
    - 生成 id
    - 组装内部 record
    - 调 repository_insert
    - 返回 KBResponse
    """
    if kb_repository_find_by_name(payload.name) is not None:
        raise ValueError("知识库名称已存在")
    current_id = next_kb_id_ref["value"]
    record = {
        "id": current_id,
        "name": payload.name,
        "description": payload.description,
        "owner_id": 1001,
        "is_deleted": False
    }
    kb_repository_insert(record)
    next_kb_id_ref["value"] += 1
    return KBResponse(
        id=current_id,
        name=payload.name,
        description=payload.description
    )


def kb_service_list() -> list[KBListItem]:
    """
    这是 service 层：
    - 取出所有未删除知识库
    - 转成 KBListItem 列表返回
    """
    all_record: list[dict] = []
    all_record = kb_repository_list()
    result:list[KBListItem] = []
    for record in all_record:
        if record["is_deleted"] == False:
            result.append(KBListItem(
                id=record["id"],
                name=record["name"],
                description=record["description"]
            ))
    return result


def kb_service_get(kb_id: int) -> KBResponse:
    """
    这是 service 层：
    - 不存在检查
    - 已删除检查
    - record -> KBResponse
    """
    record = kb_repository_get(kb_id)
    if record is None:
        raise ValueError("知识库不存在")
    if record["is_deleted"] is True:
        raise ValueError("知识库已删除")
    return KBResponse(
        id=record["id"],
        name=record["name"],
        description=record["description"]
    )


def kb_service_delete(kb_id: int) -> bool:
    """
    这是 service 层：
    - 不存在检查
    - 已删除检查
    - 调 repository_soft_delete
    """
    record = kb_repository_get(kb_id)
    if record is None:
        raise ValueError("知识库不存在")
    if record["is_deleted"] is True:
        raise ValueError("知识库已删除")
    kb_repository_soft_delete(kb_id)
    return True
