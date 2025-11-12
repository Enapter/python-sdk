import asyncio

import pytest

import enapter


class TestGenerator:

    async def test_aclose(self) -> None:
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


class TestRoutine:

    async def test_run_not_implemented(self):
        class R(enapter.async_.Routine):
            pass

        with pytest.raises(TypeError):
            R()

    async def test_start_twice(self) -> None:
        started = asyncio.Event()

        class R(enapter.async_.Routine):
            async def _run(self):
                started.set()
                await asyncio.Event().wait()

        async with R() as r:
            await started.wait()
            with pytest.raises(RuntimeError):
                await r.start()

    async def test_stop_without_start(self) -> None:
        class R(enapter.async_.Routine):
            async def _run(self):  # pragma: no cover
                await asyncio.Event().wait()

        r = R()
        with pytest.raises(RuntimeError):
            await r.stop()

    async def test_context_manager(self):
        started = asyncio.Event()
        done = asyncio.Event()

        class R(enapter.async_.Routine):
            async def _run(self):
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    done.set()

        async with R():
            await started.wait()

        assert done.is_set()

    async def test_task_group(self):
        started = asyncio.Event()
        done = asyncio.Event()

        class R(enapter.async_.Routine):
            async def _run(self):
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    done.set()

        async with asyncio.TaskGroup() as tg:
            async with R(task_group=tg):
                await started.wait()

        assert done.is_set()
