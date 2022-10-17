import contextlib
import functools


def generator(func):
    @functools.wraps(func)
    @contextlib.asynccontextmanager
    async def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        try:
            yield gen
        finally:
            await gen.aclose()

    return wrapper
