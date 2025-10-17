from unittest import mock

import enapter


class TestDeviceChannel:
    async def test_publish_telemetry(self, fake):
        hardware_id = fake.hardware_id()
        channel_id = fake.channel_id()
        timestamp = fake.timestamp()
        mock_client = mock.Mock()
        device_channel = enapter.mqtt.api.DeviceChannel(
            client=mock_client, hardware_id=hardware_id, channel_id=channel_id
        )
        await device_channel.publish_telemetry(
            enapter.mqtt.api.Telemetry(timestamp=timestamp)
        )
        mock_client.publish.assert_called_once_with(
            f"v1/from/{hardware_id}/{channel_id}/v1/telemetry",
            '{"timestamp": ' + str(timestamp) + "}",
        )

    async def test_publish_properties(self, fake):
        hardware_id = fake.hardware_id()
        channel_id = fake.channel_id()
        timestamp = fake.timestamp()
        mock_client = mock.Mock()
        device_channel = enapter.mqtt.api.DeviceChannel(
            client=mock_client, hardware_id=hardware_id, channel_id=channel_id
        )
        await device_channel.publish_properties(
            enapter.mqtt.api.Properties(timestamp=timestamp)
        )
        mock_client.publish.assert_called_once_with(
            f"v1/from/{hardware_id}/{channel_id}/v1/register",
            '{"timestamp": ' + str(timestamp) + "}",
        )
