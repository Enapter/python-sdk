import pytest

import enapter


class TestGenerator:

    async def test_aclose(self) -> None:
        @enapter.async_.generator
        async def agen():
            yield 1
            yield 2
            yield 3

        async with agen() as g:
            assert await g.__anext__() == 1
            assert await g.__anext__() == 2

        with pytest.raises(StopAsyncIteration):
            await g.__anext__()
