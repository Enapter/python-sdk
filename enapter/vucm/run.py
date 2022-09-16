import asyncio
import contextlib
import os

from .. import log, mqtt
from .vucm import VUCM


async def run(device_factory):
    logger = log.new(level=os.environ.get("ENAPTER_LOG_LEVEL", "INFO"))
    mqtt_config = mqtt.Config.from_env()

    hardware_id = os.environ["ENAPTER_VUCM_HARDWARE_ID"]
    channel_id = os.environ["ENAPTER_VUCM_CHANNEL_ID"]

    async with contextlib.AsyncExitStack() as stack:
        mqtt_client = await stack.enter_async_context(
            mqtt.Client(logger=logger, config=mqtt_config)
        )
        vucm = await stack.enter_async_context(
            VUCM(
                mqtt_client=mqtt_client,
                device_factory=device_factory,
                hardware_id=hardware_id,
                channel_id=channel_id,
            )
        )
        await asyncio.wait(
            {mqtt_client.task(), vucm.task()},
            return_when=asyncio.FIRST_COMPLETED,
        )
