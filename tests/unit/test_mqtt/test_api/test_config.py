import pytest

import enapter


def test_plaintext_config_from_env() -> None:
    env = {
        "ENAPTER_MQTT_API_HOST": "mqtt.example.com",
        "ENAPTER_MQTT_API_PORT": "8883",
        "ENAPTER_MQTT_API_USER": "testuser",
        "ENAPTER_MQTT_API_PASSWORD": "testpass",
    }
    config = enapter.mqtt.api.Config.from_env(env)
    assert config.host == "mqtt.example.com"
    assert config.port == 8883
    assert config.user == "testuser"
    assert config.password == "testpass"
    assert config.tls is None


def test_tls_config_from_env() -> None:
    env = {
        "ENAPTER_MQTT_API_HOST": "mqtt.example.com",
        "ENAPTER_MQTT_API_PORT": "8883",
        "ENAPTER_MQTT_API_TLS_SECRET_KEY": "my_secret_key",
        "ENAPTER_MQTT_API_TLS_CERT": "my_cert",
        "ENAPTER_MQTT_API_TLS_CA_CERT": "my_ca_cert",
    }
    config = enapter.mqtt.api.Config.from_env(env)
    assert config.host == "mqtt.example.com"
    assert config.port == 8883
    assert config.user is None
    assert config.password is None
    assert config.tls is not None
    assert config.tls.secret_key == "my_secret_key"
    assert config.tls.cert == "my_cert"
    assert config.tls.ca_cert == "my_ca_cert"


def test_tls_config_secret_key_missing() -> None:
    env = {
        "ENAPTER_MQTT_API_TLS_CERT": "my_cert",
        "ENAPTER_MQTT_API_TLS_CA_CERT": "my_ca_cert",
    }
    with pytest.raises(KeyError):
        enapter.mqtt.api.TLSConfig.from_env(env)


def test_tls_config_cert_missing() -> None:
    env = {
        "ENAPTER_MQTT_API_TLS_SECRET_KEY": "my_secret_key",
        "ENAPTER_MQTT_API_TLS_CA_CERT": "my_ca_cert",
    }
    with pytest.raises(KeyError):
        enapter.mqtt.api.TLSConfig.from_env(env)


def test_tls_config_ca_cert_missing() -> None:
    env = {
        "ENAPTER_MQTT_API_TLS_SECRET_KEY": "my_secret_key",
        "ENAPTER_MQTT_API_TLS_CERT": "my_cert",
    }
    with pytest.raises(KeyError):
        enapter.mqtt.api.TLSConfig.from_env(env)


def test_tls_config_replace_newlines() -> None:
    env = {
        "ENAPTER_MQTT_API_TLS_SECRET_KEY": "line1\\nline2",
        "ENAPTER_MQTT_API_TLS_CERT": "line1\\nline2",
        "ENAPTER_MQTT_API_TLS_CA_CERT": "line1\\nline2",
    }
    tls_config = enapter.mqtt.api.TLSConfig.from_env(env)
    assert tls_config is not None
    assert tls_config.secret_key == "line1\nline2"
    assert tls_config.cert == "line1\nline2"
    assert tls_config.ca_cert == "line1\nline2"
