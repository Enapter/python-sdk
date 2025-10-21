import base64
import json
import os
from typing import MutableMapping, Optional

import enapter


class Config:

    @classmethod
    def from_env(
        cls, prefix: Optional[str] = None, env: MutableMapping[str, str] = os.environ
    ) -> "Config":
        if prefix is None:
            prefix = "ENAPTER_VUCM_"
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

        mqtt = enapter.mqtt.Config.from_env(prefix=prefix, env=env)

        start_ucm = env.get(prefix + "START_UCM", "1") != "0"

        return cls(
            hardware_id=hardware_id,
            channel_id=channel_id,
            mqtt=mqtt,
            start_ucm=start_ucm,
        )

    @classmethod
    def from_blob(cls, blob: str) -> "Config":
        payload = json.loads(base64.b64decode(blob))

        mqtt = enapter.mqtt.Config(
            host=payload["mqtt_host"],
            port=int(payload["mqtt_port"]),
            tls=enapter.mqtt.TLSConfig(
                ca_cert=payload["mqtt_ca"],
                cert=payload["mqtt_cert"],
                secret_key=payload["mqtt_private_key"],
            ),
        )

        return cls(
            hardware_id=payload["ucm_id"],
            channel_id=payload["channel_id"],
            mqtt=mqtt,
        )

    def __init__(
        self,
        hardware_id: str,
        channel_id: str,
        mqtt: enapter.mqtt.Config,
        start_ucm: bool = True,
    ) -> None:
        self.hardware_id = hardware_id
        self.channel_id = channel_id
        self.mqtt = mqtt
        self.start_ucm = start_ucm
