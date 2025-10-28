import abc
from typing import Any, AsyncGenerator, TypeAlias

from .logger import Log, Logger

Properties: TypeAlias = dict[str, Any]
Telemetry: TypeAlias = dict[str, Any]
CommandArgs: TypeAlias = dict[str, Any]
CommandResult: TypeAlias = dict[str, Any]


class Device(abc.ABC):

    def __init__(self, command_prefix: str = "") -> None:
        self.logger = Logger()
        self.__command_prefix = command_prefix

    @abc.abstractmethod
    async def send_properties(self) -> AsyncGenerator[Properties, None]:
        yield {}

    @abc.abstractmethod
    async def send_telemetry(self) -> AsyncGenerator[Telemetry, None]:
        yield {}

    async def send_logs(self) -> AsyncGenerator[Log, None]:
        while True:
            yield await self.logger.queue.get()

    async def execute_command(self, name: str, args: CommandArgs) -> CommandResult:
        try:
            command = getattr(self, self.__command_prefix + name)
        except AttributeError:
            raise NotImplementedError() from None
        result = await command(**args)
        return result if result is not None else {}
