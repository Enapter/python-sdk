import json
import logging
import time

import enapter

from .command import CommandRequest

LOGGER = logging.getLogger(__name__)


class DeviceChannel:
    def __init__(self, client, hardware_id, channel_id):
        self._client = client
        self._logger = self._new_logger(hardware_id, channel_id)
        self._hardware_id = hardware_id
        self._channel_id = channel_id

    @property
    def hardware_id(self):
        return self._hardware_id

    @property
    def channel_id(self):
        return self._channel_id

    @staticmethod
    def _new_logger(hardware_id, channel_id):
        extra = {"hardware_id": hardware_id, "channel_id": channel_id}
        return logging.LoggerAdapter(LOGGER, extra=extra)

    @enapter.async_.generator
    async def subscribe_to_command_requests(self):
        async with self._subscribe("v1/command/requests") as messages:
            async for msg in messages:
                yield CommandRequest.unmarshal_json(msg.payload)

    async def publish_command_response(self, resp):
        await self._publish_json("v1/command/responses", resp.json())

    async def publish_telemetry(self, telemetry, **kwargs):
        await self._publish_json("v1/telemetry", telemetry, **kwargs)

    async def publish_properties(self, properties, **kwargs):
        await self._publish_json("v1/register", properties, **kwargs)

    async def publish_logs(self, msg, severity, persist=False, **kwargs):
        logs = {
            "message": msg,
            "severity": severity.value,
        }
        if persist:
            logs["persist"] = True

        await self._publish_json("v3/logs", logs, **kwargs)

    def _subscribe(self, path):
        topic = f"v1/to/{self._hardware_id}/{self._channel_id}/{path}"
        return self._client.subscribe(topic)

    async def _publish_json(self, path, json_object, **kwargs):
        if "timestamp" not in json_object:
            json_object["timestamp"] = int(time.time())

        payload = json.dumps(json_object)

        await self._publish(path, payload, **kwargs)

    async def _publish(self, path, payload, **kwargs):
        topic = f"v1/from/{self._hardware_id}/{self._channel_id}/{path}"
        try:
            await self._client.publish(topic, payload, **kwargs)
        except Exception as e:
            self._logger.error("failed to publish %s: %r", path, e)
