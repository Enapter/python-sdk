import abc
from typing import Any, AsyncGenerator, Dict, TypeAlias

from .logger import Log, Logger

Properties: TypeAlias = Dict[str, Any]
Telemetry: TypeAlias = Dict[str, Any]
CommandArgs: TypeAlias = Dict[str, Any]
CommandResult: TypeAlias = Dict[str, Any]


class Device(abc.ABC):

    def __init__(self) -> None:
        self.logger = Logger()

    @abc.abstractmethod
    async def send_properties(self) -> AsyncGenerator[Properties]:
        yield {}

    @abc.abstractmethod
    async def send_telemetry(self) -> AsyncGenerator[Telemetry]:
        yield {}

    async def send_logs(self) -> AsyncGenerator[Log]:
        while True:
            yield await self.logger.queue.get()

    async def execute_command(self, name: str, args: CommandArgs) -> CommandResult:
        try:
            command = getattr(self, name)
        except AttributeError:
            raise NotImplementedError() from None
        result = await command(**args)
        return result if result is not None else {}
