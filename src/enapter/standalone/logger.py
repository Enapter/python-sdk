import asyncio

from .device_protocol import Log


class Logger:

    def __init__(self, queue: asyncio.Queue[Log]) -> None:
        self._queue = queue

    async def debug(self, msg: str, persist: bool = False) -> None:
        await self._queue.put(Log("debug", msg, persist))

    async def info(self, msg: str, persist: bool = False) -> None:
        await self._queue.put(Log("info", msg, persist))

    async def warning(self, msg: str, persist: bool = False) -> None:
        await self._queue.put(Log("warning", msg, persist))

    async def error(self, msg: str, persist: bool = False) -> None:
        await self._queue.put(Log("error", msg, persist))
