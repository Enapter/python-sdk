import contextlib
import functools


def generator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        return contextlib.aclosing(gen)

    return wrapper
