import time


def mean(k: int):
    if not isinstance(k, int):
        raise TypeError("k must be int")

    def mean_inner(func):
        def inner(*args, **kwargs):
            full_time = 0
            for _ in range(k):
                start_ts = time.time()
                func(*args, **kwargs)
                end_ts = time.time()
                delta_time = end_ts - start_ts
                full_time += delta_time

            print(f"Mean time of executing of {func.__name__} is {full_time / k}")
        return inner
    return mean_inner
