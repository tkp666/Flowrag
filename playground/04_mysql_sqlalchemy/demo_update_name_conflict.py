"""
演示：更新知识库名称时，为什么要区分“查到自己”和“查到当前用户的另一条记录”。

运行方式：
cd /home/tkp666/FlowRAG/playground/04_mysql_sqlalchemy
/home/tkp666/miniconda3/envs/flowrag/bin/python demo_update_name_conflict.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.repositories import kb_repository_find_active_by_name
from app.schemas import KBCreate, KBUpdate, UserCreate
from app.services import kb_service_create, kb_service_update, user_service_create


def explain_result(current_kb_id: int, target_name: str, found_id: int | None) -> None:
    print(f"\n准备更新 id={current_kb_id} 的知识库，把 name 设为 {target_name!r}")

    if found_id is None:
        print("按 user_id + name 没查到任何未删除知识库：可以改。")
        return

    print(f"按 user_id + name 查到了 id={found_id}")
    if found_id == current_kb_id:
        print("查到的是当前知识库自己：应该允许。")
    else:
        print("查到的是当前用户的另一条知识库：应该拒绝，否则同一用户下会重名。")


def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with SessionLocal() as session:
        user = user_service_create(
            session,
            UserCreate(email="a@example.com", username="alice"),
        )

        paper_kb = kb_service_create(
            session,
            KBCreate(name="paper-kb", description="论文知识库"),
            current_user_id=user.id,
        )
        job_kb = kb_service_create(
            session,
            KBCreate(name="job-kb", description="求职知识库"),
            current_user_id=user.id,
        )

        print("当前用户有两个知识库：")
        print(f"- id={paper_kb.id}, name={paper_kb.name!r}")
        print(f"- id={job_kb.id}, name={job_kb.name!r}")

        # 情况 1：把 job-kb 更新成它自己的原名称。
        found = kb_repository_find_active_by_name(session, user.id, "job-kb")
        explain_result(
            current_kb_id=job_kb.id,
            target_name="job-kb",
            found_id=None if found is None else found.id,
        )

        try:
            kb_service_update(
                session,
                job_kb.id,
                KBUpdate(name="job-kb", description="只是改描述"),
                current_user_id=user.id,
            )
        except ValueError as exc:
            print(f"当前 kb_service_update 实际结果：报错 {exc!r}")
            print("这就是当前 bug：它把自己也当成重复名称了。")
        else:
            print("当前 kb_service_update 实际结果：成功")

        # 情况 2：把 job-kb 更新成同一用户另一条知识库的名称。
        found = kb_repository_find_active_by_name(session, user.id, "paper-kb")
        explain_result(
            current_kb_id=job_kb.id,
            target_name="paper-kb",
            found_id=None if found is None else found.id,
        )

        try:
            kb_service_update(
                session,
                job_kb.id,
                KBUpdate(name="paper-kb", description=None),
                current_user_id=user.id,
            )
        except ValueError as exc:
            print(f"当前 kb_service_update 实际结果：报错 {exc!r}")
            print("这个报错是正确的，因为同一用户下 paper-kb 已经被另一条记录占用了。")
        else:
            print("当前 kb_service_update 实际结果：成功，这反而是不应该的。")

        # 情况 3：把 job-kb 更新成没人用的新名称。
        found = kb_repository_find_active_by_name(session, user.id, "new-kb")
        explain_result(
            current_kb_id=job_kb.id,
            target_name="new-kb",
            found_id=None if found is None else found.id,
        )


if __name__ == "__main__":
    main()
