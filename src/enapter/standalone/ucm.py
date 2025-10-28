import asyncio
from typing import AsyncGenerator

from .device import CommandResult, Device, Properties, Telemetry


class UCM(Device):

    async def reboot(self) -> CommandResult:
        raise NotImplementedError

    async def upload_lua_script(
        self, url: str, sha1: str, payload=None
    ) -> CommandResult:
        raise NotImplementedError

    async def send_telemetry(self) -> AsyncGenerator[Telemetry, None]:
        while True:
            yield {}
            await asyncio.sleep(1)

    async def send_properties(self) -> AsyncGenerator[Properties, None]:
        while True:
            yield {"virtual": True, "lua_api_ver": 1}
            await asyncio.sleep(30)
