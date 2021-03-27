import rx
import rx.operators as op
import threading

# 与えられたものをそのまま
rx.just(3).subscribe(print)
rx.from_list([1,2,3,4]).subscribe(print)
rx.from_iterable([1,2,3,4]).subscribe(print)

# bufferはたまってから処理する
rx.from_iterable(range(10)).pipe(
    op.map(lambda x: x *2),
    op.buffer_with_count(3)
).subscribe(print)

rx.from_iterable(range(10)).pipe(
    op.map(lambda x: x *2),
    op.buffer_with_count(3),
    # ここではリストになっている
    op.map(len)
).subscribe(print)

# windowもたまってから処理するがlistではなくObservableになる
rx.from_iterable(range(10)).pipe(
    op.map(lambda x: x *2),
    op.window_with_count(3),
).subscribe(print)

# observableの中身を1つ1つ処理したい場合はflatmapが使える
rx.from_iterable(range(10)).pipe(
    op.map(lambda x: x *2),
    op.window_with_count(3),
    # ただしこの時点でxはObservable
    # 複数のObservableを1つにまとめる
    op.flat_map(lambda x: x),
    # flat_mapを抜けると要素の型になる
    op.map(lambda x: x / 2)
).subscribe(print,print)


def gen(count: int):
    for i in range(count):
        print('call yield')
        yield i

# generatorの場合すべての処理が終わってから次のものに進む
# bufferは溜まるまで待つので処理自体は進む
# bufferの後ろはbufferがたまってからしか処理されない
rx.from_iterable(gen(10)).pipe(
    op.map(lambda x :print('map call', x) or x),
    op.buffer_with_count(2),
    op.map(print)
).run()

# generator内包表記も同様
rx.from_iterable((print('generator call',i) or i for i in range(10))).pipe(
    op.map(lambda x :print('map call', x) or x),
    op.buffer_with_count(2),
    op.map(print),
).run()

# takeした場合はtake分だけしか呼ばれない
print('call take !!!!!!!!!!')
rx.from_iterable((print('generator call',i) or i for i in range(10))).pipe(
    op.take(1),
    op.map(lambda x :print('map call', x) or x),
    op.buffer_with_count(2),
    op.map(print),
).run()

# take lastした場合はもちろん最後まで呼ばれる
print('call take2 !!!!!!!!!!')
rx.from_iterable((print('generator call',i) or i for i in range(10))).pipe(
    op.take_last(2),
    op.map(lambda x :print('map call', x) or x),
    op.buffer_with_count(2),
    op.map(print),
).run()

# 3こためて先頭の2こを処理
print('call take3 !!!!!!!!!!')
rx.from_iterable((print('generator call',i) or i for i in range(10))).pipe(
    op.window_with_count(3),
    op.flat_map(lambda x: x.pipe(op.take(2))),
    op.map(print),
).run()

# delayはobservableを引数に取りobservableを返す関数
# 引数にobservable以外を渡しても関数は通るが、呼び出すときにエラーになる
print('call take4 !!!!!!!!!!')
rx.from_iterable((print('generator call',i) or i for i in range(10))).pipe(
    op.map(lambda x : op.delay(3)(rx.just(x))),
    # op.window_with_count(1),
    op.flat_map(lambda x:x),
    op.map(print),
).run()

print('=================')
# generatorはrepeatできない
# repeatはもとのoncompletedが来てから最初からやり直す
# repeatをしてできたobservable自体のon completed は1回
rx.from_iterable([1,2,3,4]).pipe(
    op.repeat(3),
    op.map(print),
).subscribe(on_completed=lambda : print('on completed'))