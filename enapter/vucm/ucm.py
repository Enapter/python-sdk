import asyncio

from .device import Device


class UCM(Device):
    def __init__(self, mqtt_client, hardware_id):
        super().__init__(
            channel=mqtt_client.device_channel(
                hardware_id=hardware_id, channel_id="ucm"
            )
        )

    async def _create_tasks(self):
        return {
            self._telemetry_publisher(),
            self._properties_publisher(),
        }

    async def cmd_reboot(self):
        await asyncio.sleep(0)
        raise NotImplementedError

    async def cmd_upload_lua_script(self, url, sha1, payload=None):
        await asyncio.sleep(0)
        raise NotImplementedError

    async def _telemetry_publisher(self):
        while True:
            await self._channel.publish_telemetry({"alerts": []})
            await asyncio.sleep(1)

    async def _properties_publisher(self):
        while True:
            await self._channel.publish_properties(
                {
                    "virtual": True,
                    "lua_api_ver": 1,
                }
            )
            await asyncio.sleep(10)
