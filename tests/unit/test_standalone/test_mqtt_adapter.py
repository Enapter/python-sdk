import asyncio
from typing import Literal
from unittest import mock

import pytest

import enapter


class Device(enapter.standalone.Device):

    def __init__(
        self,
        log_severity: Literal["debug", "info", "warning", "error"] | None = None,
        persist_logs: bool = False,
    ) -> None:
        super().__init__()
        self._log_severity = log_severity
        self._persist_logs = persist_logs

    async def cmd_add(self, a: int, b: int) -> dict:
        return {"sum": a + b}

    async def run(self) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.properties_sender())
            tg.create_task(self.telemetry_sender())
            if self._log_severity is not None:
                tg.create_task(self.logs_sender())

    async def properties_sender(self) -> None:
        while True:
            await self.send_properties({"status": "ok"})
            await asyncio.sleep(0.01)

    async def telemetry_sender(self) -> None:
        while True:
            await self.send_telemetry({"value": 42})
            await asyncio.sleep(0.01)

    async def logs_sender(self) -> None:
        assert self._log_severity is not None
        while True:
            log_method = getattr(self.logger, self._log_severity)
            await log_method("status: ok", persist=self._persist_logs)
            await asyncio.sleep(0.01)


async def test_publish_properties():
    device = Device()
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    mqtt_api_client.device_channel.return_value = device_channel
    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            await asyncio.sleep(0.02)
            device_channel.publish_properties.assert_called()
            last_call = device_channel.publish_properties.call_args
            published_properties = last_call.kwargs["properties"]
            assert published_properties.timestamp > 0
            assert published_properties.values == {"status": "ok"}


async def test_publish_telemetry():
    device = Device()
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    mqtt_api_client.device_channel.return_value = device_channel
    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            await asyncio.sleep(0.02)
            device_channel.publish_telemetry.assert_called()
            last_call = device_channel.publish_telemetry.call_args
            published_telemetry = last_call.kwargs["telemetry"]
            assert published_telemetry.timestamp > 0
            assert published_telemetry.values == {"value": 42}


@pytest.mark.parametrize("persist_logs", [False, True])
@pytest.mark.parametrize("log_severity,", ["debug", "info", "warning", "error"])
async def test_publish_logs(log_severity, persist_logs) -> None:
    device = Device(log_severity=log_severity, persist_logs=persist_logs)
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    mqtt_api_client.device_channel.return_value = device_channel
    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            await asyncio.sleep(0.02)
            device_channel.publish_log.assert_called()
            last_call = device_channel.publish_log.call_args
            published_log = last_call.kwargs["log"]
            assert published_log.timestamp > 0
            assert published_log.severity == enapter.mqtt.api.device.LogSeverity(
                log_severity
            )
            assert published_log.message == "status: ok"
            assert published_log.persist == persist_logs


async def test_publish_properties_exception():
    device = Device()
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    device_channel.publish_properties.side_effect = RuntimeError("Publish error")
    mqtt_api_client.device_channel.return_value = device_channel
    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            await asyncio.sleep(0.02)
            device_channel.publish_properties.assert_called()


async def test_publish_telemetry_exception():
    device = Device()
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    device_channel.publish_telemetry.side_effect = RuntimeError("Publish error")
    mqtt_api_client.device_channel.return_value = device_channel
    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            await asyncio.sleep(0.02)
            device_channel.publish_telemetry.assert_called()


async def test_publish_logs_exception():
    device = Device(log_severity="error")
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    device_channel.publish_log.side_effect = RuntimeError("Publish error")
    mqtt_api_client.device_channel.return_value = device_channel
    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            await asyncio.sleep(0.02)
            device_channel.publish_log.assert_called()


