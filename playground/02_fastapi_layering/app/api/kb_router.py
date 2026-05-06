from fastapi import APIRouter

from app.schemas.kb import KBCreate, KBListItem, KBResponse
from app.services.kb_service import (
    kb_service_create,
    kb_service_delete,
    kb_service_get,
    kb_service_list,
)


router = APIRouter(prefix="/knowledge-bases", tags=["knowledge-bases"])


@router.post("", response_model=KBResponse)
def create_kb(payload: KBCreate) -> KBResponse:
    """
    这是 router 层：
    - 接收 request body
    - 调用 service
    - 不直接操作底层存储
    """
    return kb_service_create(payload)


@router.get("", response_model=list[KBListItem])
def list_kbs() -> list[KBListItem]:
    """
    这是 router 层：
    - 负责列表接口入口
    - 不直接碰 repository
    """
    return kb_service_list()


@router.get("/{kb_id}", response_model=KBResponse)
def get_kb(kb_id: int) -> KBResponse:
    """
    这是 router 层：
    - 接收 path parameter
    - 调用 service
    """
    return kb_service_get(kb_id)


@router.delete("/{kb_id}")
def delete_kb(kb_id: int) -> dict:
    """
    这是 router 层：
    - 调用 service 执行软删除
    - 返回一个简单成功结果
    """
    if kb_service_delete(kb_id) is True:
        return {"status": "deleted"}
