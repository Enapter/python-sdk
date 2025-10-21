import asyncio
import contextlib
import time
import traceback

from enapter import async_, mqtt

from .device import Device


class DeviceDriver(async_.Routine):

    def __init__(self, device_channel: mqtt.api.DeviceChannel, device: Device) -> None:
        self._device_channel = device_channel
        self._device = device

    async def _run(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._send_properties())
            tg.create_task(self._send_telemetry())
            tg.create_task(self._execute_commands())
            self._started.set()

    async def _send_properties(self) -> None:
        async with contextlib.aclosing(self._device.send_properties()) as iterator:
            async for properties in iterator:
                properties = properties.copy()
                timestamp = properties.pop("timestamp", int(time.time()))
                await self._device_channel.publish_properties(
                    properties=mqtt.api.Properties(
                        timestamp=timestamp, values=properties
                    )
                )

    async def _send_telemetry(self) -> None:
        async with contextlib.aclosing(self._device.send_telemetry()) as iterator:
            async for telemetry in iterator:
                telemetry = telemetry.copy()
                timestamp = telemetry.pop("timestamp", int(time.time()))
                alerts = telemetry.pop("alerts", None)
                await self._device_channel.publish_telemetry(
                    telemetry=mqtt.api.Telemetry(
                        timestamp=timestamp, alerts=alerts, values=telemetry
                    )
                )

    async def _execute_commands(self) -> None:
        async with asyncio.TaskGroup() as tg:
            async with self._device_channel.subscribe_to_command_requests() as requests:
                async for request in requests:
                    tg.create_task(self._execute_command(request))

    async def _execute_command(self, request: mqtt.api.CommandRequest) -> None:
        await self._device_channel.publish_command_response(
            request.new_response(
                mqtt.api.CommandState.LOG, {"message": "Executing command..."}
            )
        )
        try:
            payload = await self._device.execute_command(
                request.name, request.arguments
            )
        except NotImplementedError:
            await self._device_channel.publish_command_response(
                request.new_response(
                    mqtt.api.CommandState.ERROR,
                    {"message": "Command handler not implemented."},
                )
            )
        except Exception:
            await self._device_channel.publish_command_response(
                request.new_response(
                    mqtt.api.CommandState.ERROR, {"message": traceback.format_exc()}
                )
            )
        else:
            if payload is None:
                payload = {}
            await self._device_channel.publish_command_response(
                request.new_response(mqtt.api.CommandState.COMPLETED, payload)
            )
