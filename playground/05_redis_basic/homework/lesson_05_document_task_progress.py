"""
阶段 5 综合课后动手题：文档入库任务的 Redis 进度状态设计。

这道题不是重复“知识库详情缓存”，而是换到 FlowRAG 未来真实会用到的场景：
用户上传文档后，文档解析、切块、embedding、入库会变成一个后台任务。

当前阶段还没学 Celery，所以这里不启动真正后台任务，只练 Redis 在任务进度中的职责：

- MySQL 保存任务的权威状态和最终结果；
- Redis 保存短期、高频变化的过程进度；
- Redis 进度丢失时，不能把任务误判为失败；
- 任务完成或失败时，可以删除 Redis 里的进度 key；
- 失败原因这种需要追溯的信息，应该写回 MySQL。

运行前确认 Redis 可用：
    redis-cli ping

运行本题：
    cd /home/tkp666/FlowRAG
    /home/tkp666/miniconda3/envs/flowrag/bin/python playground/05_redis_basic/homework/lesson_05_document_task_progress.py

你需要完成所有 TODO。通过时输出：
    lesson 05 document task progress homework looks good
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import redis


REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
TASK_PROGRESS_TTL_SECONDS = 30 * 60


VALID_MYSQL_STATUS = {"queued", "running", "succeeded", "failed"}


FAKE_MYSQL_TASK_TABLE: dict[int, dict[str, object]] = {
    1001: {
        "task_id": 1001,
        "document_id": 501,
        "status": "running",
        "error_message": None,
    },
    1002: {
        "task_id": 1002,
        "document_id": 502,
        "status": "succeeded",
        "error_message": None,
    },
} 


@dataclass
class ProgressSnapshot:
    task_id: int
    stage: str
    percent: int
    message: str


@dataclass
class TaskStatusResponse:
    task_id: int
    mysql_status: str
    progress_source: str
    progress: ProgressSnapshot | None
    error_message: str | None


def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )


def build_task_progress_key(task_id: int) -> str:
    """
    TODO:
    返回任务进度 Redis key。

    要求：
    - task_id=1001 时返回 task:1001:progress
    - 这个 key 存的是短期过程进度，不是任务最终状态
    """
    return f"task:{task_id}:progress"


def get_task_from_mysql(task_id: int) -> dict[str, object] | None:
    """
    TODO:
    从模拟 MySQL 表查询任务。

    要求：
    - 不存在时返回 None
    - 存在时返回浅拷贝，避免调用方直接改 FAKE_MYSQL_TASK_TABLE
    """
    record = FAKE_MYSQL_TASK_TABLE.get(task_id)
    if record is None:
        return None
    return record.copy()


def update_task_status_in_mysql(
    task_id: int,
    status: str,
    error_message: str | None = None,
) -> dict[str, object]:
    """
    TODO:
    更新模拟 MySQL 中的任务权威状态。

    要求：
    - task_id 不存在时抛出 ValueError("task not found")
    - status 必须在 VALID_MYSQL_STATUS 中，否则抛出 ValueError("invalid task status")
    - 更新 status
    - 更新 error_message
    - 返回更新后记录的浅拷贝
    """
    record = FAKE_MYSQL_TASK_TABLE.get(task_id)
    if record is None:
        raise ValueError("task not found")
    if status not in VALID_MYSQL_STATUS:
        raise ValueError("invalid task status")
    record["status"] = status
    record["error_message"] = error_message
    return record.copy()
    


def write_task_progress_to_redis(
    client: redis.Redis,
    snapshot: ProgressSnapshot,
    ttl_seconds: int = TASK_PROGRESS_TTL_SECONDS,
) -> None:
    """
    TODO:
    把任务过程进度写到 Redis。

    要求：
    - key 使用 build_task_progress_key(snapshot.task_id)
    - value 使用 JSON 字符串，至少包含 task_id/stage/percent/message
    - percent 必须在 0 到 100 之间，否则抛出 ValueError("invalid progress percent")
    - 使用 setex(key, ttl_seconds, value)
    """
    key = build_task_progress_key(snapshot.task_id)
    if snapshot.percent < 0 or snapshot.percent > 100:
        raise ValueError("invalid progress percent")
    value = {
        "task_id": snapshot.task_id,
        "stage": snapshot.stage,
        "percent": snapshot.percent,
        "message": snapshot.message,
    }
    value = json.dumps(value, ensure_ascii=False)
    client.setex(
        key,
        ttl_seconds,
        value,
    )
    


def read_task_progress_from_redis(
    client: redis.Redis,
    task_id: int,
) -> ProgressSnapshot | None:
    """
    TODO:
    从 Redis 读取任务过程进度。

    要求：
    - key 使用 build_task_progress_key(task_id)
    - Redis 没有这个 key 时返回 None
    - 取到 JSON 后用 json.loads 还原
    - 返回 ProgressSnapshot(...)
    """
    key = build_task_progress_key(task_id)
    task_progress = client.get(key)
    if task_progress is None:
        return None
    return ProgressSnapshot(**json.loads(task_progress))


def clear_task_progress_from_redis(client: redis.Redis, task_id: int) -> None:
    """
    TODO:
    删除任务过程进度 key。

    要求：
    - key 使用 build_task_progress_key(task_id)
    - 调 client.delete(key)
    """
    key = build_task_progress_key(task_id)
    client.delete(key)


def get_task_status(
    client: redis.Redis,
    task_id: int,
) -> TaskStatusResponse:
    """
    TODO:
    组合 MySQL 权威状态和 Redis 过程进度，返回任务状态。

    业务要求：
    1. 先查 MySQL 任务；
    2. MySQL 没有时抛出 ValueError("task not found")；
    3. 如果 MySQL 状态是 failed：
       - 返回 mysql_status="failed"
       - error_message 使用 MySQL 中的错误信息
       - progress_source="mysql"
       - progress=None
    4. 如果 MySQL 状态是 succeeded：
       - 返回 mysql_status="succeeded"
       - progress_source="mysql"
       - progress 可以是 percent=100 的 ProgressSnapshot
    5. 如果 MySQL 状态是 queued 或 running：
       - 优先读 Redis 过程进度
       - Redis 有进度时 progress_source="redis"
       - Redis 没进度时 progress_source="missing"，progress=None
       - Redis 进度丢失不能把任务误判成 failed
    """
    record = get_task_from_mysql(task_id)
    if record is None:
        raise ValueError("task not found")
    if record["status"] == "failed":
        return TaskStatusResponse(
            task_id=task_id,
            mysql_status=record["status"],
            progress_source="mysql",
            progress=None,
            error_message=record["error_message"],
        )
    if record["status"] == "succeeded":
        return TaskStatusResponse(
            task_id=task_id,
            mysql_status=record["status"],
            progress_source="mysql",
            progress= ProgressSnapshot(
                task_id=task_id,
                stage="succeeded",
                percent=100,
                message="任务已完成",
            ),
            error_message=record["error_message"],
        )
    if record["status"] == "queued" or record["status"] == "running":
        redis_record = read_task_progress_from_redis(client, task_id)
        if redis_record is None:
            progress_source = "missing"
            progress = None
        else:
            progress_source = "redis"
            progress = redis_record
        return TaskStatusResponse(
            task_id=task_id,
            mysql_status=record["status"],
            progress_source=progress_source,
            progress=progress,
            error_message=record["error_message"],
        )
    raise ValueError("invalid task status")
    


def mark_task_failed(
    client: redis.Redis,
    task_id: int,
    error_message: str,
) -> TaskStatusResponse:
    """
    TODO:
    标记任务失败。

    业务要求：
    - 失败状态和错误信息写回 MySQL
    - 删除 Redis 里的过程进度
    - 返回 get_task_status(...) 的结果
    """
    update_task_status_in_mysql(task_id, "failed", error_message)
    clear_task_progress_from_redis(client, task_id)
    return get_task_status(client, task_id)
    


def mark_task_succeeded(client: redis.Redis, task_id: int) -> TaskStatusResponse:
    """
    TODO:
    标记任务成功。

    业务要求：
    - 成功状态写回 MySQL
    - 删除 Redis 里的过程进度
    - 返回 get_task_status(...) 的结果
    """
    update_task_status_in_mysql(task_id, "succeeded", None)
    clear_task_progress_from_redis(client, task_id)
    return get_task_status(client, task_id)


def reset_fake_mysql_table() -> None:
    FAKE_MYSQL_TASK_TABLE.clear()
    FAKE_MYSQL_TASK_TABLE.update(
        {
            1001: {
                "task_id": 1001,
                "document_id": 501,
                "status": "running",
                "error_message": None,
            },
            1002: {
                "task_id": 1002,
                "document_id": 502,
                "status": "succeeded",
                "error_message": None,
            },
        }
    )


def reset_homework_keys(client: redis.Redis) -> None:
    keys = [
        build_task_progress_key(1001),
        build_task_progress_key(1002),
        build_task_progress_key(9999),
    ]
    client.delete(*keys)


def self_check() -> None:
    client = get_redis_client()
    assert client.ping() is True, "Redis 连接失败，请先确认 redis-cli ping 能返回 PONG"

    reset_fake_mysql_table()
    reset_homework_keys(client)

    key = build_task_progress_key(1001)
    assert key == "task:1001:progress", "任务进度 key 命名不正确"

    task = get_task_from_mysql(1001)
    assert task is not None
    assert task["status"] == "running"
    task["status"] = "failed"
    assert FAKE_MYSQL_TASK_TABLE[1001]["status"] == "running", "查询 MySQL 任务时应该返回浅拷贝"

    write_task_progress_to_redis(
        client,
        ProgressSnapshot(
            task_id=1001,
            stage="embedding",
            percent=45,
            message="正在生成向量",
        ),
        ttl_seconds=60,
    )
    assert client.ttl(key) > 0, "任务进度必须设置 TTL"

    progress = read_task_progress_from_redis(client, 1001)
    assert progress is not None
    assert progress.stage == "embedding"
    assert progress.percent == 45

    running_status = get_task_status(client, 1001)
    assert running_status.mysql_status == "running"
    assert running_status.progress_source == "redis"
    assert running_status.progress is not None
    assert running_status.progress.percent == 45

    clear_task_progress_from_redis(client, 1001)
    missing_progress_status = get_task_status(client, 1001)
    assert missing_progress_status.mysql_status == "running"
    assert missing_progress_status.progress_source == "missing"
    assert missing_progress_status.progress is None, "Redis 进度丢失时不能伪造进度"

    succeeded_status = mark_task_succeeded(client, 1001)
    assert succeeded_status.mysql_status == "succeeded"
    assert succeeded_status.progress_source == "mysql"
    assert succeeded_status.progress is not None
    assert succeeded_status.progress.percent == 100
    assert client.exists(key) == 0, "任务完成后应该删除 Redis 过程进度"

    reset_fake_mysql_table()
    write_task_progress_to_redis(
        client,
        ProgressSnapshot(
            task_id=1001,
            stage="chunking",
            percent=20,
            message="正在切分文档",
        ),
        ttl_seconds=60,
    )
    failed_status = mark_task_failed(client, 1001, "PDF 解析失败")
    assert failed_status.mysql_status == "failed"
    assert failed_status.progress_source == "mysql"
    assert failed_status.progress is None
    assert failed_status.error_message == "PDF 解析失败"
    assert FAKE_MYSQL_TASK_TABLE[1001]["error_message"] == "PDF 解析失败"
    assert client.exists(key) == 0, "任务失败后应该删除 Redis 过程进度"

    try:
        write_task_progress_to_redis(
            client,
            ProgressSnapshot(
                task_id=1001,
                stage="embedding",
                percent=120,
                message="错误进度",
            ),
            ttl_seconds=60,
        )
    except ValueError as exc:
        assert str(exc) == "invalid progress percent"
    else:
        raise AssertionError("percent 超过 100 时应该抛出 ValueError")

    try:
        update_task_status_in_mysql(1001, "half_done")
    except ValueError as exc:
        assert str(exc) == "invalid task status"
    else:
        raise AssertionError("非法任务状态应该抛出 ValueError")

    try:
        get_task_status(client, 9999)
    except ValueError as exc:
        assert str(exc) == "task not found"
    else:
        raise AssertionError("不存在的任务应该抛出 ValueError")

    reset_homework_keys(client)
    reset_fake_mysql_table()
    print("lesson 05 document task progress homework looks good")


if __name__ == "__main__":
    self_check()
