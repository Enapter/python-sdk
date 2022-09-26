import base64
import json
import os

from .. import mqtt


class Config:
    @classmethod
    def from_env(cls, prefix="ENAPTER_", env=os.environ):
        log_level = os.environ.get(prefix + "LOG_LEVEL", "INFO")
        start_ucm = os.environ.get(prefix + "VUCM_START_UCM", "1") != "0"

        try:
            blob = os.environ[prefix + "VUCM_BLOB"]
        except KeyError:
            pass
        else:
            config = cls.from_blob(log_level=log_level, blob=blob, start_ucm=start_ucm)
            try:
                config.channel_id = os.environ[prefix + "VUCM_CHANNEL_ID"]
            except KeyError:
                pass
            return config

        hardware_id = os.environ[prefix + "VUCM_HARDWARE_ID"]
        channel_id = os.environ[prefix + "VUCM_CHANNEL_ID"]

        mqtt_config = mqtt.Config.from_env(prefix=prefix, env=env)

        return cls(
            log_level=log_level,
            hardware_id=hardware_id,
            channel_id=channel_id,
            mqtt_config=mqtt_config,
            start_ucm=start_ucm,
        )

    @classmethod
    def from_blob(cls, log_level, blob, start_ucm=True):
        payload = json.loads(base64.b64decode(blob))

        mqtt_config = mqtt.Config(
            host=payload["mqtt_host"],
            port=int(payload["mqtt_port"]),
            tls_ca_cert=payload["mqtt_ca"],
            tls_cert=payload["mqtt_cert"],
            tls_secret_key=payload["mqtt_private_key"],
        )

        return cls(
            log_level=log_level,
            hardware_id=payload["ucm_id"],
            channel_id=payload["channel_id"],
            mqtt_config=mqtt_config,
            start_ucm=start_ucm,
        )

    def __init__(self, log_level, hardware_id, channel_id, mqtt_config, start_ucm=True):
        self.log_level = log_level
        self.hardware_id = hardware_id
        self.channel_id = channel_id
        self.mqtt = mqtt_config
        self.start_ucm = start_ucm
