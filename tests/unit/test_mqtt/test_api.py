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
        await device_channel.publish_telemetry({"timestamp": timestamp})
        mock_client.publish.assert_called_once_with(
            f"v1/from/{hardware_id}/{channel_id}/v1/telemetry",
            '{"timestamp": ' + str(timestamp) + "}",
        )

    async def test_publish_telemetry_without_timestamp(self, fake):
        hardware_id = fake.hardware_id()
        channel_id = fake.channel_id()
        timestamp = fake.timestamp()
        mock_client = mock.Mock()
        device_channel = enapter.mqtt.api.DeviceChannel(
            client=mock_client, hardware_id=hardware_id, channel_id=channel_id
        )
        with mock.patch("time.time") as mock_time:
            mock_time.return_value = timestamp
            await device_channel.publish_telemetry({})
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
        await device_channel.publish_properties({"timestamp": timestamp})
        mock_client.publish.assert_called_once_with(
            f"v1/from/{hardware_id}/{channel_id}/v1/register",
            '{"timestamp": ' + str(timestamp) + "}",
        )

    async def test_publish_properties_without_timestamp(self, fake):
        hardware_id = fake.hardware_id()
        channel_id = fake.channel_id()
        timestamp = fake.timestamp()
        mock_client = mock.Mock()
        device_channel = enapter.mqtt.api.DeviceChannel(
            client=mock_client, hardware_id=hardware_id, channel_id=channel_id
        )
        with mock.patch("time.time") as mock_time:
            mock_time.return_value = timestamp
            await device_channel.publish_properties({})
        mock_client.publish.assert_called_once_with(
            f"v1/from/{hardware_id}/{channel_id}/v1/register",
            '{"timestamp": ' + str(timestamp) + "}",
        )
