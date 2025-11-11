import abc
import asyncio
import contextlib
from typing import Self


class Routine(abc.ABC):

    def __init__(self, task_group: asyncio.TaskGroup | None) -> None:
        self._task_group = task_group
        self._task: asyncio.Task | None = None

    @abc.abstractmethod
    async def _run(self) -> None:
        pass

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, *_) -> None:
        await self.stop()

    async def start(self) -> None:
        if self._task is not None:
            raise RuntimeError("already started")
        if self._task_group is None:
            self._task = asyncio.create_task(self._run())
        else:
            self._task = self._task_group.create_task(self._run())

    async def stop(self) -> None:
        if self._task is None:
            raise RuntimeError("not started yet")
        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
