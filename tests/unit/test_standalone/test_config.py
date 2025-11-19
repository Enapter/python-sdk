import base64
import json

import enapter


def test_communication_config_v1_from_dto():
    assert enapter.standalone.CommunicationConfigV1.from_dto(
        {
            "mqtt_host": "mqtt.example.com",
            "mqtt_port": 8883,
            "mqtt_ca": "my_ca_cert",
            "mqtt_cert": "my_cert",
            "mqtt_private_key": "my_private_key",
            "ucm_id": "hardware123",
            "channel_id": "channelABC",
        }
    ) == enapter.standalone.CommunicationConfigV1(
        mqtt_host="mqtt.example.com",
        mqtt_port=8883,
        mqtt_ca="my_ca_cert",
        mqtt_cert="my_cert",
        mqtt_private_key="my_private_key",
        ucm_id="hardware123",
        channel_id="channelABC",
    )


def test_communication_config_v3_mqtts_from_dto():
    assert enapter.standalone.CommunicationConfigV3.from_dto(
        {
            "mqtt_host": "mqtt.example.com",
            "mqtt_port": 8883,
            "mqtt_protocol": "MQTTS",
            "mqtt_credentials": {
                "private_key": "my_private_key",
                "certificate": "my_cert",
                "ca_chain": "my_ca_cert",
            },
            "hardware_id": "hardware123",
            "channel_id": "channelABC",
        }
    ) == enapter.standalone.CommunicationConfigV3(
        mqtt_host="mqtt.example.com",
        mqtt_port=8883,
        mqtt_protocol=enapter.standalone.CommunicationConfigV3.MQTTProtocol.MQTTS,
        mqtt_credentials=enapter.standalone.CommunicationConfigV3.MQTTSCredentials(
            private_key="my_private_key",
            certificate="my_cert",
            ca_chain="my_ca_cert",
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
    )


def test_communication_config_v3_mqtt_from_dto():
    assert enapter.standalone.CommunicationConfigV3.from_dto(
        {
            "mqtt_host": "mqtt.example.com",
            "mqtt_port": 1883,
            "mqtt_protocol": "MQTT",
            "mqtt_credentials": {
                "username": "testuser",
                "password": "testpass",
            },
            "hardware_id": "hardware123",
            "channel_id": "channelABC",
        }
    ) == enapter.standalone.CommunicationConfigV3(
        mqtt_host="mqtt.example.com",
        mqtt_port=1883,
        mqtt_protocol=enapter.standalone.CommunicationConfigV3.MQTTProtocol.MQTT,
        mqtt_credentials=enapter.standalone.CommunicationConfigV3.MQTTCredentials(
            username="testuser",
            password="testpass",
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
    )


def test_communication_config_from_config_v1():
    config_v1 = enapter.standalone.CommunicationConfigV1(
        mqtt_host="mqtt.example.com",
        mqtt_port=8883,
        mqtt_ca="my_ca_cert",
        mqtt_cert="my_cert",
        mqtt_private_key="my_private_key",
        ucm_id="hardware123",
        channel_id="channelABC",
    )
    config = enapter.standalone.CommunicationConfig.from_config_v1(config_v1)
    assert config == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=8883,
            user=None,
            password=None,
            tls_config=enapter.mqtt.api.TLSConfig(
                secret_key="my_private_key",
                cert="my_cert",
                ca_cert="my_ca_cert",
            ),
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=True,
    )


def test_communication_config_from_config_v3_mqtts():
    config_v3 = enapter.standalone.CommunicationConfigV3(
        mqtt_host="mqtt.example.com",
        mqtt_port=8883,
        mqtt_protocol=enapter.standalone.CommunicationConfigV3.MQTTProtocol.MQTTS,
        mqtt_credentials=enapter.standalone.CommunicationConfigV3.MQTTSCredentials(
            private_key="my_private_key",
            certificate="my_cert",
            ca_chain="my_ca_cert",
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
    )
    config = enapter.standalone.CommunicationConfig.from_config_v3(config_v3)
    assert config == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=8883,
            user=None,
            password=None,
            tls_config=enapter.mqtt.api.TLSConfig(
                secret_key="my_private_key",
                cert="my_cert",
                ca_cert="my_ca_cert",
            ),
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=False,
    )


def test_communication_config_from_config_v3_mqtt():
    config_v3 = enapter.standalone.CommunicationConfigV3(
        mqtt_host="mqtt.example.com",
        mqtt_port=1883,
        mqtt_protocol=enapter.standalone.CommunicationConfigV3.MQTTProtocol.MQTT,
        mqtt_credentials=enapter.standalone.CommunicationConfigV3.MQTTCredentials(
            username="testuser",
            password="testpass",
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
    )
    config = enapter.standalone.CommunicationConfig.from_config_v3(config_v3)
    assert config == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=1883,
            user="testuser",
            password="testpass",
            tls_config=None,
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=False,
    )


def test_communication_config_from_v1_blob():
    blob_v1 = base64.b64encode(
        json.dumps(
            {
                "mqtt_host": "mqtt.example.com",
                "mqtt_port": 8883,
                "mqtt_ca": "my_ca_cert",
                "mqtt_cert": "my_cert",
                "mqtt_private_key": "my_private_key",
                "ucm_id": "hardware123",
                "channel_id": "channelABC",
            }
        ).encode()
    )
    config = enapter.standalone.CommunicationConfig.from_blob(blob_v1)
    assert config == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=8883,
            user=None,
            password=None,
            tls_config=enapter.mqtt.api.TLSConfig(
                secret_key="my_private_key",
                cert="my_cert",
                ca_cert="my_ca_cert",
            ),
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=True,
    )


