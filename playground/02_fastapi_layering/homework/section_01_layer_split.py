from pydantic import BaseModel


class KBCreate(BaseModel):
    name: str
    description: str | None = None


class KBResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


kb_store: dict[int, KBResponse] = {}
next_kb_id = 1


def create_kb_bad(payload: KBCreate) -> KBResponse:
    """
    这是一个“全部写在一起”的坏例子。
    它把：
    - 接口入口职责
    - 业务处理职责
    - 数据存取职责
    全都混到了一个函数里。

    你不用删这个函数，它只作为参考。
    """
    global next_kb_id
    kb = KBResponse(
        id=next_kb_id,
        name=payload.name,
        description=payload.description,
    )
    kb_store[next_kb_id] = kb
    next_kb_id += 1
    return kb


# 第 2 阶段 · 第 1 小节动手题：
# 本题不是再让你重复写一个最小接口，而是让你把“混在一起的代码”拆出层次感。
#
# 你要完成的内容：
# 1. 保留 create_kb_bad，不要删除。
# 2. 在下面补出 3 个函数：
#    - kb_repository_save
#    - kb_service_create
#    - kb_router_create
# 3. 要求：
#    - repository 只负责“存数据”，不要生成 id，不要决定业务规则
#    - service 负责“生成 id、组装 KBResponse、调用 repository”
#    - router 负责“接收 payload，并调用 service”，不要直接操作 kb_store
# 4. 你还要在每个函数上方补 1 行中文注释，明确写出：
#    - 这是 repository 层
#    - 这是 service 层
#    - 这是 router 层
# 5. 最后在文件底部的文字回答区，补 3 句简短回答：
#    - 为什么生成 id 更适合放在 service，而不是 repository？
#    - 为什么 router 不应该直接写 kb_store[next_kb_id] = ...？
#    - 如果以后把内存 dict 换成 MySQL，哪一层改动最大？
#
# 自查方式：
# 1. 完成后运行：
#    python section_01_layer_split.py
# 2. 你应该至少看到：
#    - created: {...}
#    - store_keys: [1]
# 3. 如果 router 里直接碰 kb_store，或者 repository 里生成 id，就说明分层还没分干净。

#这是 repository 层
def kb_repository_save(kb: KBResponse) -> KBResponse:
    kb_store[kb.id] = kb
    return kb

#这是 service 层
def kb_service_create(payload: KBCreate) -> KBResponse:
    global next_kb_id
    kb = KBResponse(
        id=next_kb_id,
        name=payload.name,
        description=payload.description,
    )
    kb_repository_save(kb)
    next_kb_id += 1
    return kb

#这是 router 层
def kb_router_create(payload: KBCreate) -> KBResponse:
    return kb_service_create(payload)


# 文字回答区：
#
# 1. 为什么生成 id 更适合放在 service，而不是 repository？
# 答：repository层应该只负责存取数据，他接到的应该就已经是完整的数据了，id属于业务规则，应该放在service
#
# 2. 为什么 router 不应该直接写 kb_store[next_kb_id] = ...？
# 答：kb_store[next_kb_id] = ...应该是repository的任务
#
# 3. 如果以后把内存 dict 换成 MySQL，哪一层改动最大？
# 答：repository 层


if __name__ == "__main__":
    payload = KBCreate(name="demo-kb", description="first kb")
    created = kb_router_create(payload)
    print("created:", created.model_dump())
    print("store_keys:", list(kb_store.keys()))
