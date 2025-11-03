import asyncio

from .device import Device
from .device_protocol import CommandResult


class UCM(Device):

    async def run(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.properties_sender())
            tg.create_task(self.telemetry_sender())

    async def properties_sender(self) -> None:
        while True:
            await self.send_properties({"virtual": True, "lua_api_ver": 1})
            await asyncio.sleep(30)

    async def telemetry_sender(self) -> None:
        while True:
            await self.send_telemetry({})
            await asyncio.sleep(1)

    async def cmd_reboot(self, *args, **kwargs) -> CommandResult:
        raise NotImplementedError

    async def cmd_upload_lua_script(self, *args, **kwargs) -> CommandResult:
        raise NotImplementedError
