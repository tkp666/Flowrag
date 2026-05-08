"""
阶段 5 第 1 小节动手题：Redis 和 MySQL 的职责边界。

本题不需要连接真实 Redis，也不需要连接 MySQL。
目标是判断 FlowRAG 中不同数据应该放在哪里，以及为什么。

填写规则：
- storage 可选值：mysql / redis / both
- reason 用中文写 1-2 句话，说明原因

判断标准不是“Redis 快不快”，而是：
- 这个数据是不是长期业务事实
- 能不能过期
- 丢了能不能重建
- 是否需要外键、分页、审计、历史查询
- 是否属于高频变化的临时状态、缓存、计数
"""

from __future__ import annotations


CASES = [
    {
        "id": "kb_name",
        "description": "知识库 id=3 的名称 paper-kb，以及它属于 user_id=1",
    },
    {
        "id": "task_progress",
        "description": "文档入库任务 task_id=1001 当前进度 73%，当前提示：正在处理第 38 个 chunk",
    },
    {
        "id": "task_final_failure",
        "description": "文档入库任务 task_id=1001 最终失败，错误码 PDF_PARSE_ERROR，错误信息：PDF 文件损坏",
    },
    {
        "id": "chat_rate_counter",
        "description": "user_id=7 在 60 秒内已经调用 chat 接口 4 次，用于限流判断",
    },
    {
        "id": "retrieval_cache",
        "description": "知识库 kb_id=3 中 query_hash=abc123 的检索结果缓存，短时间内可复用，过期后可重新检索",
    },
    {
        "id": "document_metadata",
        "description": "文档 document_id=10 的 filename、kb_id、ingest_status、created_at",
    },
]



ANSWERS = {
    "kb_name": {
        "storage": "mysql",
        "reason": "知识库的ID、名称、外键这些关键信息应该持久化保存，所以要存到mysql",
    },
    "task_progress": {
        "storage": "redis",
        "reason": "信息过于细粒度了，很快就会过时，并且也没那么重要，所以存redis",
    },
    "task_final_failure": {
        "storage": "both",
        "reason": "信息比较重要，所以mysql需要保存，redis中存一份缓存副本，让用户快点的查到结果，但是可以设置较短的过期时间",
    },
    "chat_rate_counter": {
        "storage": "redis",
        "reason": "限流判断的信息可以存redis",
    },
    "retrieval_cache": {
        "storage": "redis",
        "reason": "结果缓存可以存redis，短时间内可以快速查询提升用户体验",
    },
    "document_metadata": {
        "storage": "mysql",
        "reason": "这些重要信息应该持久化的保存到数据库",
    },
}


VALID_STORAGE = {"mysql", "redis", "both"}


def self_check() -> None:
    case_ids = {case["id"] for case in CASES}
    answer_ids = set(ANSWERS)
    assert answer_ids == case_ids, "ANSWERS 必须覆盖所有 CASES，不能多也不能少"

    for case_id, answer in ANSWERS.items():
        storage = answer.get("storage")
        reason = answer.get("reason", "")

        assert storage in VALID_STORAGE, f"{case_id}: storage 必须是 mysql / redis / both"
        assert reason != "TODO", f"{case_id}: reason 还没有填写"
        assert len(reason.strip()) >= 12, f"{case_id}: reason 太短，至少写清楚核心理由"

    print("section 01 redis/mysql boundary homework is complete")


if __name__ == "__main__":
    self_check()
