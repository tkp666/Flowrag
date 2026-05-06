"""
阶段 4 第 1 小节动手题：表、主键、外键、索引、唯一约束。

当前还不写 SQLAlchemy，也不连接 MySQL。
你只需要把 FlowRAG 的几个业务表关系设计清楚。

运行方式：
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/homework/section_01_table_constraints.py
"""


# 任务 1：
# 根据注释补全下面 4 个字段的角色。
#
# 可选答案只允许使用这几个字符串：
# - "primary_key"
# - "foreign_key"
# - "normal_column"
FIELD_ROLES = {
    # users.id 用来唯一表示一个用户
    "users.id": "primary_key",

    # knowledge_bases.id 用来唯一表示一个知识库
    "knowledge_bases.id": "primary_key",

    # knowledge_bases.user_id 表示这个知识库属于哪个用户
    "knowledge_bases.user_id": "foreign_key",

    # knowledge_bases.description 只是知识库描述文本
    "knowledge_bases.description": "normal_column",
}


# 任务 2：
# 下面这些字段是否适合在当前阶段优先考虑普通索引？
#
# 可选答案只允许使用 True / False。
INDEX_DECISIONS = {
    # 经常按用户查询知识库列表：WHERE user_id = ?
    "knowledge_bases.user_id": True,

    # 只是描述文本，当前不会高频精确查询
    "knowledge_bases.description": False,

    # 经常按知识库查询文档列表：WHERE kb_id = ?
    "documents.kb_id": True,
}


# 任务 3：
# 下面两个业务规则分别应该用什么约束表达？
#
# 可选答案：
# - "unique_constraint"
# - "combined_unique_index"
UNIQUE_RULES = {
    # 一个邮箱只能注册一个用户
    "users.email": "unique_constraint",

    # 同一个用户下面，知识库名称不能重复；不同用户可以使用同名知识库
    "knowledge_bases.user_id_name": "combined_unique_index",
}


# 任务 4：
# 用一句话解释为什么不能给所有字段都无脑加索引。
# 要求：
# - 写成一个字符串
# - 必须提到“写入”或“空间”中的至少一个
WHY_NOT_INDEX_EVERYTHING = "索引是拿写入成本和存储空间换查询速度，所以不能无脑全加。"


def check_homework() -> None:
    expected_field_roles = {
        "users.id": "primary_key",
        "knowledge_bases.id": "primary_key",
        "knowledge_bases.user_id": "foreign_key",
        "knowledge_bases.description": "normal_column",
    }
    expected_index_decisions = {
        "knowledge_bases.user_id": True,
        "knowledge_bases.description": False,
        "documents.kb_id": True,
    }
    expected_unique_rules = {
        "users.email": "unique_constraint",
        "knowledge_bases.user_id_name": "combined_unique_index",
    }

    assert FIELD_ROLES == expected_field_roles, f"FIELD_ROLES 不正确：{FIELD_ROLES}"
    assert INDEX_DECISIONS == expected_index_decisions, f"INDEX_DECISIONS 不正确：{INDEX_DECISIONS}"
    assert UNIQUE_RULES == expected_unique_rules, f"UNIQUE_RULES 不正确：{UNIQUE_RULES}"

    assert isinstance(WHY_NOT_INDEX_EVERYTHING, str), "WHY_NOT_INDEX_EVERYTHING 必须是字符串"
    assert WHY_NOT_INDEX_EVERYTHING.strip(), "WHY_NOT_INDEX_EVERYTHING 不能为空"
    assert (
        "写入" in WHY_NOT_INDEX_EVERYTHING
        or "空间" in WHY_NOT_INDEX_EVERYTHING
    ), "解释里至少要提到“写入”或“空间”"

    print("section 01 table constraints homework looks good")


if __name__ == "__main__":
    check_homework()
