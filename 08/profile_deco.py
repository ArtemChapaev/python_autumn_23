from functools import wraps
import cProfile
import pstats
import io


def profile_deco(func):
    profile = cProfile.Profile()

    def print_stat():
        stream = io.StringIO()
        stat = pstats.Stats(profile, stream=stream).sort_stats("cumulative")
        stat.print_stats()
        print(stream.getvalue())

    @wraps(func)
    def wrapper(*args, **kwargs):
        profile.enable()
        result = func(*args, **kwargs)
        profile.disable()
        return result

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    try:
        return a + b
    except TypeError:
        return 0


@profile_deco
def sub(a, b):
    try:
        return a - b
    except TypeError:
        return 0


add(1, 2)
add(4, 5)
sub(1, 5)


add.print_stat()
sub.print_stat()
