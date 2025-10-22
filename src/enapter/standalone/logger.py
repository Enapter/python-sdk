import asyncio
from typing import Literal, Tuple, TypeAlias

Log: TypeAlias = Tuple[Literal["debug", "info", "warning", "error"], str, bool]


class Logger:

    def __init__(self) -> None:
        self._queue: asyncio.Queue[Log] = asyncio.Queue(1)

    async def debug(self, msg: str, persist: bool = False) -> None:
        await self._queue.put(("debug", msg, persist))

    async def info(self, msg: str, persist: bool = False) -> None:
        await self._queue.put(("info", msg, persist))

    async def warning(self, msg: str, persist: bool = False) -> None:
        await self._queue.put(("warning", msg, persist))

    async def error(self, msg: str, persist: bool = False) -> None:
        await self._queue.put(("error", msg, persist))

    @property
    def queue(self) -> asyncio.Queue[Log]:
        return self._queue
