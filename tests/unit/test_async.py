import asyncio

import pytest

import enapter


class TestGenerator:
    async def test_aclose(self):
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


class TestRoutine:
    async def test_run_not_implemented(self):
        class R(enapter.async_.Routine):
            pass

        with pytest.raises(TypeError):
            R()

    async def test_context_manager(self):
        done = asyncio.Event()

        class R(enapter.async_.Routine):
            async def _run(self):
                self._started.set()
                await asyncio.sleep(0)
                done.set()

        async with R():
            await asyncio.sleep(0)

        await asyncio.wait_for(done.wait(), 1)

    async def test_task_getter(self):
        can_exit = asyncio.Event()

        class R(enapter.async_.Routine):
            async def _run(self):
                self._started.set()
                await asyncio.wait_for(can_exit.wait(), 1)

        async with R() as r:
            assert not r.task().done()
            can_exit.set()

        assert r.task().done()

    async def test_started_fine(self):
        done = asyncio.Event()

        class R(enapter.async_.Routine):
            async def _run(self):
                await asyncio.sleep(0)
                self._started.set()
                await asyncio.sleep(0)
                done.set()
                await asyncio.sleep(10)

        r = R()
        await r.start(cancel_parent_task_on_exception=False)
        try:
            await asyncio.wait_for(done.wait(), 1)
        finally:
            await r.stop()

    async def test_finished_after_started(self):
        class R(enapter.async_.Routine):
            async def _run(self):
                self._started.set()
                await asyncio.sleep(0)

        r = R()
        await r.start(cancel_parent_task_on_exception=False)
        await asyncio.wait_for(r.join(), 1)

    async def test_finished_before_started(self):
        class R(enapter.async_.Routine):
            async def _run(self):
                await asyncio.sleep(0)

        r = R()
        await r.start(cancel_parent_task_on_exception=False)
        await asyncio.wait_for(r.join(), 1)

    async def test_failed_before_started(self):
        class R(enapter.async_.Routine):
            async def _run(self):
                await asyncio.sleep(0)
                raise RuntimeError()

        r = R()
        with pytest.raises(RuntimeError):
            await r.start(cancel_parent_task_on_exception=False)

    async def test_failed_after_started(self):
        can_fail = asyncio.Event()

        class R(enapter.async_.Routine):
            async def _run(self):
                self._started.set()
                await asyncio.wait_for(can_fail.wait(), 1)
                raise RuntimeError()

        r = R()
        await r.start(cancel_parent_task_on_exception=False)
        can_fail.set()
        with pytest.raises(RuntimeError):
            await r.join()

    async def test_cancel_parent_task_on_exception_after_started(self):
        can_fail = asyncio.Event()

        class R(enapter.async_.Routine):
            async def _run(self):
                self._started.set()
                await asyncio.wait_for(can_fail.wait(), 1)
                raise RuntimeError()

        r = R()

        async def parent():
            await r.start()
            can_fail.set()
            with pytest.raises(asyncio.CancelledError):
                await asyncio.wait_for(asyncio.sleep(2), 1)

        parent_task = asyncio.create_task(parent())
        await parent_task

        with pytest.raises(RuntimeError):
            await r.join()

    async def test_do_not_cancel_parent_task_on_exception_before_started(self):
        class R(enapter.async_.Routine):
            async def _run(self):
                raise RuntimeError()

        r = R()
        with pytest.raises(RuntimeError):
            await r.start()
