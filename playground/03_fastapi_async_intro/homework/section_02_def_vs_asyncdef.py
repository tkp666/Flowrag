import asyncio
import time


# 第 3 阶段 · 第 2 小节动手题
#
# 本题重点：
# 1. 让你区分 FastAPI 里“写成 async def”和“真正有异步收益”不是一回事
# 2. 比较 3 种风格：
#    - 普通 def + time.sleep
#    - async def + time.sleep
#    - async def + await asyncio.sleep
#
# 你要完成的内容：
# 1. 补完 sync_route_like
# 2. 补完 fake_async_but_blocking
# 3. 补完 real_async_route_like
# 4. 补完 main() 里的 3 组调用
# 5. 补完底部 3 个文字回答
#
# 自查方式：
# 1. 运行：
#    python section_02_def_vs_asyncdef.py
# 2. 你应该至少看到：
#    - sync_route_like 和 fake_async_but_blocking 单次都是大约 2 秒
#    - 两个 real_async_route_like 并发等待时，总耗时接近 2 秒
#    - 你会直观看到：async def + time.sleep 并不会自动带来异步收益


def sync_route_like(name: str, delay: int) -> str:
    """
    模拟一个同步风格接口：
    - 打印开始
    - 用 time.sleep(delay)
    - 打印结束
    - 返回结果字符串
    """
    print(f"{name} start!")
    time.sleep(delay)
    print(f"{name} end!")
    return (f"{name} done!")


async def fake_async_but_blocking(name: str, delay: int) -> str:
    """
    模拟一个“看起来是 async def，但里面仍然阻塞”的接口：
    - 打印开始
    - 用 time.sleep(delay) 进行阻塞等待
    - 打印结束
    - 返回结果字符串
    """
    print(f"{name} start!")
    time.sleep(delay)
    print(f"{name} end!")
    return (f"{name} done!")


async def real_async_route_like(name: str, delay: int) -> str:
    """
    模拟一个真正有异步等待价值的接口：
    - 打印开始
    - 用 await asyncio.sleep(delay)
    - 打印结束
    - 返回结果字符串
    """
    print(f"{name} start!")
    await asyncio.sleep(delay)
    print(f"{name} end!")
    return (f"{name} done!")


async def main() -> None:
    print("=== part 1: 普通 def + time.sleep ===")
    # TODO:
    # 1. 记录开始时间
    # 2. 顺序调用两次 sync_route_like("sync-a", 2) 和 sync_route_like("sync-b", 2)
    # 3. 打印总耗时，格式类似：
    #    sync total cost: 4.00
    start = time.time()
    sync_route_like("sync-a", 2)
    sync_route_like("sync-b", 2)
    end = time.time()
    print("sync total cost: ", end - start)

    print("\n=== part 2: async def + time.sleep（仍然阻塞） ===")
    # TODO:
    # 1. 记录开始时间
    # 2. 顺序 await 两次 fake_async_but_blocking("fake-a", 2) 和 fake_async_but_blocking("fake-b", 2)
    # 3. 打印总耗时，格式类似：
    #    fake async total cost: 4.00
    start = time.time()
    await fake_async_but_blocking("fake-a", 2)
    await fake_async_but_blocking("fake-b", 2)
    end = time.time()
    print("fake async total cost: ", end - start)

    print("\n=== part 3: async def + await asyncio.sleep（真正异步等待） ===")
    # TODO:
    # 1. 记录开始时间
    # 2. 用 asyncio.gather(...) 并发等待：
    #    - real_async_route_like("real-a", 2)
    #    - real_async_route_like("real-b", 2)
    # 3. 打印总耗时，格式类似：
    #    real async total cost: 2.00
    start = time.time()
    await asyncio.gather(
        real_async_route_like("real-a", 2),
        real_async_route_like("real-b", 2)
    )
    end = time.time()
    print("real async total cost: ", end - start)


# 文字回答区：
#
# 1. 为什么 `async def + time.sleep` 看起来是异步函数，但总耗时仍然像同步一样？
# 答：因为他没有用 asyncio.sleep,相当于还是没有放开控制权，单个协程在死等时间结束
#
# 2. 为什么 `async def + await asyncio.sleep` 更能体现异步等待的价值？
# 答：因为放开了控制权，可以在等待的过程中调用其他协程运行
#
# 3. 如果一个 FastAPI 路由里主要调用的都是阻塞式函数，你会优先考虑直接写 `def` 还是硬写 `async def`？为什么？
# 答：def。async def对于阻塞式函数起不到任何作用


if __name__ == "__main__":
    asyncio.run(main())
