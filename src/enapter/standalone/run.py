import asyncio
import contextlib

from enapter import log, mqtt

from .config import Config
from .device_protocol import DeviceProtocol
from .mqtt_adapter import MQTTAdapter
from .ucm import UCM


async def run(device: DeviceProtocol) -> None:
    log.configure(level=log.LEVEL or "info")
    config = Config.from_env()
    async with contextlib.AsyncExitStack() as stack:
        task_group = await stack.enter_async_context(asyncio.TaskGroup())
        mqtt_api_client = await stack.enter_async_context(
            mqtt.api.Client(config=config.communication.mqtt_api, task_group=task_group)
        )
        _ = await stack.enter_async_context(
            MQTTAdapter(
                device_channel=mqtt_api_client.device_channel(
                    hardware_id=config.communication.hardware_id,
                    channel_id=config.communication.channel_id,
                ),
                device=device,
                task_group=task_group,
            )
        )
        if config.communication.ucm_needed:
            _ = await stack.enter_async_context(
                MQTTAdapter(
                    device_channel=mqtt_api_client.device_channel(
                        hardware_id=config.communication.hardware_id,
                        channel_id="ucm",
                    ),
                    device=UCM(),
                    task_group=task_group,
                )
            )
        await asyncio.Event().wait()
