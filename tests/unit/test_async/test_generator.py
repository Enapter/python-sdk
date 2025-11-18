import pytest

import enapter


async def test_aclose() -> None:
    @enapter.async_.generator
    async def agen():
        yield 1
        yield 2
        yield 3  # pragma: no cover

    async with agen() as g:
        assert await g.__anext__() == 1
        assert await g.__anext__() == 2

    with pytest.raises(StopAsyncIteration):
        await g.__anext__()
