import base64
import json
import os
from typing import MutableMapping

from enapter import mqtt


class Config:

    @classmethod
    def from_env(
        cls, env: MutableMapping[str, str] = os.environ, namespace: str = "ENAPTER_"
    ) -> "Config":
        prefix = namespace + "STANDALONE_"

        try:
            blob = env[prefix + "BLOB"]
        except KeyError:
            pass
        else:
            config = cls.from_blob(blob)
            try:
                config.channel_id = env[prefix + "CHANNEL_ID"]
            except KeyError:
                pass
            return config

        hardware_id = env[prefix + "HARDWARE_ID"]
        channel_id = env[prefix + "CHANNEL_ID"]

        mqtt_config = mqtt.Config.from_env(env, namespace=namespace)

        start_ucm = env.get(prefix + "START_UCM", "1") != "0"

        return cls(
            hardware_id=hardware_id,
            channel_id=channel_id,
            mqtt=mqtt_config,
            start_ucm=start_ucm,
        )

    @classmethod
    def from_blob(cls, blob: str) -> "Config":
        payload = json.loads(base64.b64decode(blob))

        mqtt_config = mqtt.Config(
            host=payload["mqtt_host"],
            port=int(payload["mqtt_port"]),
            tls=mqtt.TLSConfig(
                ca_cert=payload["mqtt_ca"],
                cert=payload["mqtt_cert"],
                secret_key=payload["mqtt_private_key"],
            ),
        )

        return cls(
            hardware_id=payload["ucm_id"],
            channel_id=payload["channel_id"],
            mqtt=mqtt_config,
        )

    def __init__(
        self,
        hardware_id: str,
        channel_id: str,
        mqtt: mqtt.Config,
        start_ucm: bool = True,
    ) -> None:
        self.hardware_id = hardware_id
        self.channel_id = channel_id
        self.mqtt = mqtt
        self.start_ucm = start_ucm
