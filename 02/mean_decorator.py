import time


def mean(k: int):
    if not isinstance(k, int):
        raise TypeError("k must be int")

    def mean_inner(func):
        last_calls_time = []

        def inner(*args, **kwargs):
            start_ts = time.time()
            res = func(*args, **kwargs)
            end_ts = time.time()

            nonlocal last_calls_time
            if (len(last_calls_time)) == k:
                last_calls_time.pop(0)

            last_calls_time.append(end_ts - start_ts)
            print(f"Mean time of executing of {func.__name__} is {sum(last_calls_time) / len(last_calls_time)}")

            return res
        return inner
    return mean_inner
