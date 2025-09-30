import contextlib
import functools
from typing import AsyncContextManager, AsyncGenerator, Callable


def generator(
    func: Callable[..., AsyncGenerator],
) -> Callable[..., AsyncContextManager[AsyncGenerator]]:
    @functools.wraps(func)
    @contextlib.asynccontextmanager
    async def wrapper(*args, **kwargs) -> AsyncGenerator[AsyncGenerator, None]:
        gen = func(*args, **kwargs)
        try:
            yield gen
        finally:
            await gen.aclose()

    return wrapper
