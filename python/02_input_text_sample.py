import rx
import rx.operators as op

rx.from_((input(f'input text[{i+1:00}/10]:') for i in range(10))).pipe(
    op.map(lambda x: 'append:' + x),
    op.debounce(0.5),
    # op.buffer_with_count(2),
    op.map(print)
).run()