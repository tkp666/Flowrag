import asyncio
import time


# 第 3 阶段 · 第 1 小节动手题
#
# 本题重点：
# 1. 亲眼看到 async def 调用后先得到的是“协程对象”，不是返回值
# 2. 亲手区分 time.sleep() 和 await asyncio.sleep()
# 3. 亲手比较“同步顺序等待”和“异步并发等待”的总耗时
#
# 你要完成的内容：
# 1. 补完 sync_task
# 2. 补完 async_task
# 3. 补完 run_sync_demo
# 4. 补完 run_async_demo
# 5. 补完 main 里的 3 个观察点
# 6. 补完底部 3 个文字回答
#
# 自查方式：
# 1. 运行：
#    python section_01_async_basics_compare.py
# 2. 你应该至少观察到：
#    - 直接调用 async_task(...) 打印出来的是协程对象，不是最终结果
#    - 同步版 3 个 2 秒任务总耗时接近 6 秒
#    - 异步版 3 个 2 秒任务总耗时接近 2 秒


def sync_task(name: str, delay: int) -> str:
    """
    同步任务：
    - 打印开始
    - 用 time.sleep(delay) 等待
    - 打印结束
    - 返回一个字符串结果
    """
    print(f"{name} start")
    time.sleep(delay)
    print(f"{name} end")
    return f"{name} done"


async def async_task(name: str, delay: int) -> str:
    """
    异步任务：
    - 打印开始
    - 用 await asyncio.sleep(delay) 等待
    - 打印结束
    - 返回一个字符串结果
    """
    print(f"{name} start")
    await asyncio.sleep(delay)
    print(f"{name} end")
    return f"{name} done"


def run_sync_demo() -> None:
    """
    这里要顺序执行 3 个同步任务：
    - sync_task("sync-1", 2)
    - sync_task("sync-2", 2)
    - sync_task("sync-3", 2)

    要求：
    - 记录开始时间和结束时间
    - 打印 3 个返回值
    - 打印总耗时，格式类似：
      sync cost: 6.00
    """
    start = time.time()

    r1 = sync_task("sync-1", 2)
    r2 = sync_task("sync-2", 2)
    r3 = sync_task("sync-3", 2)

    end = time.time()
    print(r1, r2, r3)
    print("cost:", end - start)


async def run_async_demo() -> None:
    """
    这里要并发等待 3 个异步任务：
    - async_task("async-1", 2)
    - async_task("async-2", 2)
    - async_task("async-3", 2)

    要求：
    - 使用 asyncio.gather(...)
    - 记录开始时间和结束时间
    - 打印 3 个返回值
    - 打印总耗时，格式类似：
      async cost: 2.00
    """
    start = time.time()

    r1, r2, r3 = await asyncio.gather(
        async_task("async-1", 2),
        async_task("async-2", 2),
        async_task("async-3", 2),
    )

    end = time.time()
    print(r1, r2, r3)
    print("cost:", end - start)


async def main() -> None:
    print("=== part 1: 直接调用 async def 会得到什么 ===")
    coroutine_obj = async_task("preview", 1)
    # TODO:
    # 1. 打印 coroutine_obj
    # 2. 用 await coroutine_obj 真正执行它
    # 3. 打印 await 后拿到的结果
    print(coroutine_obj)
    result = await coroutine_obj
    print("result = ", result)

    print("\n=== part 2: 同步顺序等待 ===")
    run_sync_demo()

    print("\n=== part 3: 异步并发等待 ===")
    await run_async_demo()


# 文字回答区：
#
# 1. 为什么 direct call 的 async_task(...) 打印出来不是最终结果？
# 答：只是创建协程对象，不会自动执行
#
# 2. 为什么同步版 3 个 2 秒任务总耗时大约是 6 秒，而异步版大约是 2 秒？
# 答：同步版的每个都会等待2秒，所以是六秒。异步版的在等待的时候会把控制权让给别的协程，向当于几乎每个协程都同时开始了2秒的倒计时，因此大约就是两秒
#
# 3. 这个实验里异步真正提升的是什么：单个任务速度，还是多个等待能重叠？
# 答：多个等待能重叠


if __name__ == "__main__":
    asyncio.run(main())
