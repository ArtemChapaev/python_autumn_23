from itertools import chain
from typing import Callable


def custom_gen(*args, drop_filter: Callable = None, repeat_filter: Callable = None):
    iterables = []
    for arg in args:
        try:
            iter(arg)
        except TypeError:
            iterables.append([arg])
        else:
            iterables.append(arg)

    generalize_list = chain(*iterables)

    for value in generalize_list:
        if drop_filter is not None:
            if drop_filter(value):
                continue

        if repeat_filter is not None:
            for _ in range(repeat_filter(value)):
                yield value
        else:
            yield value


print(list(custom_gen([1, 2], 3, range(4, 6), {6: 6, 7: 7}, "89")) == [1, 2, 3, 4, 5, 6, 7, '8', '9'])

print(
    list(custom_gen([1, 2], 3, range(4, 6), {6: 6, 7: 7}, "89", drop_filter=lambda x: x == 6))
    == [1, 2, 3, 4, 5, 7, '8', '9']
)

print(
    list(custom_gen([1, 2], 3, range(4, 6), {6: 6, 7: 7}, "89", repeat_filter=lambda x: 3 if x == 5 else 1))
    == [1, 2, 3, 4, 5, 5, 5, 6, 7, '8', '9']
)

print()

