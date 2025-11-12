import asyncio
import contextlib
import time
import traceback

from enapter import async_, mqtt

from .device_protocol import DeviceProtocol


class MQTTAdapter(async_.Routine):

    def __init__(
        self,
        device_channel: mqtt.api.device.Channel,
        device: DeviceProtocol,
        task_group: asyncio.TaskGroup | None,
    ) -> None:
        super().__init__(task_group=task_group)
        self._device_channel = device_channel
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
                await self._device_channel.publish_properties(
                    properties=mqtt.api.device.Properties(
                        timestamp=timestamp, values=properties
                    )
                )

    async def _stream_telemetry(self) -> None:
        async with contextlib.aclosing(self._device.stream_telemetry()) as stream:
            async for telemetry in stream:
                telemetry = telemetry.copy()
                timestamp = telemetry.pop("timestamp", int(time.time()))
                alerts = telemetry.pop("alerts", None)
                await self._device_channel.publish_telemetry(
                    telemetry=mqtt.api.device.Telemetry(
                        timestamp=timestamp, alerts=alerts, values=telemetry
                    )
                )

    async def _stream_logs(self) -> None:
        async with contextlib.aclosing(self._device.stream_logs()) as stream:
            async for log in stream:
                await self._device_channel.publish_log(
                    log=mqtt.api.device.Log(
                        timestamp=int(time.time()),
                        severity=mqtt.api.device.LogSeverity(log.severity),
                        message=log.message,
                        persist=log.persist,
                    )
                )

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
