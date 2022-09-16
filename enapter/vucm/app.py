import asyncio

from .. import async_, log, mqtt
from .config import Config
from .ucm import UCM


async def run(device_factory):
    config = Config.from_env()

    async with App(config=config, device_factory=device_factory) as app:
        await app.join()


class App(async_.Routine):
    def __init__(self, config, device_factory):
        self._config = config
        self._device_factory = device_factory

    async def _run(self):
        logger = log.new(level=self._config.log_level)

        mqtt_client = await self._stack.enter_async_context(
            mqtt.Client(logger=logger, config=self._config.mqtt)
        )

        ucm = await self._stack.enter_async_context(
            UCM(mqtt_client=mqtt_client, hardware_id=self._config.hardware_id)
        )

        device = await self._stack.enter_async_context(
            self._device_factory(
                channel=mqtt_client.device_channel(
                    hardware_id=self._config.hardware_id,
                    channel_id=self._config.channel_id,
                )
            )
        )

        self._started.set()

        await asyncio.wait(
            {mqtt_client.task(), ucm.task(), device.task()},
            return_when=asyncio.FIRST_COMPLETED,
        )
