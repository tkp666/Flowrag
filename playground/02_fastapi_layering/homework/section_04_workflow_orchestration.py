from pydantic import BaseModel


# 这是知识库详情响应体 schema
class KBDetailResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    doc_count: int
    doc_titles_preview: list[str]


# 这是模拟知识库表
fake_kb_table: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "demo-kb",
        "description": "first kb",
        "is_deleted": False,
    },
    2: {
        "id": 2,
        "name": "deleted-kb",
        "description": "already deleted",
        "is_deleted": True,
    },
}


# 这是模拟文档表
fake_doc_table: list[dict] = [
    {"id": 101, "kb_id": 1, "title": "intro.md", "is_deleted": False},
    {"id": 102, "kb_id": 1, "title": "faq.md", "is_deleted": False},
    {"id": 103, "kb_id": 1, "title": "draft.md", "is_deleted": True},
    {"id": 201, "kb_id": 2, "title": "old.md", "is_deleted": False},
]


# 这是 repository 层：查知识库原始 record
def kb_repository_get(kb_id: int) -> dict | None:
    return fake_kb_table.get(kb_id)


# 这是 repository 层：统计某个知识库下未删除文档数量
def doc_repository_count_active_by_kb_id(kb_id: int) -> int:
    count = 0
    for record in fake_doc_table:
        if record["kb_id"] == kb_id and record["is_deleted"] is False:
            count += 1
    return count


# 这是 repository 层：取某个知识库下未删除文档标题预览
def doc_repository_list_active_titles_by_kb_id(kb_id: int, limit: int) -> list[str]:
    titles: list[str] = []
    for record in fake_doc_table:
        if record["kb_id"] == kb_id and record["is_deleted"] is False:
            titles.append(record["title"])
        if len(titles) >= limit:
            break
    return titles


def kb_service_detail_bad(kb_id: int) -> dict | None:
    """
    这是一个坏例子。
    问题：
    1. 它直接返回 repository 的原始 record；
    2. 它没有检查知识库是否已删除；
    3. 它完全没有把“文档数量”和“标题预览”编排进来；
    4. 它没有返回真正面向接口的响应结构。
    """
    return kb_repository_get(kb_id)


# 第 2 阶段 · 第 4 小节动手题：
# 这一题的重点是：让你亲手实现“一个 service 调多个 repository，并把多个步骤编排成一件业务事”。
#
# 你要完成的内容：
# 1. 保留 kb_service_detail_bad，不要删除。
# 2. 在下面补 1 个函数：
#    - kb_service_detail
# 3. 要求：
#    - 这是 service 层，先补 1 行中文注释标明“这是 service 层”
#    - 先调用 kb_repository_get(kb_id)
#    - 如果知识库不存在，抛出 ValueError("知识库不存在")
#    - 如果知识库已删除，抛出 ValueError("知识库已删除")
#    - 再调用 doc_repository_count_active_by_kb_id(kb_id)
#    - 再调用 doc_repository_list_active_titles_by_kb_id(kb_id, limit=2)
#    - 最后把这些结果组装成 KBDetailResponse 返回
# 4. 在文件底部的文字回答区补 3 句简短回答：
#    - 为什么“查知识库基本信息”和“查文档数量”可以放在同一个 service 里？
#    - 为什么这道题里 service 调多个 repository 是合理的？
#    - 如果把这些步骤全写进 router，最容易导致什么问题？
#
# 自查方式：
# 1. 完成后运行：
#    python section_04_workflow_orchestration.py
# 2. 你应该至少看到：
#    - detail_ok: {...}
#    - detail_missing_error: 知识库不存在
#    - detail_deleted_error: 知识库已删除
# 3. 你还要重点观察：
#    - 返回体里既有知识库基本信息，也有文档统计信息
#    - 这不是某一个 repository 单独能完成的，而是 service 编排出来的结果

#这是 service 层
def kb_service_detail(kb_id: int) -> KBDetailResponse:
    record = kb_repository_get(kb_id)
    if record is None:
        raise ValueError("知识库不存在")
    if record["is_deleted"]:
        raise ValueError("知识库已删除")
    return KBDetailResponse(
        id=kb_id,
        name=record["name"],
        description=record["description"],
        doc_count=doc_repository_count_active_by_kb_id(kb_id),
        doc_titles_preview=doc_repository_list_active_titles_by_kb_id(kb_id, limit=2)
    )


# 文字回答区：
#
# 1. 为什么“查知识库基本信息”和“查文档数量”可以放在同一个 service 里？
# 答：因为这个service的业务逻辑是需要的
#
# 2. 为什么这道题里 service 调多个 repository 是合理的？
# 答：因为这个业务逻辑需要调用多个repository才能完成
#
# 3. 如果把这些步骤全写进 router，最容易导致什么问题？
# 答：router太臃肿，其他层要做的事就少了


if __name__ == "__main__":
    detail_ok = kb_service_detail(1)
    print("detail_ok:", detail_ok.model_dump())

    try:
        kb_service_detail(999)
    except ValueError as exc:
        print("detail_missing_error:", str(exc))

    try:
        kb_service_detail(2)
    except ValueError as exc:
        print("detail_deleted_error:", str(exc))