def test_communication_config_from_v3_blob():
    blob_v3 = base64.b64encode(
        json.dumps(
            {
                "mqtt_host": "mqtt.example.com",
                "mqtt_port": 1883,
                "mqtt_protocol": "MQTT",
                "mqtt_credentials": {
                    "username": "testuser",
                    "password": "testpass",
                },
                "hardware_id": "hardware123",
                "channel_id": "channelABC",
            }
        ).encode()
    )
    config = enapter.standalone.CommunicationConfig.from_blob(blob_v3)
    assert config == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=1883,
            user="testuser",
            password="testpass",
            tls_config=None,
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=False,
    )


def test_communication_config_from_env() -> None:
    blob_v3 = base64.b64encode(
        json.dumps(
            {
                "mqtt_host": "mqtt.example.com",
                "mqtt_port": 1883,
                "mqtt_protocol": "MQTT",
                "mqtt_credentials": {
                    "username": "testuser",
                    "password": "testpass",
                },
                "hardware_id": "hardware123",
                "channel_id": "channelABC",
            }
        ).encode()
    )
    env = {
        "ENAPTER_STANDALONE_COMMUNICATION_CONFIG": blob_v3.decode(),
    }
    config = enapter.standalone.CommunicationConfig.from_env(env)
    assert config == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=1883,
            user="testuser",
            password="testpass",
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=False,
    )


def test_communication_config_from_legacy_vucm_blob():
    blob_v1 = base64.b64encode(
        json.dumps(
            {
                "mqtt_host": "mqtt.example.com",
                "mqtt_port": 8883,
                "mqtt_ca": "my_ca_cert",
                "mqtt_cert": "my_cert",
                "mqtt_private_key": "my_private_key",
                "ucm_id": "hardware123",
                "channel_id": "channelABC",
            }
        ).encode()
    )
    env = {
        "ENAPTER_VUCM_BLOB": blob_v1.decode(),
    }
    config = enapter.standalone.CommunicationConfig.from_env(env)
    assert config == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=8883,
            user=None,
            password=None,
            tls_config=enapter.mqtt.api.TLSConfig(
                secret_key="my_private_key",
                cert="my_cert",
                ca_cert="my_ca_cert",
            ),
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=True,
    )


def test_communication_config_from_env_with_override() -> None:
    blob_v3 = base64.b64encode(
        json.dumps(
            {
                "mqtt_host": "mqtt.example.com",
                "mqtt_port": 1883,
                "mqtt_protocol": "MQTT",
                "mqtt_credentials": {
                    "username": "testuser",
                    "password": "testpass",
                },
                "hardware_id": "hardware123",
                "channel_id": "channelABC",
            }
        ).encode()
    )
    env = {
        "ENAPTER_STANDALONE_COMMUNICATION_CONFIG": blob_v3.decode(),
        "ENAPTER_STANDALONE_COMMUNICATION_OVERRIDE_MQTT_API_HOST": "override.example.com",
    }
    config = enapter.standalone.CommunicationConfig.from_env(env)
    assert config == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="override.example.com",
            port=1883,
            user="testuser",
            password="testpass",
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=False,
    )


def test_config_from_env() -> None:
    blob_v3 = base64.b64encode(
        json.dumps(
            {
                "mqtt_host": "mqtt.example.com",
                "mqtt_port": 1883,
                "mqtt_protocol": "MQTT",
                "mqtt_credentials": {
                    "username": "testuser",
                    "password": "testpass",
                },
                "hardware_id": "hardware123",
                "channel_id": "channelABC",
            }
        ).encode()
    )
    env = {
        "ENAPTER_STANDALONE_COMMUNICATION_CONFIG": blob_v3.decode(),
    }
    config = enapter.standalone.Config.from_env(env)
    assert config.communication == enapter.standalone.CommunicationConfig(
        mqtt_api_config=enapter.mqtt.api.Config(
            host="mqtt.example.com",
            port=1883,
            user="testuser",
            password="testpass",
        ),
        hardware_id="hardware123",
        channel_id="channelABC",
        ucm_needed=False,
    )
