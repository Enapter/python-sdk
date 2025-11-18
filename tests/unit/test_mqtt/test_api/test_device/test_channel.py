from unittest import mock

import enapter


async def test_subscribe_to_command_requests() -> None:
    @enapter.async_.generator
    async def subscribe(topic: str):
        assert (
            topic
            == "v1/to/6BAA9455E3E70682C2094CAC629F6FBED82C07CD/main/v1/command/requests"
        )
        yield enapter.mqtt.Message(
            topic=topic,
            payload='{"id": "bbe17a10-3107-47cb-b0ec-99648debade6", "name": "my_command", "arguments": {"foo": "bar"}}',
            qos=0,
            retain=False,
            mid=1,
            properties=None,
        )

    mock_client = mock.AsyncMock()
    mock_client.subscribe = subscribe
    channel = enapter.mqtt.api.device.Channel(
        client=mock_client,
        hardware_id="6BAA9455E3E70682C2094CAC629F6FBED82C07CD",
        channel_id="main",
    )
    async with channel.subscribe_to_command_requests() as requests:
        request = await requests.__anext__()
        assert request == enapter.mqtt.api.device.CommandRequest(
            id="bbe17a10-3107-47cb-b0ec-99648debade6",
            name="my_command",
            arguments={"foo": "bar"},
        )


async def test_publish_command_response() -> None:
    mock_client = mock.AsyncMock()
    channel = enapter.mqtt.api.device.Channel(
        client=mock_client,
        hardware_id="6BAA9455E3E70682C2094CAC629F6FBED82C07CD",
        channel_id="main",
    )
    await channel.publish_command_response(
        enapter.mqtt.api.device.CommandResponse(
            id="bbe17a10-3107-47cb-b0ec-99648debade6",
            state=enapter.mqtt.api.device.CommandState.COMPLETED,
            payload={"foo": "bar"},
        )
    )
    mock_client.publish.assert_called_once_with(
        "v1/from/6BAA9455E3E70682C2094CAC629F6FBED82C07CD/main/v1/command/responses",
        '{"id": "bbe17a10-3107-47cb-b0ec-99648debade6", "state": "completed", "payload": {"foo": "bar"}}',
    )


async def test_publish_telemetry() -> None:
    mock_client = mock.AsyncMock()
    channel = enapter.mqtt.api.device.Channel(
        client=mock_client,
        hardware_id="6BAA9455E3E70682C2094CAC629F6FBED82C07CD",
        channel_id="main",
    )
    await channel.publish_telemetry(
        enapter.mqtt.api.device.Telemetry(
            timestamp=1234567890, alerts=["aaa"], values={"foo": "bar"}
        )
    )
    mock_client.publish.assert_called_once_with(
        "v1/from/6BAA9455E3E70682C2094CAC629F6FBED82C07CD/main/v1/telemetry",
        '{"timestamp": 1234567890, "alerts": ["aaa"], "foo": "bar"}',
    )


async def test_publish_properties() -> None:
    mock_client = mock.AsyncMock()
    channel = enapter.mqtt.api.device.Channel(
        client=mock_client,
        hardware_id="6BAA9455E3E70682C2094CAC629F6FBED82C07CD",
        channel_id="main",
    )
    await channel.publish_properties(
        enapter.mqtt.api.device.Properties(timestamp=1234567890, values={"foo": "bar"})
    )
    mock_client.publish.assert_called_once_with(
        "v1/from/6BAA9455E3E70682C2094CAC629F6FBED82C07CD/main/v1/register",
        '{"timestamp": 1234567890, "foo": "bar"}',
    )


async def test_publish_log() -> None:
    mock_client = mock.AsyncMock()
    channel = enapter.mqtt.api.device.Channel(
        client=mock_client,
        hardware_id="6BAA9455E3E70682C2094CAC629F6FBED82C07CD",
        channel_id="main",
    )
    await channel.publish_log(
        enapter.mqtt.api.device.Log(
            timestamp=1234567890,
            severity=enapter.mqtt.api.device.LogSeverity.INFO,
            message="Test log",
            persist=False,
        )
    )
    mock_client.publish.assert_called_once_with(
        "v1/from/6BAA9455E3E70682C2094CAC629F6FBED82C07CD/main/v3/logs",
        '{"timestamp": 1234567890, "message": "Test log", "severity": "info", "persist": false}',
    )
