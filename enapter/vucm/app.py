import asyncio

from .. import async_, log, mqtt
from .config import Config
from .ucm import UCM


async def run(device_factory):
    log.configure(level=log.LEVEL or "info")

    config = Config.from_env()

    async with App(config=config, device_factory=device_factory) as app:
        await app.join()


class App(async_.Routine):
    def __init__(self, config, device_factory):
        self._config = config
        self._device_factory = device_factory

    async def _run(self):
        tasks = set()

        mqtt_client = await self._stack.enter_async_context(
            mqtt.Client(config=self._config.mqtt)
        )
        tasks.add(mqtt_client.task())

        if self._config.start_ucm:
            ucm = await self._stack.enter_async_context(
                UCM(mqtt_client=mqtt_client, hardware_id=self._config.hardware_id)
            )
            tasks.add(ucm.task())

        device = await self._stack.enter_async_context(
            self._device_factory(
                channel=mqtt_client.device_channel(
                    hardware_id=self._config.hardware_id,
                    channel_id=self._config.channel_id,
                )
            )
        )
        tasks.add(device.task())

        self._started.set()

        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
