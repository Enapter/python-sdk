import asyncio

import pytest

import enapter


async def test_run_not_implemented() -> None:
    class R(enapter.async_.Routine):
        pass

    with pytest.raises(TypeError):
        R()  # type: ignore


async def test_start_twice() -> None:
    started = asyncio.Event()

    class R(enapter.async_.Routine):
        async def _run(self) -> None:
            started.set()
            await asyncio.Event().wait()

    async with R() as r:
        await started.wait()
        with pytest.raises(RuntimeError):
            await r.start()


async def test_stop_without_start() -> None:
    class R(enapter.async_.Routine):
        async def _run(self) -> None:
            await asyncio.Event().wait()  # pragma: no cover

    r = R()
    with pytest.raises(RuntimeError):
        await r.stop()


async def test_context_manager() -> None:
    started = asyncio.Event()
    done = asyncio.Event()

    class R(enapter.async_.Routine):
        async def _run(self) -> None:
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                done.set()

    async with R():
        await started.wait()

    assert done.is_set()


async def test_task_group() -> None:
    started = asyncio.Event()
    done = asyncio.Event()

    class R(enapter.async_.Routine):
        async def _run(self) -> None:
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                done.set()

    async with asyncio.TaskGroup() as tg:
        async with R(task_group=tg):
            await started.wait()

    assert done.is_set()
