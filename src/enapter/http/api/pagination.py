import dataclasses
import itertools
from typing import AsyncGenerator, Awaitable, Callable, TypeVar

from enapter import async_

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class PageQuery:
    offset: int
    limit: int


@async_.generator
async def paginate(
    fetch_page: Callable[[PageQuery], Awaitable[list[T]]],
    chunk_size: int,
    offset: int,
    limit: int | None,
) -> AsyncGenerator[T, None]:
    if limit == 0:
        return

    if limit is not None and limit < 0:
        limit = None

    yielded_count = 0

    for i in itertools.count():
        query = PageQuery(offset=offset + (i * chunk_size), limit=chunk_size)
        items = await fetch_page(query)

        if not items:
            break

        for item in items:
            if limit is not None and yielded_count >= limit:
                return
            yield item
            yielded_count += 1
