import concurrent.futures
import time

import rx
from rx import operators as ops
import random
import threading
import os

seconds = [(i,random.randint(5,10) * 0.1)  for i in range(10)]

# https://github.com/ReactiveX/RxPY/blob/master/examples/parallel/timer.py


def sleep(tm):
    print(tm[0],os.getpid(), threading.current_thread().name)
    time.sleep(tm[1])
    return tm


def output(result):
    print(f'{result} seconds')
    print(os.getpid(), threading.current_thread().name)

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(2) as executor:
        print("main",os.getpid())
        rx.from_(seconds).pipe(
            ops.flat_map(lambda s: executor.submit(sleep, s))
        ).subscribe(output)

# 1 seconds
# 2 seconds
# 3 seconds
# 4 seconds
# 5 seconds