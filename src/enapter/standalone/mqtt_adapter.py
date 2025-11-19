import asyncio
import contextlib
import logging
import time
import traceback

from enapter import async_, mqtt

from .device_protocol import DeviceProtocol

LOGGER = logging.getLogger(__name__)


class MQTTAdapter(async_.Routine):

    def __init__(
        self,
        hardware_id: str,
        channel_id: str,
        mqtt_api_client: mqtt.api.Client,
        device: DeviceProtocol,
        task_group: asyncio.TaskGroup | None,
    ) -> None:
        super().__init__(task_group=task_group)
        self._logger = logging.LoggerAdapter(
            LOGGER, extra={"hardware_id": hardware_id, "channel_id": channel_id}
        )
        self._device_channel = mqtt_api_client.device_channel(hardware_id, channel_id)
        self._device = device

    async def _run(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._device.run())
            tg.create_task(self._stream_properties())
            tg.create_task(self._stream_telemetry())
            tg.create_task(self._stream_logs())
            tg.create_task(self._execute_commands())

    async def _stream_properties(self) -> None:
        async with contextlib.aclosing(self._device.stream_properties()) as stream:
            async for properties in stream:
                properties = properties.copy()
                timestamp = properties.pop("timestamp", int(time.time()))
                await self._publish_properties(
                    mqtt.api.device.Properties(timestamp=timestamp, values=properties)
                )

    async def _publish_properties(self, properties: mqtt.api.device.Properties) -> None:
        try:
            await self._device_channel.publish_properties(properties=properties)
        except Exception as e:
            self._logger.error("failed to publish properties: %s", e)

    async def _stream_telemetry(self) -> None:
        async with contextlib.aclosing(self._device.stream_telemetry()) as stream:
            async for telemetry in stream:
                telemetry = telemetry.copy()
                timestamp = telemetry.pop("timestamp", int(time.time()))
                alerts = telemetry.pop("alerts", None)
                await self._publish_telemetry(
                    mqtt.api.device.Telemetry(
                        timestamp=timestamp, alerts=alerts, values=telemetry
                    )
                )

    async def _publish_telemetry(self, telemetry: mqtt.api.device.Telemetry) -> None:
        try:
            await self._device_channel.publish_telemetry(telemetry=telemetry)
        except Exception as e:
            self._logger.error("failed to publish telemetry: %s", e)

    async def _stream_logs(self) -> None:
        async with contextlib.aclosing(self._device.stream_logs()) as stream:
            async for log in stream:
                match log.severity:
                    case "debug":
                        self._logger.debug(log.message)
                    case "info":
                        self._logger.info(log.message)
                    case "warning":
                        self._logger.warning(log.message)
                    case "error":
                        self._logger.error(log.message)
                    case _:  # pragma: no cover
                        raise NotImplementedError(log.severity)  # pragma: no cover
                await self._publish_log(
                    mqtt.api.device.Log(
                        timestamp=int(time.time()),
                        severity=mqtt.api.device.LogSeverity(log.severity),
                        message=log.message,
                        persist=log.persist,
                    )
                )

    async def _publish_log(self, log: mqtt.api.device.Log) -> None:
        try:
            await self._device_channel.publish_log(log=log)
        except Exception as e:
            self._logger.error("failed to publish log: %s", e)

    async def _execute_commands(self) -> None:
        async with asyncio.TaskGroup() as tg:
            async with self._device_channel.subscribe_to_command_requests() as requests:
                async for request in requests:
                    tg.create_task(self._execute_command(request))

    async def _execute_command(self, request: mqtt.api.device.CommandRequest) -> None:
        await self._device_channel.publish_command_response(
            request.new_response(
                mqtt.api.device.CommandState.LOG, {"message": "Executing command..."}
            )
        )
        try:
            payload = await self._device.execute_command(
                request.name, request.arguments
            )
        except NotImplementedError:
            await self._device_channel.publish_command_response(
                request.new_response(
                    mqtt.api.device.CommandState.ERROR,
                    {"message": "Command handler not implemented."},
                )
            )
        except Exception:
            await self._device_channel.publish_command_response(
                request.new_response(
                    mqtt.api.device.CommandState.ERROR,
                    {"message": traceback.format_exc()},
                )
            )
        else:
            await self._device_channel.publish_command_response(
                request.new_response(mqtt.api.device.CommandState.COMPLETED, payload)
            )
