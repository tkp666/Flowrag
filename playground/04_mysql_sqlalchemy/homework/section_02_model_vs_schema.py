"""
阶段 4 第 2 小节动手题：SQLAlchemy Model 和 Pydantic Schema 的区别。

当前还不连接 MySQL，也不要求你真的导入 SQLAlchemy。
这道题只检查你是否能分清：
- 数据库表结构应该放 SQLAlchemy model
- API 请求/响应结构应该放 Pydantic schema
- repository 以后负责在 model 对象和数据库之间读写

运行方式：
cd /home/tkp666/FlowRAG
/home/tkp666/miniconda3/envs/flowrag/bin/python playground/04_mysql_sqlalchemy/homework/section_02_model_vs_schema.py
"""


# 任务 1：
# 判断下面这些定义更应该属于哪一类。
#
# 可选答案只允许使用：
# - "sqlalchemy_model"
# - "pydantic_schema"
DEFINITION_OWNERS = {
    # 描述 users 表里 email 列唯一
    "users.email_unique": "sqlalchemy_model",

    # 描述 POST /knowledge-bases 请求体里允许用户传 name 和 description
    "kb_create_request_body": "pydantic_schema",

    # 描述 knowledge_bases.user_id 是外键，指向 users.id
    "knowledge_bases.user_id_foreign_key": "sqlalchemy_model",

    # 描述 GET /knowledge-bases/{kb_id} 响应里返回 id、name、description
    "kb_detail_response_body": "pydantic_schema",
}


# 任务 2：
# 下面这些字段是否应该直接暴露在 API 响应里？
#
# 可选答案只允许使用 True / False。
API_RESPONSE_FIELD_DECISIONS = {
    # 用户详情响应可以返回用户 id
    "users.id": True,

    # 用户详情响应不能返回密码哈希
    "users.password_hash": False,

    # 知识库详情响应可以返回知识库名称
    "knowledge_bases.name": True,

    # 普通知识库详情响应不应该直接暴露软删除内部标记
    "knowledge_bases.is_deleted": False,
}


# 任务 3：
# 把下面几种“对象/结构”和它们最合适的职责对应起来。
#
# 可选答案只允许使用：
# - "database_table_mapping"
# - "api_contract"
# - "business_flow"
# - "database_read_write"
LAYER_RESPONSIBILITIES = {
    # SQLAlchemy model
    "KnowledgeBaseModel": "database_table_mapping",

    # Pydantic schema
    "KBCreateSchema": "api_contract",

    # service 层
    "kb_service_create": "business_flow",

    # repository 层
    "kb_repository_insert": "database_read_write",
}


# 任务 4：
# 用一句话解释为什么不建议把 SQLAlchemy model 直接当成 API 响应结构。
# 要求：
# - 写成一个字符串
# - 必须提到“内部字段”或“暴露”中的至少一个
WHY_NOT_RETURN_MODEL_DIRECTLY = "SQLAlchemy model中有许多的内部字段如密码哈希值等，是不应该暴露给前端的API的"


def check_homework() -> None:
    expected_definition_owners = {
        "users.email_unique": "sqlalchemy_model",
        "kb_create_request_body": "pydantic_schema",
        "knowledge_bases.user_id_foreign_key": "sqlalchemy_model",
        "kb_detail_response_body": "pydantic_schema",
    }
    expected_api_response_field_decisions = {
        "users.id": True,
        "users.password_hash": False,
        "knowledge_bases.name": True,
        "knowledge_bases.is_deleted": False,
    }
    expected_layer_responsibilities = {
        "KnowledgeBaseModel": "database_table_mapping",
        "KBCreateSchema": "api_contract",
        "kb_service_create": "business_flow",
        "kb_repository_insert": "database_read_write",
    }

    assert DEFINITION_OWNERS == expected_definition_owners, f"DEFINITION_OWNERS 不正确：{DEFINITION_OWNERS}"
    assert (
        API_RESPONSE_FIELD_DECISIONS == expected_api_response_field_decisions
    ), f"API_RESPONSE_FIELD_DECISIONS 不正确：{API_RESPONSE_FIELD_DECISIONS}"
    assert (
        LAYER_RESPONSIBILITIES == expected_layer_responsibilities
    ), f"LAYER_RESPONSIBILITIES 不正确：{LAYER_RESPONSIBILITIES}"

    assert isinstance(WHY_NOT_RETURN_MODEL_DIRECTLY, str), "WHY_NOT_RETURN_MODEL_DIRECTLY 必须是字符串"
    assert WHY_NOT_RETURN_MODEL_DIRECTLY.strip(), "WHY_NOT_RETURN_MODEL_DIRECTLY 不能为空"
    assert (
        "内部字段" in WHY_NOT_RETURN_MODEL_DIRECTLY
        or "暴露" in WHY_NOT_RETURN_MODEL_DIRECTLY
    ), "解释里至少要提到“内部字段”或“暴露”"

    print("section 02 model vs schema homework looks good")


if __name__ == "__main__":
    check_homework()
