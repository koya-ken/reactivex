import rx
import time
import rx.operators as op
import random
import threading
import asyncio

from rx.subject import Subject
from rx.scheduler import ThreadPoolScheduler,ImmediateScheduler,CurrentThreadScheduler,TrampolineScheduler,NewThreadScheduler
from rx.scheduler.eventloop import AsyncIOScheduler
from rx.scheduler.currentthreadscheduler import CurrentThreadSchedulerSingleton
# https://rxpy.readthedocs.io/en/latest/get_started.html#concurrency

optimal_thread_count = 5
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
pool_scheduler2 = ThreadPoolScheduler(optimal_thread_count)
# main_thread = CurrentThreadScheduler.singleton()
main_thread = ImmediateScheduler()

def woker(x):
    print(x,threading.current_thread().name)
    wt = random.randint(3,10) * 0.1
    time.sleep(wt)
    return x

event = Subject()
a = rx.from_iterable(range(10)).pipe(
    # op.subscribe_on(main_thread),
    op.observe_on(pool_scheduler),
    op.map(lambda x: print("start",x,threading.current_thread().name) or x),
    # op.flat_map(lambda x: rx.just(x).pipe(op.subscribe_on(pool_scheduler),op.map(woker))),
    # op.flat_map(lambda x: rx.just(x).pipe(op.observe_on(pool_scheduler),op.map(woker))),
    op.flat_map(lambda x: rx.just(x).pipe(op.map(woker))),
).subscribe(print,print,print)
print("test")
# a.dispose()
# https://stackoverflow.com/questions/39318723/how-can-i-notify-rxpy-observers-on-separate-threads-using-asyncio