from functools import wraps
import cProfile
import pstats
import io


def profile_deco(func):
    _stats = []

    def print_stat():
        for stat in _stats:
            print(stat)

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.print_stat = print_stat

        profile = cProfile.Profile()
        profile.enable()
        result = func(*args, **kwargs)
        profile.disable()

        stream = io.StringIO()
        stat = pstats.Stats(profile, stream=stream).sort_stats("cumulative")
        stat.print_stats()
        _stats.append(stream.getvalue())

        return result
    return wrapper


# @profile_deco
# def add(a, b):
#     return a + b
#
#
# @profile_deco
# def sub(a, b):
#     return a - b
#
#
# add(1, 2)
# add(4, 5)
# sub(4, 5)
#
#
# add.print_stat()
# sub.print_stat()
