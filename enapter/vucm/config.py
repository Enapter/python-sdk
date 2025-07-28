import base64
import json
import os

import enapter


class Config:
    @classmethod
    def from_env(cls, prefix=None, env=os.environ):
        if prefix is None:
            prefix = "ENAPTER_VUCM_"
        try:
            blob = os.environ[prefix + "BLOB"]
        except KeyError:
            pass
        else:
            config = cls.from_blob(blob)
            try:
                config.channel_id = os.environ[prefix + "CHANNEL_ID"]
            except KeyError:
                pass
            return config

        hardware_id = os.environ[prefix + "HARDWARE_ID"]
        channel_id = os.environ[prefix + "CHANNEL_ID"]

        mqtt_config = enapter.mqtt.Config.from_env(prefix=prefix, env=env)

        start_ucm = os.environ.get(prefix + "START_UCM", "1") != "0"

        return cls(
            hardware_id=hardware_id,
            channel_id=channel_id,
            mqtt_config=mqtt_config,
            start_ucm=start_ucm,
        )

    @classmethod
    def from_blob(cls, blob):
        payload = json.loads(base64.b64decode(blob))

        mqtt_config = enapter.mqtt.Config(
            host=payload["mqtt_host"],
            port=int(payload["mqtt_port"]),
            tls_ca_cert=payload["mqtt_ca"],
            tls_cert=payload["mqtt_cert"],
            tls_secret_key=payload["mqtt_private_key"],
        )

        return cls(
            hardware_id=payload["ucm_id"],
            channel_id=payload["channel_id"],
            mqtt_config=mqtt_config,
        )

    def __init__(self, hardware_id, channel_id, mqtt_config, start_ucm=True):
        self.hardware_id = hardware_id
        self.channel_id = channel_id
        self.mqtt = mqtt_config
        self.start_ucm = start_ucm
