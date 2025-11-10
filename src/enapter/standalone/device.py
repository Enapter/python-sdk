import abc
import asyncio
from typing import AsyncGenerator

from .device_protocol import CommandArgs, CommandResult, Log, Properties, Telemetry
from .logger import Logger


class Device(abc.ABC):

    def __init__(
        self,
        properties_queue_size: int = 1,
        telemetry_queue_size: int = 1,
        log_queue_size: int = 1,
        command_prefix: str = "cmd_",
    ) -> None:
        self._properties_queue: asyncio.Queue[Properties] = asyncio.Queue(
            properties_queue_size
        )
        self._telemetry_queue: asyncio.Queue[Telemetry] = asyncio.Queue(
            telemetry_queue_size
        )
        self._log_queue: asyncio.Queue[Log] = asyncio.Queue(log_queue_size)
        self._logger = Logger(self._log_queue)
        self._command_prefix = command_prefix

    @abc.abstractmethod
    async def run(self) -> None:
        pass

    @property
    def logger(self) -> Logger:
        return self._logger

    async def send_properties(self, properties: Properties) -> None:
        await self._properties_queue.put(properties.copy())

    async def send_telemetry(self, telemetry: Telemetry) -> None:
        await self._telemetry_queue.put(telemetry.copy())

    async def stream_properties(self) -> AsyncGenerator[Properties, None]:
        while True:
            yield await self._properties_queue.get()

    async def stream_telemetry(self) -> AsyncGenerator[Telemetry, None]:
        while True:
            yield await self._telemetry_queue.get()

    async def stream_logs(self) -> AsyncGenerator[Log, None]:
        while True:
            yield await self._log_queue.get()

    async def execute_command(self, name: str, args: CommandArgs) -> CommandResult:
        try:
            command = getattr(self, self._command_prefix + name)
        except AttributeError:
            raise NotImplementedError() from None
        return {"result": await command(**args)}
