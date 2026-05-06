# 这是 repository 层：
# 当前仍然用内存结构模拟数据库。


fake_kb_table: dict[int, dict] = {}
next_kb_id_ref = {"value": 1}


def kb_repository_find_by_name(name: str) -> dict | None:
    """
    按名称查未删除知识库。
    """
    for record in fake_kb_table.values():
        if record["name"] == name and record["is_deleted"] is False:
            return record
    return None


def kb_repository_insert(record: dict) -> dict:
    """
    插入一条原始 record。
    """
    fake_kb_table[record["id"]] = record
    return record


def kb_repository_list() -> list[dict]:
    """
    返回全部原始 record。
    """
    all_result: list[dict] = []
    for res in fake_kb_table.values():
        all_result.append(res)
    return all_result
    


def kb_repository_get(kb_id: int) -> dict | None:
    """
    按 id 取单条原始 record。
    """
    res = fake_kb_table.get(kb_id)
    if res is None:
        return None
    return res


def kb_repository_soft_delete(kb_id: int) -> dict | None:
    """
    软删除一条 record。
    """
    record = fake_kb_table.get(kb_id)
    if record is None:
        return None
    record["is_deleted"] = True
    return record
