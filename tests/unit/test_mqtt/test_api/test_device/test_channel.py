from unittest import mock

import enapter
import tests


async def test_publish_telemetry(fake: tests.FakeDataGenerator) -> None:
    hardware_id = fake.hardware_id()
    channel_id = fake.channel_id()
    timestamp = fake.timestamp()
    mock_client = mock.AsyncMock()
    channel = enapter.mqtt.api.device.Channel(
        client=mock_client, hardware_id=hardware_id, channel_id=channel_id
    )
    await channel.publish_telemetry(
        enapter.mqtt.api.device.Telemetry(timestamp=timestamp)
    )
    mock_client.publish.assert_called_once_with(
        f"v1/from/{hardware_id}/{channel_id}/v1/telemetry",
        '{"timestamp": ' + str(timestamp) + ', "alerts": null}',
    )


async def test_publish_properties(fake: tests.FakeDataGenerator) -> None:
    hardware_id = fake.hardware_id()
    channel_id = fake.channel_id()
    timestamp = fake.timestamp()
    mock_client = mock.AsyncMock()
    channel = enapter.mqtt.api.device.Channel(
        client=mock_client, hardware_id=hardware_id, channel_id=channel_id
    )
    await channel.publish_properties(
        enapter.mqtt.api.device.Properties(timestamp=timestamp)
    )
    mock_client.publish.assert_called_once_with(
        f"v1/from/{hardware_id}/{channel_id}/v1/register",
        '{"timestamp": ' + str(timestamp) + "}",
    )
