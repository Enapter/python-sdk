import asyncio

import enapter

from .device import Device, device_command, device_task


class UCM(Device):
    def __init__(self, mqtt_client, hardware_id):
        super().__init__(
            channel=enapter.mqtt.api.DeviceChannel(
                client=mqtt_client, hardware_id=hardware_id, channel_id="ucm"
            )
        )

    @device_command
    async def reboot(self):
        await asyncio.sleep(0)
        raise NotImplementedError

    @device_command
    async def upload_lua_script(self, url, sha1, payload=None):
        await asyncio.sleep(0)
        raise NotImplementedError

    @device_task
    async def telemetry_publisher(self) -> None:
        while True:
            await self.send_telemetry()
            await asyncio.sleep(1)

    @device_task
    async def properties_publisher(self):
        while True:
            await self.send_properties({"virtual": True, "lua_api_ver": 1})
            await asyncio.sleep(10)
