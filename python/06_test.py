import asyncio
import time
import profile
import random

import threading

async def calc(x):
    r = 0
    print(x,threading.current_thread().name)
    for i in range(10**7):
        if random.random() < 0.99:
            r += i % x
    return r

async def main():
    tasks = [asyncio.create_task(calc(i)) for i in range(1, 16)]
    # この書き方がmainの中のthreadも進行できて良い
    # ここになにか処理を書くのがasyncioのプラクティス
    r = [await task for task in tasks]
    print(r)
# https://qiita.com/nardtree/items/68dfeaefc7787e7a114a
start = time.time()
asyncio.run(main())
elapsed = time.time() - start
print(elapsed)