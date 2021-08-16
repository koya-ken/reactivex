import os, glob
import rx
import rx.operators as op
from rx.scheduler import ImmediateScheduler

l = rx.from_iterable(glob.glob('./train/*.png')).pipe(
    op.map(os.path.basename),
    op.map(rx.just),
    op.flat_map(lambda x: x.pipe(
        op.repeat(3),
        op.subscribe_on(ImmediateScheduler()),
        op.map_indexed(lambda x,i: x.replace(".png",f"_{i}.png")),
        ),
    ),
    op.to_list()
).run()

print('=======================take1=======================')
print(l)

print('=======================take2=======================')
l = rx.from_iterable(glob.glob('./train/*.png')).pipe(
    op.map(os.path.basename),
    op.map(rx.just),
    op.map(op.repeat(3)),
    op.map(op.subscribe_on(ImmediateScheduler())),
    # op.flat_map(lambda x : x.pipe(op.map_indexed(lambda x,i: x.replace(".png",f"_{i}.png")))),
    # op.flat_map(lambda x: op.map_indexed(lambda x,i: x.replace(".png",f"_{i}.png"))(x) ),
    # op.flat_map(op.map_indexed(lambda x,i: x.replace(".png",f"_{i}.png"))),
    # op.flat_map(lambda x: print('way',x) or x),
    op.map(lambda x :op.map_indexed(lambda x,i: x.replace(".png",f"_{i}.png"))(x) ),
    op.flat_map(lambda x:x),
    # op.flat_map_indexed(lambda x,i: print(x,i) or x),
    op.map(print)
).run()


print('=======================take3=======================')
l = rx.from_iterable(glob.glob('./train/*.png')).pipe(
    op.map(os.path.basename),
    op.map(rx.just),
    op.map(op.repeat(3)),
    op.map(op.subscribe_on(ImmediateScheduler())),
    op.map(lambda x :op.map_indexed(lambda x,i: x.replace(".png",f"_{i}.png"))(x) ),
    op.flat_map(lambda x:x),
    op.map(print)
).run()


print('=======================take4=======================')
rx.from_iterable(range(3)).pipe(
    op.map(rx.just),
    # op.map(lambda x : op.map_indexed(lambda x, i: (x, i ))(x) ),
    op.flat_map_indexed(lambda x, i: (x, i )),
    op.map(rx.just),
    op.map(op.repeat(3)),
    op.map(op.subscribe_on(ImmediateScheduler())),
    # op.map(op.map_indexed(lambda x, i: (x, i / 0))),
    op.flat_map(lambda x:x),
    op.map(print)
).run()