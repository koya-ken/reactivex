import asyncio
import threading
import time

def heavy_func(i):
    print(i,"begin",threading.current_thread(), threading.current_thread().ident)
    time.sleep(1)
    print(i,"end",threading.current_thread(), threading.current_thread().ident)

async def main():
    tasks = [asyncio.to_thread(heavy_func,i) for i in range(10)]
    await asyncio.gather(*tasks)
    tasks = [asyncio.to_thread(heavy_func,i) for i in range(10)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
