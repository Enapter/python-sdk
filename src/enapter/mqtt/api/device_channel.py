import logging
from typing import AsyncContextManager, AsyncGenerator

from enapter import async_, mqtt

from .command_request import CommandRequest
from .command_response import CommandResponse
from .log import Log
from .properties import Properties
from .telemetry import Telemetry

LOGGER = logging.getLogger(__name__)


class DeviceChannel:

    def __init__(self, client: mqtt.Client, hardware_id: str, channel_id: str) -> None:
        self._client = client
        self._logger = self._new_logger(hardware_id, channel_id)
        self._hardware_id = hardware_id
        self._channel_id = channel_id

    @property
    def hardware_id(self) -> str:
        return self._hardware_id

    @property
    def channel_id(self) -> str:
        return self._channel_id

    @staticmethod
    def _new_logger(hardware_id: str, channel_id: str) -> logging.LoggerAdapter:
        extra = {"hardware_id": hardware_id, "channel_id": channel_id}
        return logging.LoggerAdapter(LOGGER, extra=extra)

    @async_.generator
    async def subscribe_to_command_requests(
        self,
    ) -> AsyncGenerator[CommandRequest, None]:
        async with self._subscribe("v1/command/requests") as messages:
            async for msg in messages:
                assert isinstance(msg.payload, str) or isinstance(msg.payload, bytes)
                yield CommandRequest.from_json(msg.payload)

    async def publish_command_response(self, response: CommandResponse) -> None:
        await self._publish("v1/command/responses", response.to_json())

    async def publish_telemetry(self, telemetry: Telemetry, **kwargs) -> None:
        await self._publish("v1/telemetry", telemetry.to_json(), **kwargs)

    async def publish_properties(self, properties: Properties, **kwargs) -> None:
        await self._publish("v1/register", properties.to_json(), **kwargs)

    async def publish_log(self, log: Log, **kwargs) -> None:
        await self._publish("v3/logs", log.to_json(), **kwargs)

    def _subscribe(
        self, path: str
    ) -> AsyncContextManager[AsyncGenerator[mqtt.Message, None]]:
        topic = f"v1/to/{self._hardware_id}/{self._channel_id}/{path}"
        return self._client.subscribe(topic)

    async def _publish(self, path: str, payload: str, **kwargs) -> None:
        topic = f"v1/from/{self._hardware_id}/{self._channel_id}/{path}"
        try:
            await self._client.publish(topic, payload, **kwargs)
        except Exception as e:
            self._logger.error("failed to publish %s: %r", path, e)