async def test_execute_command():
    device = Device()
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    mqtt_api_client.device_channel.return_value = device_channel

    command_requests = asyncio.Queue()
    command_responses = asyncio.Queue()

    @enapter.async_.generator
    async def subscribe_to_command_requests():
        while True:
            yield await command_requests.get()

    async def publish_command_response(r: enapter.mqtt.api.device.CommandResponse):
        await command_responses.put(r)

    device_channel.subscribe_to_command_requests = subscribe_to_command_requests
    device_channel.publish_command_response = publish_command_response

    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            command_requests.put_nowait(
                enapter.mqtt.api.device.CommandRequest(
                    id="cmd1", name="add", arguments={"a": 2, "b": 3}
                )
            )

            response = await asyncio.wait_for(command_responses.get(), timeout=1.0)
            assert response.id == "cmd1"
            assert response.state == enapter.mqtt.api.device.CommandState.LOG
            assert response.payload == {"message": "Executing command..."}

            response = await asyncio.wait_for(command_responses.get(), timeout=1.0)
            assert response.id == "cmd1"
            assert response.state == enapter.mqtt.api.device.CommandState.COMPLETED
            assert response.payload == {"result": {"sum": 5}}


async def test_execute_command_not_implemented():
    device = Device()
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    mqtt_api_client.device_channel.return_value = device_channel

    command_requests = asyncio.Queue()
    command_responses = asyncio.Queue()

    @enapter.async_.generator
    async def subscribe_to_command_requests():
        while True:
            yield await command_requests.get()

    async def publish_command_response(r: enapter.mqtt.api.device.CommandResponse):
        await command_responses.put(r)

    device_channel.subscribe_to_command_requests = subscribe_to_command_requests
    device_channel.publish_command_response = publish_command_response

    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            command_requests.put_nowait(
                enapter.mqtt.api.device.CommandRequest(
                    id="cmd2", name="non_existing_command", arguments={}
                )
            )

            response = await asyncio.wait_for(command_responses.get(), timeout=1.0)
            assert response.id == "cmd2"
            assert response.state == enapter.mqtt.api.device.CommandState.LOG
            assert response.payload == {"message": "Executing command..."}

            response = await asyncio.wait_for(command_responses.get(), timeout=1.0)
            assert response.id == "cmd2"
            assert response.state == enapter.mqtt.api.device.CommandState.ERROR
            assert response.payload == {"message": "Command handler not implemented."}


async def test_execute_command_exception():
    device = Device()
    mqtt_api_client = mock.AsyncMock(spec=enapter.mqtt.api.Client)
    device_channel = mock.AsyncMock(spec=enapter.mqtt.api.device.Channel)
    mqtt_api_client.device_channel.return_value = device_channel

    command_requests = asyncio.Queue()
    command_responses = asyncio.Queue()

    @enapter.async_.generator
    async def subscribe_to_command_requests():
        while True:
            yield await command_requests.get()

    async def publish_command_response(r: enapter.mqtt.api.device.CommandResponse):
        await command_responses.put(r)

    device_channel.subscribe_to_command_requests = subscribe_to_command_requests
    device_channel.publish_command_response = publish_command_response

    async with asyncio.TaskGroup() as tg:
        async with enapter.standalone.mqtt_adapter.MQTTAdapter(
            hardware_id="hardware123",
            channel_id="channelABC",
            mqtt_api_client=mqtt_api_client,
            device=device,
            task_group=tg,
        ):
            command_requests.put_nowait(
                enapter.mqtt.api.device.CommandRequest(
                    id="cmd3", name="add", arguments={"a": "invalid", "b": 3}
                )
            )

            response = await asyncio.wait_for(command_responses.get(), timeout=1.0)
            assert response.id == "cmd3"
            assert response.state == enapter.mqtt.api.device.CommandState.LOG
            assert response.payload == {"message": "Executing command..."}

            response = await asyncio.wait_for(command_responses.get(), timeout=1.0)
            assert response.id == "cmd3"
            assert response.state == enapter.mqtt.api.device.CommandState.ERROR
            assert "Traceback" in response.payload["message"]
