import time


def mean(k: int):
    if not isinstance(k, int):
        raise TypeError("k must be int")

    def mean_inner(func):
        def inner(*args, **kwargs):
            res = None

            full_time = 0
            for i in range(1, k + 1):
                start_ts = time.time()
                res = func(*args, **kwargs)
                end_ts = time.time()
                delta_time = end_ts - start_ts
                full_time += delta_time
                print(f"Mean time of executing of {func.__name__} is {full_time / i}")

            return res
        return inner
    return mean_inner
