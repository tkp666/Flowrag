from pydantic import BaseModel


# 这是请求体 schema：创建知识库时前端提交的数据格式
class KBCreate(BaseModel):
    name: str
    description: str | None = None


# 这是响应体 schema：返回给前端的知识库数据格式
class KBResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


# 这是模拟数据库记录的存储区
fake_kb_table: dict[int, dict] = {}
next_kb_id = 1


# 这是 repository 层：按名称查原始 record
def kb_repository_find_by_name(name: str) -> dict | None:
    for record in fake_kb_table.values():
        if record["name"] == name and record["is_deleted"] is False:
            return record
    return None


# 这是 repository 层：插入原始 record
def kb_repository_insert(record: dict) -> dict:
    fake_kb_table[record["id"]] = record
    return record


# 这是 repository 层：按 id 查原始 record
def kb_repository_get(kb_id: int) -> dict | None:
    return fake_kb_table.get(kb_id)


# 这是 repository 层：软删除原始 record
def kb_repository_soft_delete(kb_id: int) -> dict | None:
    record = fake_kb_table.get(kb_id)
    if record is None:
        return None
    record["is_deleted"] = True
    return record


def kb_service_create_bad(payload: KBCreate) -> dict:
    """
    这是一个“空心 service / 纯转发 service”的坏例子。
    问题：
    1. 没有检查知识库名称是否重复；
    2. 没有组装完整的内部 record；
    3. 没有返回接口层真正需要的 KBResponse；
    4. 它只是把 payload 原样塞给 repository，service 自己几乎没做事。
    """
    return kb_repository_insert(payload.model_dump())


# 第 2 阶段 · 第 3 小节动手题：
# 这一题的重点是：让 service 真正承载“业务规则”和“流程编排”，而不是当中转站。
#
# 你要完成的内容：
# 1. 保留 kb_service_create_bad，不要删除。
# 2. 在下面补 3 个函数：
#    - kb_service_create
#    - kb_service_detail
#    - kb_service_delete
# 3. 要求：
#    - service_create 负责：
#      - 检查知识库名称是否重复（调用 repository_find_by_name）
#      - 重名时抛出 ValueError("知识库名称已存在")
#      - 生成 id
#      - 组装内部 record（至少包含 id/name/description/owner_id/is_deleted）
#      - 调 repository_insert
#      - 返回 KBResponse
#    - service_detail 负责：
#      - 调用 repository_get
#      - 如果不存在，抛出 ValueError("知识库不存在")
#      - 如果已删除，抛出 ValueError("知识库已删除")
#      - 否则把原始 record 转成 KBResponse 返回
#    - service_delete 负责：
#      - 调用 repository_get
#      - 如果不存在，抛出 ValueError("知识库不存在")
#      - 如果已删除，抛出 ValueError("知识库已删除")
#      - 否则调用 repository_soft_delete
#      - 返回 True
# 4. 你还要在每个 service 函数上方补 1 行中文注释，明确写出“这是 service 层”。
# 5. 在文件底部的文字回答区补 3 句简短回答：
#    - 为什么“重名检查”更适合放在 service，而不是 repository？
#    - 为什么“已删除不能重复删除”更像业务规则，而不是存储细节？
#    - 如果 service 只是 return repository_xxx(...)，它最容易变成什么问题？
#
# 自查方式：
# 1. 完成后运行：
#    python section_03_service_business_rules.py
# 2. 你应该至少看到：
#    - created: {...}
#    - duplicate_error: 知识库名称已存在
#    - detail: {...}
#    - deleted: True
#    - delete_again_error: 知识库已删除

#这是 service 层
def kb_service_create(payload: KBCreate, owner_id: int) -> KBResponse:
    global next_kb_id
    if not kb_repository_find_by_name(payload.name):
        record = {
            "id": next_kb_id,
            "name": payload.name,
            "description": payload.description,
            "owner_id": owner_id,
            "is_deleted": False
        }
        kb_repository_insert(record)
        result =  KBResponse(id=next_kb_id, name=payload.name, description=payload.description)
        next_kb_id += 1
        return result
    raise ValueError("知识库名称已存在")
    

#这是 service 层
def kb_service_detail(kb_id: int) -> KBResponse:
    record = kb_repository_get(kb_id)
    if record is None:
        raise ValueError("知识库不存在")
    if record["is_deleted"]:
        raise ValueError("知识库已删除") 
    return KBResponse(id=record["id"], name=record["name"], description=record["description"])

        

#这是 service 层
def kb_service_delete(kb_id: int) -> bool:
    record = kb_repository_get(kb_id)
    if record is None:
        raise ValueError("知识库不存在")
    if record["is_deleted"]:
        raise ValueError("知识库已删除")
    kb_repository_soft_delete(kb_id)
    return True

# 文字回答区：
#
# 1. 为什么“重名检查”更适合放在 service，而不是 repository？
# 答：repository只应该负责存取查数据，而不应该做这种跟业务相关的工作
#
# 2. 为什么“已删除不能重复删除”更像业务规则，而不是存储细节？
# 答：存储部分只应该去做查存取数据，至于每个字段以及对应的值有什么含义这需要交给service层去判断
#
# 3. 如果 service 只是 return repository_xxx(...)，它最容易变成什么问题？
# 答：把大量的任务交给repository层去做，service层形同虚设


if __name__ == "__main__":
    payload = KBCreate(name="demo-kb", description="first kb")

    created = kb_service_create(payload, owner_id=1001)
    print("created:", created.model_dump())

    try:
        kb_service_create(payload, owner_id=1001)
    except ValueError as exc:
        print("duplicate_error:", str(exc))

    detail = kb_service_detail(1)
    print("detail:", detail.model_dump())

    deleted = kb_service_delete(1)
    print("deleted:", deleted)

    try:
        kb_service_delete(1)
    except ValueError as exc:
        print("delete_again_error:", str(exc))
