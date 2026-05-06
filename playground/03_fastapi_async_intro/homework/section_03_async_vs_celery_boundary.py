"""
第 3 阶段 · 第 3 小节动手题

本题重点：
- 区分“当前请求里的异步等待”和“应该丢到后台的长任务”
- 区分“async 能解决的问题”和“async 本身解决不了的问题”

你要做的事情：
1. 阅读下面 6 个场景
2. 给每个场景填一个分类
3. 补完底部 3 个文字回答

可选分类只有 3 个：
- ASYNC_REQUEST：适合放在当前请求里，用 async/await 处理 I/O 等待
- CELERY_BACKGROUND：更适合做成后台任务，当前请求先结束
- CPU_NOT_ENOUGH：主要是 CPU 重计算，不能指望 async def 本身解决

自查方式：
1. 运行：
   python section_03_async_vs_celery_boundary.py
2. 如果分类都对，你会看到：
   async/celery boundary looks good
"""


ASYNC_REQUEST = "async_request"
CELERY_BACKGROUND = "celery_background"
CPU_NOT_ENOUGH = "cpu_not_enough"


SCENARIOS = {
    "case_1": "聊天接口调用外部 LLM API，当前请求必须拿到回答后才能返回给用户。",
    "case_2": "用户上传 200 篇文档，系统需要解析、切块、生成 embedding、批量入库，当前请求只需先返回 task_id。",
    "case_3": "某接口必须当前返回 OCR 结果，但 OCR 过程本身是本地 CPU 重计算。",
    "case_4": "接口里需要同时等待两个外部 HTTP API，然后把两个结果拼成一个响应体。",
    "case_5": "后台定时重建整库 embedding，不需要用户当前盯着等结果。",
    "case_6": "接口里只是查一下 Redis、再查一下数据库，然后返回结果给前端。",
}


# 第 3 阶段 · 第 3 小节动手题：
# 你要把每个 case 填成上面 3 个分类之一。
#
# 提示：
# - 当前请求必须等结果，而且主要是 I/O 等待 -> 更像 ASYNC_REQUEST
# - 当前请求不该一直等完，任务很长 -> 更像 CELERY_BACKGROUND
# - 当前请求必须拿结果，但主要瓶颈是 CPU 重计算 -> 更像 CPU_NOT_ENOUGH


case_1 = "async_request"
case_2 = "celery_background"
case_3 = "cpu_not_enough"
case_4 = "async_request"
case_5 = "celery_background"
case_6 = "async_request"


EXPECTED = {
    "case_1": ASYNC_REQUEST,
    "case_2": CELERY_BACKGROUND,
    "case_3": CPU_NOT_ENOUGH,
    "case_4": ASYNC_REQUEST,
    "case_5": CELERY_BACKGROUND,
    "case_6": ASYNC_REQUEST,
}


# 文字回答区：
#
# 1. 为什么“当前请求必须拿到结果”不等于“就一定该用 async def”？
# 答：对于重CPU任务而言，必须拿到结果的，即使用了async def也没用啊
#
# 2. 为什么“任务很长”不等于“只要写成 async def 就行”？
# 答：对于重CPU任务而言，必须拿到结果的，即使用了async def也没用啊。以及可以放在后台运行，不着急拿到结果的，用celery也行
#
# 3. 为什么 Celery 和 async/await 不是替代关系，而是解决不同层面的问题？
# 答：Celery解决的是耗时很长，但是不急着拿到结果的任务   async def解决的主要是IO任务，必须拿到结果，并且可以在等待的时候去做别的事的


def collect_answers() -> dict[str, str]:
    return {
        "case_1": case_1,
        "case_2": case_2,
        "case_3": case_3,
        "case_4": case_4,
        "case_5": case_5,
        "case_6": case_6,
    }


def main() -> None:
    answers = collect_answers()
    valid_choices = {ASYNC_REQUEST, CELERY_BACKGROUND, CPU_NOT_ENOUGH}

    for key, value in answers.items():
        if value not in valid_choices:
            raise ValueError(f"{key} 还没填对分类：{value!r}")

    for key, expected in EXPECTED.items():
        actual = answers[key]
        if actual != expected:
            raise ValueError(
                f"{key} 分错了。当前是 {actual}，正确应为 {expected}。"
            )

    print("async/celery boundary looks good")


if __name__ == "__main__":
    main()
