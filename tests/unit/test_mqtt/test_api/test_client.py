import enapter


def test_device_channel() -> None:
    client = enapter.mqtt.api.Client(
        enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=8883,
            user="testuser",
            password="testpass",
            tls_config=None,
        )
    )
    channel = client.device_channel("hardware123", "channelABC")
    assert channel.hardware_id == "hardware123"
    assert channel.channel_id == "channelABC"
