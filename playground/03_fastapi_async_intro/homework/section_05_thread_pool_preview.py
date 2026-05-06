"""
阶段 3 补充专题 · 第 2 小节动手题：ThreadPoolExecutor 处理同步阻塞 PDF 预览

作业目标：
1. 练习在 async 函数里使用 loop.run_in_executor(...)
2. 练习给 run_in_executor 传多个位置参数
3. 练习使用 functools.partial 给同步函数传关键字参数

业务背景：
FlowRAG 以后可能需要“上传 PDF 后立刻返回前几页预览”。
假设第三方 PDF 库只有同步阻塞接口，这时不能在 async def 里直接调用它，
而应该把它交给线程池执行。
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial


thread_pool = ThreadPoolExecutor(max_workers=3)


def read_pdf_metadata_sync(file_path: str, delay_seconds: float) -> dict:
    """
    模拟同步阻塞 PDF SDK：读取 PDF 元信息。
    这个函数不需要你改。
    """
    time.sleep(delay_seconds)
    return {
        "file_path": file_path,
        "page_count": 12,
        "title": "FlowRAG 入门文档",
    }


def render_pdf_preview_sync(
    file_path: str,
    page_no: int,
    quality: str,
    delay_seconds: float,
) -> dict:
    """
    模拟同步阻塞 PDF SDK：渲染某一页预览图。
    这个函数不需要你改。
    """
    time.sleep(delay_seconds)
    return {
        "file_path": file_path,
        "page_no": page_no,
        "quality": quality,
        "preview_path": f"/tmp/previews/{file_path}-page-{page_no}.png",
    }


async def build_pdf_preview_response(file_path: str) -> dict:
    """
    TODO:
    1. 使用 asyncio.get_running_loop() 获取当前事件循环。
    2. 用 loop.run_in_executor(...) 把 read_pdf_metadata_sync 丢进 thread_pool。
       要求：这里用位置参数传 file_path 和 delay_seconds。
    3. 用 functools.partial 包装 render_pdf_preview_sync。
       要求：这里用关键字参数传 file_path、page_no、quality、delay_seconds。
    4. 用 loop.run_in_executor(...) 把包装后的 preview task 丢进 thread_pool。
    5. 用 await asyncio.gather(...) 等两个结果。
    6. 返回下面这种结构：

       {
           "file_path": "...",
           "metadata": {...},
           "preview": {...},
       }

    注意：
    - 这里两个同步函数都模拟耗时 0.2 秒。
    - 如果你写对了，总耗时应该明显小于 0.4 秒。
    """
    # 在这里完成你的代码
    loop = asyncio.get_running_loop()
    task_1 = loop.run_in_executor(
        thread_pool,
        read_pdf_metadata_sync,
        file_path,
        0.2
    )
    preview_task = partial(
        render_pdf_preview_sync,
        file_path=file_path,
        page_no=1,
        quality="thumbnail",
        delay_seconds=0.2
    )
    task_2 = loop.run_in_executor(
        thread_pool,
        preview_task
    )
    result_1, result_2 = await asyncio.gather(
        task_1,
        task_2
    )
    return {
           "file_path": file_path,
           "metadata": result_1,
           "preview": result_2,
    }


async def self_check() -> None:
    start = time.perf_counter()
    result = await build_pdf_preview_response("demo.pdf")
    elapsed = time.perf_counter() - start

    assert result["file_path"] == "demo.pdf"
    assert result["metadata"]["page_count"] == 12
    assert result["preview"]["page_no"] == 1
    assert result["preview"]["quality"] == "thumbnail"
    assert elapsed < 0.35, f"耗时过长，可能没有并发丢进线程池：{elapsed:.3f}s"

    print("thread pool preview homework looks good")
    print(f"elapsed: {elapsed:.3f}s")


if __name__ == "__main__":
    asyncio.run(self_check())
