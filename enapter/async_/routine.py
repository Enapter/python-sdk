import abc
import asyncio
import contextlib


class Routine(abc.ABC):
    @abc.abstractmethod
    async def _run(self):
        raise NotImplementedError  # pragma: no cover

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *_):
        await self.stop()

    def task(self):
        return self._task

    async def start(self, cancel_parent_task_on_exception=True):
        self._started = asyncio.Event()
        self._stack = contextlib.AsyncExitStack()

        self._parent_task = asyncio.current_task()
        self._cancel_parent_task_on_exception = cancel_parent_task_on_exception

        self._task = asyncio.create_task(self.__run())
        wait_started_task = asyncio.create_task(self._started.wait())

        done, _ = await asyncio.wait(
            {self._task, wait_started_task},
            return_when=asyncio.FIRST_COMPLETED,
        )

        if wait_started_task not in done:
            wait_started_task.cancel()
        try:
            await wait_started_task
        except asyncio.CancelledError:
            pass

        if self._task in done:
            self._task.result()

    async def stop(self):
        self.cancel()
        await self.join()

    def cancel(self):
        self._task.cancel()

    async def join(self):
        if self._task.done():
            self._task.result()
        else:
            await self._task

    async def __run(self):
        try:
            await self._run()
        except asyncio.CancelledError:
            pass
        except:
            if self._started.is_set() and self._cancel_parent_task_on_exception:
                self._parent_task.cancel()
            raise
        finally:
            await self._stack.aclose()
