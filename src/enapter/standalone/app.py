import asyncio
from typing import Optional

from enapter import log, mqtt

from .config import Config
from .device import Device
from .device_driver import DeviceDriver
from .ucm import UCM


async def run(device: Device, config_prefix: Optional[str] = None) -> None:
    log.configure(level=log.LEVEL or "info")

    config = Config.from_env(prefix=config_prefix)

    try:
        async with asyncio.TaskGroup() as tg:
            _ = App(task_group=tg, config=config, device=device)
    except asyncio.CancelledError:
        pass


class App:

    def __init__(
        self, task_group: asyncio.TaskGroup, config: Config, device: Device
    ) -> None:
        self._config = config
        self._device = device
        self._task = task_group.create_task(self._run())

    async def _run(self) -> None:
        async with asyncio.TaskGroup() as tg:
            mqtt_client = mqtt.Client(task_group=tg, config=self._config.mqtt)
            _ = DeviceDriver(
                task_group=tg,
                device_channel=mqtt.api.DeviceChannel(
                    client=mqtt_client,
                    hardware_id=self._config.hardware_id,
                    channel_id=self._config.channel_id,
                ),
                device=self._device,
            )
            if self._config.start_ucm:
                _ = DeviceDriver(
                    task_group=tg,
                    device_channel=mqtt.api.DeviceChannel(
                        client=mqtt_client,
                        hardware_id=self._config.hardware_id,
                        channel_id="ucm",
                    ),
                    device=UCM(),
                )
