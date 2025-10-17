import asyncio
from typing import Optional, Protocol

from enapter import async_, log, mqtt

from .config import Config
from .device import Device
from .ucm import UCM


class DeviceFactory(Protocol):

    def __call__(self, channel: mqtt.api.DeviceChannel, **kwargs) -> Device:
        pass


async def run(
    device_factory: DeviceFactory, config_prefix: Optional[str] = None
) -> None:
    log.configure(level=log.LEVEL or "info")

    config = Config.from_env(prefix=config_prefix)

    async with App(config=config, device_factory=device_factory) as app:
        await app.join()


class App(async_.Routine):
    def __init__(self, config: Config, device_factory: DeviceFactory) -> None:
        self._config = config
        self._device_factory = device_factory

    async def _run(self) -> None:
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
                channel=mqtt.api.DeviceChannel(
                    client=mqtt_client,
                    hardware_id=self._config.hardware_id,
                    channel_id=self._config.channel_id,
                )
            )
        )
        tasks.add(device.task())

        self._started.set()

        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
