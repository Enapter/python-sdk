import dataclasses
from typing import AsyncGenerator, Awaitable, Callable, Generic, TypeVar

from enapter import async_

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class Page(Generic[T]):
    items: list[T]
    total_count: int


@async_.generator
async def paginate(
    fetch: Callable[[int], Awaitable[Page[T]]],
    offset: int,
    limit: int | None,
) -> AsyncGenerator[T, None]:
    if limit == 0:
        return

    if limit is not None and limit < 0:
        limit = None

    yielded_count = 0
    total_count: int | None = None

    while True:
        current_offset = offset + yielded_count

        if total_count is not None and current_offset >= total_count:
            break

        page = await fetch(current_offset)
        total_count = page.total_count

        if not page.items:
            break

        for item in page.items:
            yield item
            yielded_count += 1
            if limit is not None and yielded_count >= limit:
                return
