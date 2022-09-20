import asyncio

from .device import Device


class UCM(Device):
    def __init__(self, mqtt_client, hardware_id):
        super().__init__(
            channel=mqtt_client.device_channel(
                hardware_id=hardware_id, channel_id="ucm"
            )
        )

    async def cmd_reboot(self):
        await asyncio.sleep(0)
        raise NotImplementedError

    async def cmd_upload_lua_script(self, url, sha1, payload=None):
        await asyncio.sleep(0)
        raise NotImplementedError

    async def task_telemetry_publisher(self):
        while True:
            await self.send_telemetry()
            await asyncio.sleep(1)

    async def task_properties_publisher(self):
        while True:
            await self.send_properties({"virtual": True, "lua_api_ver": 1})
            await asyncio.sleep(10)
