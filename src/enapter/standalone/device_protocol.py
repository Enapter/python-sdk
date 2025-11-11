import dataclasses
from typing import Any, AsyncGenerator, Literal, Protocol, TypeAlias

Properties: TypeAlias = dict[str, Any]
Telemetry: TypeAlias = dict[str, Any]
CommandArgs: TypeAlias = dict[str, Any]
CommandResult: TypeAlias = dict[str, Any]


@dataclasses.dataclass
class Log:

    severity: Literal["debug", "info", "warning", "error"]
    message: str
    persist: bool


class DeviceProtocol(Protocol):

    async def run(self) -> None:
        pass

    async def stream_properties(self) -> AsyncGenerator[Properties, None]:
        yield {}

    async def stream_telemetry(self) -> AsyncGenerator[Telemetry, None]:
        yield {}

    async def stream_logs(self) -> AsyncGenerator[Log, None]:
        yield Log("debug", "", False)

    async def execute_command(self, name: str, args: CommandArgs) -> CommandResult:
        pass
