from unittest import mock

import enapter


class TestChannel:

    async def test_publish_telemetry(self, fake) -> None:
        hardware_id = fake.hardware_id()
        channel_id = fake.channel_id()
        timestamp = fake.timestamp()
        mock_client = mock.Mock()
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

    async def test_publish_properties(self, fake) -> None:
        hardware_id = fake.hardware_id()
        channel_id = fake.channel_id()
        timestamp = fake.timestamp()
        mock_client = mock.Mock()
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
