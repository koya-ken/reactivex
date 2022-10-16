import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def heavy_func(i):
    print(i,"begin",threading.current_thread(), threading.current_thread().ident)
    time.sleep(1)
    print(i,"end",threading.current_thread(), threading.current_thread().ident)

async def main():
    loop = asyncio.get_running_loop()
    # https://docs.python.org/ja/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
    # https://docs.python.org/ja/3/library/asyncio-eventloop.html
    # https://github.com/python/cpython/blob/928b5f1bdeb4f9ab243ccfdf0aa0ca52839974f9/Lib/asyncio/runners.py#L48-L49
    executor = ThreadPoolExecutor(max_workers=3)
    loop.set_default_executor(executor)
    tasks = [asyncio.to_thread(heavy_func,i) for i in range(10)]
    await asyncio.gather(*tasks)
    tasks = [asyncio.to_thread(heavy_func,i) for i in range(10)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
    # https://github.com/python/cpython/blob/928b5f1bdeb4f9ab243ccfdf0aa0ca52839974f9/Lib/asyncio/runners.py#L51-L52
    asyncio.run(main())
