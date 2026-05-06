"""
阶段 3 补充专题 · 第 3 小节动手题：ProcessPoolExecutor 处理 CPU 密集 chunk 清洗

作业目标：
1. 练习在 async 函数里使用 ProcessPoolExecutor
2. 练习把多个互不依赖的 CPU 任务提交到进程池
3. 练习用 asyncio.gather(...) 等待多个进程池任务

业务背景：
FlowRAG 后续会把文档切成多个 chunk。假设某一步清洗逻辑比较耗 CPU，
并且每个 chunk 之间互不依赖，这时可以考虑用进程池并行处理。

注意：
- 进程池函数应尽量只接收简单参数，比如 int、str、dict、list。
- 不要把 FastAPI request、数据库连接、Redis client、Qdrant client 传进进程池。
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor


def cpu_heavy_clean_chunk(chunk_id: int, text: str, repeat: int) -> dict:
    """
    模拟 CPU 密集文本清洗。
    这个函数不需要你改。

    参数都是简单数据：
    - chunk_id: int
    - text: str
    - repeat: int

    返回值也是简单 dict。
    """
    clean_text = " ".join(text.strip().split())

    checksum = 0
    for ch in clean_text:
        for _ in range(repeat):
            checksum += ord(ch) % 17

    return {
        "chunk_id": chunk_id,
        "clean_text": clean_text,
        "length": len(clean_text),
        "checksum": checksum,
    }


async def build_chunk_cleaning_report(chunks: list[str]) -> dict:
    """
    TODO:
    1. 使用 asyncio.get_running_loop() 获取当前事件循环。
    2. 使用 ProcessPoolExecutor(max_workers=2) 创建进程池。
    3. 遍历 chunks，把每个 chunk 交给 loop.run_in_executor(...)。
       要求：
       - executor 使用 process_pool
       - 函数使用 cpu_heavy_clean_chunk
       - chunk_id 从 1 开始
       - repeat 固定传 3000
    4. 把所有 run_in_executor(...) 返回的任务放进 tasks 列表。
    5. 使用 await asyncio.gather(*tasks) 等待所有结果。
    6. 返回下面这种结构：

       {
           "total": 3,
           "items": [
               {"chunk_id": 1, "clean_text": "...", ...},
               {"chunk_id": 2, "clean_text": "...", ...},
               {"chunk_id": 3, "clean_text": "...", ...},
           ],
       }

    提示：
    先用普通 for 循环写，不要用列表推导式。
    你要练的是看清楚每一步，不是追求写得短。
    """
    # 在这里完成你的代码
    loop = asyncio.get_running_loop()
    process_pool = ProcessPoolExecutor(max_workers=2)
    i = 0
    tasks: list = []
    for chunk in chunks:
        i += 1
        tasks.append(loop.run_in_executor(
            process_pool,
            cpu_heavy_clean_chunk,
            i,
            chunk,
            3000
        ))
    
    results: list = []
    results = await asyncio.gather(*tasks)
    return {
        "total": len(chunks),
        "items": results,
    }
        
        
    


async def self_check() -> None:
    chunks = [
        "  FlowRAG   supports    document   ingestion  ",
        " chunk   cleaning  can be   CPU heavy ",
        " process   pool   handles independent chunks ",
    ]

    result = await build_chunk_cleaning_report(chunks)

    assert result["total"] == 3
    assert len(result["items"]) == 3

    first = result["items"][0]
    second = result["items"][1]
    third = result["items"][2]

    assert first["chunk_id"] == 1
    assert first["clean_text"] == "FlowRAG supports document ingestion"
    assert first["length"] == len("FlowRAG supports document ingestion")
    assert first["checksum"] > 0

    assert second["chunk_id"] == 2
    assert second["clean_text"] == "chunk cleaning can be CPU heavy"
    assert second["checksum"] > 0

    assert third["chunk_id"] == 3
    assert third["clean_text"] == "process pool handles independent chunks"
    assert third["checksum"] > 0

    print("process pool chunks homework looks good")


if __name__ == "__main__":
    asyncio.run(self_check())
