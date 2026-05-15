from typing import AsyncGenerator, Awaitable, Callable, TypeVar

from enapter import async_

T = TypeVar("T")


@async_.generator
async def paginate(
    fetch: Callable[[int], Awaitable[list[T]]],
    offset: int,
    limit: int | None,
) -> AsyncGenerator[T, None]:
    """
    An asynchronous generator for paginating through Enapter API endpoints.

    This utility sequentially fetches pages of items until the server returns an
    empty list or the user-defined `limit` is reached. It calculates the offset
    for each subsequent request dynamically based on the exact number of items
    returned in previous pages.

    Why this design?
    ----------------
    While modern Enapter API endpoints consistently support pagination parameters
    (`offset`, `limit`), legacy deployments of the Gateway Rule Engine do not.

    Crucially, older Rule Engines actively reject unknown query parameters. If an
    `offset` is sent to a legacy Rule Engine, the gateway will return a fatal error
    rather than simply ignoring the parameter. The Rule Engine is the ONLY service
    where this incompatibility exists.

    To safely handle this without crashing, client implementations (specifically
    for the Rule Engine) must utilize a "probe-and-identify" pattern BEFORE delegating
    to this utility.
    """
    if limit == 0:
        return

    if limit is not None and limit < 0:
        limit = None

    yielded_count = 0

    while True:
        items = await fetch(offset + yielded_count)

        if not items:
            break

        for item in items:
            yield item
            yielded_count += 1
            if limit is not None and yielded_count >= limit:
                return
