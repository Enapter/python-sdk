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


async def test_generator_closes_on_exception_in_context() -> None:
    closed = False

    @enapter.async_.generator
    async def agen():
        nonlocal closed
        try:
            yield 1
            yield 2  # pragma: no cover
        finally:
            closed = True

    with pytest.raises(ValueError, match="Test error"):
        async with agen() as g:
            assert await g.__anext__() == 1
            raise ValueError("Test error")

    assert closed


async def test_generator_raises_exception() -> None:
    @enapter.async_.generator
    async def agen():
        yield 1
        raise ValueError("Generator error")

    async with agen() as g:
        assert await g.__anext__() == 1
        with pytest.raises(ValueError, match="Generator error"):
            await g.__anext__()


async def test_generator_with_args() -> None:
    @enapter.async_.generator
    async def agen(a: int, b: int = 0):
        yield a
        yield b

    async with agen(10, b=20) as g:
        assert await g.__anext__() == 10
        assert await g.__anext__() == 20
