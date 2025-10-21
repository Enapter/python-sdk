from typing import Any, AsyncGenerator, Dict, Optional, Protocol, TypeAlias

Properties: TypeAlias = Dict[str, Any]
Telemetry: TypeAlias = Dict[str, Any]
CommandArgs: TypeAlias = Dict[str, Any]
CommandResult: TypeAlias = Dict[str, Any]


class Device(Protocol):

    async def send_properties(self) -> AsyncGenerator[Properties]:
        yield {}

    async def send_telemetry(self) -> AsyncGenerator[Telemetry]:
        yield {}

    async def execute_command(
        self, name: str, args: CommandArgs
    ) -> Optional[CommandResult]:
        pass
