import asyncio
import contextlib
from typing import Optional

from enapter import async_, log, mqtt

from .config import Config
from .device import Device
from .device_driver import DeviceDriver
from .ucm import UCM


async def run(device: Device, config_prefix: Optional[str] = None) -> None:
    log.configure(level=log.LEVEL or "info")

    config = Config.from_env(prefix=config_prefix)

    async with App(config=config, device=device) as app:
        await app.join()


class App(async_.Routine):

    def __init__(self, config: Config, device: Device) -> None:
        self._config = config
        self._device = device

    async def _run(self) -> None:
        async with contextlib.AsyncExitStack() as stack:
            mqtt_client = await stack.enter_async_context(
                mqtt.Client(config=self._config.mqtt)
            )
            device_channel = mqtt.api.DeviceChannel(
                client=mqtt_client,
                hardware_id=self._config.hardware_id,
                channel_id=self._config.channel_id,
            )
            _ = await stack.enter_async_context(
                DeviceDriver(device_channel=device_channel, device=self._device)
            )
            if self._config.start_ucm:
                ucm_channel = mqtt.api.DeviceChannel(
                    client=mqtt_client,
                    hardware_id=self._config.hardware_id,
                    channel_id="ucm",
                )
                _ = await stack.enter_async_context(
                    DeviceDriver(device_channel=ucm_channel, device=UCM())
                )
            self._started.set()
            while True:
                await asyncio.sleep(1)
