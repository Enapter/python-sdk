import unittest.mock

import pytest

import enapter


class TestDeviceChannel:
    async def test_publish_telemetry_timestamp_field_is_reserved(self, fake):
        mock_client = unittest.mock.Mock()
        device_channel = enapter.mqtt.DeviceChannel(
            client=mock_client,
            hardware_id=fake.hardware_id(),
            channel_id=fake.channel_id(),
        )
        with pytest.raises(ValueError):
            await device_channel.publish_telemetry({"timestamp": fake.timestamp()})

    async def test_publish_properties_timestamp_field_is_reserved(self, fake):
        mock_client = unittest.mock.Mock()
        device_channel = enapter.mqtt.DeviceChannel(
            client=mock_client,
            hardware_id=fake.hardware_id(),
            channel_id=fake.channel_id(),
        )
        with pytest.raises(ValueError):
            await device_channel.publish_properties({"timestamp": fake.timestamp()})
