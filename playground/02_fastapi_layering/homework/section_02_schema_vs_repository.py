from pydantic import BaseModel


# 这是请求体 schema：创建知识库时前端提交的数据格式
class KBCreate(BaseModel):
    name: str
    description: str | None = None


# 这是响应体 schema：后端返回给前端的数据格式
class KBResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


# 这是“模拟数据库记录”的存储区，不等于接口 schema
fake_kb_table: dict[int, dict] = {}
next_kb_id = 1


def create_kb_bad(payload: KBCreate) -> dict:
    """
    这是一个“把 schema、业务规则、存储记录全混在一起”的坏例子。
    你不用删它，它只作为对照参考。
    """
    global next_kb_id
    record = {
        "id": next_kb_id,
        "name": payload.name,
        "description": payload.description,
        "owner_id": 1001,
        "is_deleted": False,
    }
    fake_kb_table[next_kb_id] = record
    next_kb_id += 1
    return record


# 第 2 阶段 · 第 2 小节动手题：
# 这一题的重点不是“再写一个接口”，而是亲手把这三件事分清楚：
# 1. 请求体 / 响应体 schema
# 2. 底层存储记录
# 3. repository / service 的职责
#
# 你要完成的内容：
# 1. 保留 create_kb_bad，不要删除。
# 2. 在下面补 4 个函数：
#    - kb_repository_insert
#    - kb_repository_get
#    - kb_service_create
#    - kb_service_get
# 3. 要求：
#    - repository 只负责“存原始 record / 取原始 record”
#    - repository 不要返回 KBResponse
#    - service_create 负责：
#      - 生成 id
#      - 组装内部 record（包含 owner_id / is_deleted）
#      - 调用 repository_insert
#      - 最后返回 KBResponse
#    - service_get 负责：
#      - 调用 repository_get
#      - 把原始 record 转成 KBResponse
#      - 如果查不到，返回 None
# 4. 你还要在每个函数上方补 1 行中文注释，明确写出：
#    - 这是 repository 层
#    - 这是 service 层
# 5. 在文件底部的文字回答区补 3 句简短回答：
#    - 为什么 repository 更适合返回原始 record，而不是直接返回 KBResponse？
#    - 为什么响应体里不应该把 owner_id / is_deleted 直接暴露给前端？
#    - 如果以后数据库里新增 created_at，哪一层最可能先改？
#
# 自查方式：
# 1. 完成后运行：
#    python section_02_schema_vs_repository.py
# 2. 你应该至少看到：
#    - created_response: {...}
#    - raw_record: {...}
#    - fetched_response: {...}
# 3. 你要重点观察：
#    - raw_record 比 response 多了哪些字段
#    - 为什么“存储记录”和“接口返回”不是同一套结构

#这是 repository 层
def kb_repository_insert(record: dict) -> dict:
    fake_kb_table[record["id"]] = record
    return record

#这是 repository 层
def kb_repository_get(kb_id: int) -> dict | None:
    if kb_id in fake_kb_table:
        return fake_kb_table[kb_id]
    return None

#这是 service 层
def kb_service_create(payload: KBCreate, owner_id: int) -> KBResponse:
    global next_kb_id
    record = {
        "id": next_kb_id,
        "name": payload.name,
        "description": payload.description,
        "owner_id": owner_id,
        "is_deleted": False,
    }
    kb_repository_insert(record)
    response_body = KBResponse(
        id=next_kb_id,
        name=payload.name,
        description=payload.description
    )
    next_kb_id += 1
    return response_body

#这是 service 层
def kb_service_get(kb_id: int) -> KBResponse | None:
    result = kb_repository_get(kb_id)
    if result:
        return KBResponse(
            id=result["id"],
            name=result["name"],
            description=result["description"]
        )
    return None
        


# 文字回答区：
#
# 1. 为什么 repository 更适合返回原始 record，而不是直接返回 KBResponse？
# 答：repository只对他已有的数据负责，原始数据是什么样他就会给你什么样，至于你要怎么用它，是组装成KBResponse还是其他形式的，跟repository没有关系，这是service层该做的事
#
# 2. 为什么响应体里不应该把 owner_id / is_deleted 直接暴露给前端？
# 答：前端不需要看到这个信息啊，他如果查询了并不属于自己的数据就不应该告诉他owner_id之类的详细信息啊
#
# 3. 如果以后数据库里新增 created_at，哪一层最可能先改？
# 答：我觉得应该是service层需要先改，他得把前端给他的数据组织成repository层所需要的数据库表的格式再传给repository层


if __name__ == "__main__":
    created_response = kb_service_create(
        KBCreate(name="demo-kb", description="first kb"),
        owner_id=1001,
    )
    raw_record = kb_repository_get(1)
    fetched_response = kb_service_get(1)

    print("created_response:", created_response.model_dump())
    print("raw_record:", raw_record)
    print("fetched_response:", fetched_response.model_dump() if fetched_response else None)
