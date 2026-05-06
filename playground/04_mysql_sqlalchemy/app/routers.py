from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import KBCreate, KBPageResponse, KBResponse, KBUpdate, UserCreate, UserResponse
from app.services import (
    kb_service_create,
    kb_service_delete,
    kb_service_get,
    kb_service_list,
    kb_service_update,
    user_service_create,
)


router = APIRouter()


def _to_http_error(exc: ValueError) -> HTTPException:
    detail = str(exc)
    status_code = 400
    if "不存在" in detail:
        status_code = 404
    if "别人" in detail:
        status_code = 403
    return HTTPException(status_code=status_code, detail=detail)


@router.post("/users", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        return user_service_create(db, payload)
    except ValueError as exc:
        raise _to_http_error(exc) from exc


@router.post("/knowledge-bases", response_model=KBResponse)
def create_kb(
    payload: KBCreate,
    current_user_id: int = Query(1, ge=1),
    db: Session = Depends(get_db),
) -> KBResponse:
    try:
        return kb_service_create(db, payload, current_user_id)
    except ValueError as exc:
        raise _to_http_error(exc) from exc


@router.get("/knowledge-bases", response_model=KBPageResponse)
def list_kbs(
    current_user_id: int = Query(1, ge=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> KBPageResponse:
    try:
        return kb_service_list(db, current_user_id, page, page_size)
    except ValueError as exc:
        raise _to_http_error(exc) from exc


@router.get("/knowledge-bases/{kb_id}", response_model=KBResponse)
def get_kb(
    kb_id: int,
    current_user_id: int = Query(1, ge=1),
    db: Session = Depends(get_db),
) -> KBResponse:
    try:
        return kb_service_get(db, kb_id, current_user_id)
    except ValueError as exc:
        raise _to_http_error(exc) from exc


@router.patch("/knowledge-bases/{kb_id}", response_model=KBResponse)
def update_kb(
    kb_id: int,
    payload: KBUpdate,
    current_user_id: int = Query(1, ge=1),
    db: Session = Depends(get_db),
) -> KBResponse:
    try:
        return kb_service_update(db, kb_id, payload, current_user_id)
    except ValueError as exc:
        raise _to_http_error(exc) from exc


@router.delete("/knowledge-bases/{kb_id}")
def delete_kb(
    kb_id: int,
    current_user_id: int = Query(1, ge=1),
    db: Session = Depends(get_db),
) -> dict:
    try:
        return kb_service_delete(db, kb_id, current_user_id)
    except ValueError as exc:
        raise _to_http_error(exc) from exc
