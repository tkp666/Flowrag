"""
阶段 5 第 2 小节动手题：Redis key 命名、set/get 语义和 TTL 设计。

本题不需要连接真实 Redis。
目标是练习为 FlowRAG 场景设计合理的 Redis key、value 示例、TTL 和过期后的处理策略。

填写规则：
- key: 使用冒号分层，能从名字看出业务含义
- value_example: 写一个示例值，可以是字符串、数字或 JSON 字符串
- ttl_seconds: 正整数，表示这个 key 应该保留多少秒
- on_miss: key 不存在或过期时应该怎么处理，用中文说明

注意：
- 不要把 key 写成无意义字符串，例如 abc123、data、cache
- 不要把 ttl_seconds 写得过长，除非你能说明理由
- Redis 缓存过期后通常应该回源 MySQL、重新检索或返回 progress unknown
"""

from __future__ import annotations


SCENARIOS = [
    {
        "id": "task_progress",
        "description": "文档入库任务 task_id=1001 当前进度 73%，给前端进度条展示",
    },
    {
        "id": "task_message",
        "description": "文档入库任务 task_id=1001 当前提示：正在处理第 38 个 chunk",
    },
    {
        "id": "retrieval_cache",
        "description": "知识库 kb_id=3 中 query_hash=abc123 的检索结果缓存",
    },
    {
        "id": "recent_chat",
        "description": "user_id=7 最近一次打开会话 conversation_id=9001 的页面摘要缓存",
    },
    {
        "id": "phone_code",
        "description": "手机号 13800000000 的登录验证码 246810",
    },
]


ANSWERS = {
    "task_progress": {
        "key": "task:1001:progress",
        "value_example": "73",
        "ttl_seconds": 600,
        "on_miss": "先查 MySQL 任务主状态；如果仍是 processing，就返回 progress unknown，而不是判断失败。",
    },
    "task_message": {
        "key": "task:1001:message",
        "value_example": "正在处理第 38 个 chunk",
        "ttl_seconds": 600,
        "on_miss": "返回默认提示：任务仍在处理中，暂无详细进度提示",
    },
    "retrieval_cache": {
        "key": "cache:kb:3:query:abc123",
        "value_example": "检索结果",
        "ttl_seconds": 300,
        "on_miss": "重新检索并写回 Redis",
    },
    "recent_chat": {
        "key": "chat:user:7:conversation:9001:summary",
        "value_example": "页面摘要缓存",
        "ttl_seconds": 600,
        "on_miss": "回源 MySQL 查询会话摘要或最近消息，再写回 Redis。",
    },
    "phone_code": {
        "key": "login_code:phone:13800000000",
        "value_example": "246810",
        "ttl_seconds": 300,
        "on_miss": "验证码已过期，重新发送",
    },
}


def self_check() -> None:
    scenario_ids = {scenario["id"] for scenario in SCENARIOS}
    answer_ids = set(ANSWERS)
    assert answer_ids == scenario_ids, "ANSWERS 必须覆盖所有 SCENARIOS，不能多也不能少"

    for scenario_id, answer in ANSWERS.items():
        key = answer.get("key", "")
        value_example = answer.get("value_example", "")
        ttl_seconds = answer.get("ttl_seconds")
        on_miss = answer.get("on_miss", "")

        assert key and key != "TODO", f"{scenario_id}: key 还没有填写"
        assert ":" in key, f"{scenario_id}: key 应该使用冒号分层，例如 task:1001:progress"
        assert " " not in key, f"{scenario_id}: key 不应该包含空格"
        assert value_example != "TODO", f"{scenario_id}: value_example 还没有填写"
        assert isinstance(ttl_seconds, int), f"{scenario_id}: ttl_seconds 必须是整数"
        assert ttl_seconds > 0, f"{scenario_id}: ttl_seconds 必须大于 0"
        assert on_miss != "TODO", f"{scenario_id}: on_miss 还没有填写"
        assert len(on_miss.strip()) >= 10, f"{scenario_id}: on_miss 太短，至少写清楚过期后的处理"

    print("section 02 key ttl design homework is complete")


if __name__ == "__main__":
    self_check()
