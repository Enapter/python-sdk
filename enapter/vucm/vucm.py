import asyncio

from .. import async_
from .ucm import UCM


class VUCM(async_.Routine):
    def __init__(self, mqtt_client, device_factory, hardware_id, channel_id):
        self._mqtt_client = mqtt_client
        self._device_factory = device_factory
        self._hardware_id = hardware_id
        self._channel_id = channel_id

    async def _run(self):
        ucm = await self._stack.enter_async_context(
            UCM(mqtt_client=self._mqtt_client, hardware_id=self._hardware_id)
        )
        device = await self._stack.enter_async_context(
            self._device_factory(
                channel=self._mqtt_client.device_channel(
                    hardware_id=self._hardware_id, channel_id=self._channel_id
                )
            )
        )
        await asyncio.wait(
            {ucm.task(), device.task()},
            return_when=asyncio.FIRST_COMPLETED,
        )
