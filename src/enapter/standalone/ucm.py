import asyncio
from typing import AsyncGenerator

from .device import CommandArgs, CommandResult, Properties, Telemetry


class UCM:

    async def execute_command(self, name: str, args: CommandArgs) -> CommandResult:
        match name:
            case "reboot":
                return await self.reboot()
            case "upload_lua_script":
                return await self.upload_lua_script(**args)
            case _:
                raise NotImplementedError

    async def reboot(self) -> CommandResult:
        raise NotImplementedError

    async def upload_lua_script(
        self, url: str, sha1: str, payload=None
    ) -> CommandResult:
        raise NotImplementedError

    async def send_telemetry(self) -> AsyncGenerator[Telemetry]:
        while True:
            yield {}
            await asyncio.sleep(1)

    async def send_properties(self) -> AsyncGenerator[Properties]:
        while True:
            yield {"virtual": True, "lua_api_ver": 1}
            await asyncio.sleep(30)
