import json
import logging
import time
from typing import Any, AsyncContextManager, AsyncGenerator, Dict

import aiomqtt  # type: ignore

import enapter

from ..client import Client
from .command import CommandRequest, CommandResponse
from .log_severity import LogSeverity

LOGGER = logging.getLogger(__name__)


class DeviceChannel:
    def __init__(self, client: Client, hardware_id: str, channel_id: str) -> None:
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
    def _new_logger(hardware_id, channel_id) -> logging.LoggerAdapter:
        extra = {"hardware_id": hardware_id, "channel_id": channel_id}
        return logging.LoggerAdapter(LOGGER, extra=extra)

    @enapter.async_.generator
    async def subscribe_to_command_requests(
        self,
    ) -> AsyncGenerator[CommandRequest, None]:
        async with self._subscribe("v1/command/requests") as messages:
            async for msg in messages:
                assert isinstance(msg.payload, str) or isinstance(msg.payload, bytes)
                yield CommandRequest.unmarshal_json(msg.payload)

    async def publish_command_response(self, resp: CommandResponse) -> None:
        await self._publish_json("v1/command/responses", resp.json())

    async def publish_telemetry(self, telemetry: Dict[str, Any], **kwargs) -> None:
        await self._publish_json("v1/telemetry", telemetry, **kwargs)

    async def publish_properties(self, properties: Dict[str, Any], **kwargs) -> None:
        await self._publish_json("v1/register", properties, **kwargs)

    async def publish_logs(
        self, msg: str, severity: LogSeverity, persist: bool = False, **kwargs
    ) -> None:
        logs = {
            "message": msg,
            "severity": severity.value,
            "persist": persist,
        }
        await self._publish_json("v3/logs", logs, **kwargs)

    def _subscribe(
        self, path: str
    ) -> AsyncContextManager[AsyncGenerator[aiomqtt.Message, None]]:
        topic = f"v1/to/{self._hardware_id}/{self._channel_id}/{path}"
        return self._client.subscribe(topic)

    async def _publish_json(
        self, path: str, json_object: Dict[str, Any], **kwargs
    ) -> None:
        if "timestamp" not in json_object:
            json_object["timestamp"] = int(time.time())
        payload = json.dumps(json_object)
        await self._publish(path, payload, **kwargs)

    async def _publish(self, path: str, payload: str, **kwargs) -> None:
        topic = f"v1/from/{self._hardware_id}/{self._channel_id}/{path}"
        try:
            await self._client.publish(topic, payload, **kwargs)
        except Exception as e:
            self._logger.error("failed to publish %s: %r", path, e)
