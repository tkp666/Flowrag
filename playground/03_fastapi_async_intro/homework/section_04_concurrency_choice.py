"""
阶段 3 补充专题 · 第 1 小节动手题：并发工具选型判断

本题不是让你重复写 FastAPI 路由，也不是照抄 asyncio.gather。
重点是：看到一个 FlowRAG 场景后，先判断该优先考虑 async、线程池、进程池还是 Celery。

可选答案：
- ASYNC_IO：当前请求要等结果，且主要是异步 I/O 等待
- THREAD_POOL：当前请求要等结果，但手里是阻塞式 I/O 库
- PROCESS_POOL：当前请求要等结果，且主要是 CPU 重计算
- CELERY_BACKGROUND：当前请求不该等完，应该后台执行并返回 task_id

自查方式：
1. 运行：
   python section_04_concurrency_choice.py
2. 如果格式完整，你会看到：
   concurrency choice answers are complete

注意：
- 这个脚本只检查你有没有完成和答案值是否合法；
- 你的选型是否合理，需要发给 Codex 检查。
"""


ASYNC_IO = "async_io"
THREAD_POOL = "thread_pool"
PROCESS_POOL = "process_pool"
CELERY_BACKGROUND = "celery_background"


SCENARIOS = {
    "case_1": (
        "聊天接口需要调用外部 LLM API，当前请求必须拿到回答后返回。"
        "所用 HTTP 客户端支持 async/await。"
    ),
    "case_2": (
        "文档详情页需要立即预览 PDF 前 2 页文字。"
        "当前请求必须返回预览结果，但 PDF 解析库只有同步阻塞 API。"
    ),
    "case_3": (
        "用户上传 200 篇 PDF 后，系统要解析、切块、生成 embedding、入库。"
        "当前请求只需要快速返回 task_id。"
    ),
    "case_4": (
        "某个接口必须立即返回一张图片的 OCR 结果。"
        "OCR 主要消耗本机 CPU。"
    ),
    "case_5": (
        "知识库首页需要同时展示用户信息、知识库统计、最近任务状态。"
        "这三类数据互不依赖，且当前页面要一起返回。"
    ),
    "case_6": (
        "系统每晚凌晨重建整个知识库的 embedding 索引。"
        "不需要任何用户请求一直等待它完成。"
    ),
}


ANSWERS = {
    # TODO: 把每个 case 的 choice 改成上面 4 个常量之一。
    # TODO: reason 用 1-2 句话说明原因，不要只写“因为它适合”。
    "case_1": {"choice": "async_io", "reason": "需要返回的结果，且是IO动作"},
    "case_2": {"choice": "thread_pool", "reason": "会被阻塞的IO占用，且需要返回的结果"},
    "case_3": {"choice": "celery_background", "reason": "不需要立即返回结果且运行时间较长"},
    "case_4": {"choice": "process_pool", "reason": "重CPU任务且需要返回结果"},
    "case_5": {"choice": "async_io", "reason": "互不依赖可以使用异步查询，且需要返回的结果"},
    "case_6": {"choice": "celery_background", "reason": "无需立即返回结果且时间较长"},
}


def check_answers() -> None:
    valid_choices = {
        ASYNC_IO,
        THREAD_POOL,
        PROCESS_POOL,
        CELERY_BACKGROUND,
    }

    for case_id in SCENARIOS:
        answer = ANSWERS[case_id]
        choice = answer["choice"]
        reason = answer["reason"].strip()

        if choice not in valid_choices:
            raise ValueError(f"{case_id} 的 choice 还没填对：{choice!r}")
        if len(reason) < 8:
            raise ValueError(f"{case_id} 的 reason 太短，需要写清楚判断依据")

    print("concurrency choice answers are complete")


if __name__ == "__main__":
    check_answers()
