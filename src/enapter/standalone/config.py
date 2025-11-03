import base64
import dataclasses
import enum
import json
import os
from typing import Any, MutableMapping, Self

from enapter import mqtt


@dataclasses.dataclass
class Config:

    communication_config: "CommunicationConfig"

    @property
    def communication(self) -> "CommunicationConfig":
        return self.communication_config

    @classmethod
    def from_env(
        cls, env: MutableMapping[str, str] = os.environ, namespace: str = "ENAPTER_"
    ) -> Self:
        communication_config = CommunicationConfig.from_env(env, namespace=namespace)
        return cls(communication_config=communication_config)


@dataclasses.dataclass
class CommunicationConfig:

    mqtt_config: mqtt.Config
    hardware_id: str
    channel_id: str
    ucm_needed: bool

    @property
    def mqtt(self) -> mqtt.Config:
        return self.mqtt_config

    @classmethod
    def from_env(
        cls, env: MutableMapping[str, str] = os.environ, namespace: str = "ENAPTER_"
    ) -> Self:
        prefix = namespace + "STANDALONE_COMMUNICATION_"
        blob = env[prefix + "CONFIG"]
        config = cls.from_blob(blob)
        override_mqtt_host = env.get(prefix + "OVERRIDE_MQTT_HOST")
        if override_mqtt_host is not None:
            config.mqtt.host = override_mqtt_host
        return config

    @classmethod
    def from_blob(cls, blob: str) -> Self:
        dto = json.loads(base64.b64decode(blob))
        if "ucm_id" in dto:
            config_v1 = CommunicationConfigV1.from_dto(dto)
            return cls.from_config_v1(config_v1)
        else:
            config_v3 = CommunicationConfigV3.from_dto(dto)
            return cls.from_config_v3(config_v3)

    @classmethod
    def from_config_v1(cls, config: "CommunicationConfigV1") -> Self:
        mqtt_config = mqtt.Config(
            host=config.mqtt_host,
            port=config.mqtt_port,
            tls_config=mqtt.TLSConfig(
                secret_key=config.mqtt_private_key,
                cert=config.mqtt_cert,
                ca_cert=config.mqtt_ca,
            ),
        )
        return cls(
            mqtt_config=mqtt_config,
            hardware_id=config.ucm_id,
            channel_id=config.channel_id,
            ucm_needed=True,
        )

    @classmethod
    def from_config_v3(cls, config: "CommunicationConfigV3") -> Self:
        mqtt_config: mqtt.Config | None = None
        match config.mqtt_protocol:
            case CommunicationConfigV3.MQTTProtocol.MQTT:
                assert isinstance(
                    config.mqtt_credentials, CommunicationConfigV3.MQTTCredentials
                )
                mqtt_config = mqtt.Config(
                    host=config.mqtt_host,
                    port=config.mqtt_port,
                    user=config.mqtt_credentials.username,
                    password=config.mqtt_credentials.password,
                )
            case CommunicationConfigV3.MQTTProtocol.MQTTS:
                assert isinstance(
                    config.mqtt_credentials, CommunicationConfigV3.MQTTSCredentials
                )
                mqtt_config = mqtt.Config(
                    host=config.mqtt_host,
                    port=config.mqtt_port,
                    tls_config=mqtt.TLSConfig(
                        secret_key=config.mqtt_credentials.private_key,
                        cert=config.mqtt_credentials.certificate,
                        ca_cert=config.mqtt_credentials.ca_chain,
                    ),
                )
            case _:
                raise NotImplementedError(config.mqtt_protocol)
        assert mqtt_config is not None
        return cls(
            mqtt_config=mqtt_config,
            hardware_id=config.hardware_id,
            channel_id=config.channel_id,
            ucm_needed=False,
        )


@dataclasses.dataclass
class CommunicationConfigV1:

    mqtt_host: str
    mqtt_port: int
    mqtt_ca: str
    mqtt_cert: str
    mqtt_private_key: str
    ucm_id: str
    channel_id: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            mqtt_host=dto["mqtt_host"],
            mqtt_port=int(dto["mqtt_port"]),
            mqtt_ca=dto["mqtt_ca"],
            mqtt_cert=dto["mqtt_cert"],
            mqtt_private_key=dto["mqtt_private_key"],
            ucm_id=dto["ucm_id"],
            channel_id=dto["channel_id"],
        )


@dataclasses.dataclass
class CommunicationConfigV3:

    class MQTTProtocol(enum.Enum):

        MQTT = "MQTT"
        MQTTS = "MQTTS"

    @dataclasses.dataclass
    class MQTTCredentials:

        username: str
        password: str

        @classmethod
        def from_dto(cls, dto: dict[str, Any]) -> Self:
            return cls(username=dto["username"], password=dto["password"])

    @dataclasses.dataclass
    class MQTTSCredentials:

        private_key: str
        certificate: str
        ca_chain: str

        @classmethod
        def from_dto(cls, dto: dict[str, Any]) -> Self:
            return cls(
                private_key=dto["private_key"],
                certificate=dto["certificate"],
                ca_chain=dto["ca_chain"],
            )

    mqtt_host: str
    mqtt_port: int
    mqtt_protocol: MQTTProtocol
    mqtt_credentials: MQTTCredentials | MQTTSCredentials
    hardware_id: str
    channel_id: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        mqtt_protocol = cls.MQTTProtocol(dto["mqtt_protocol"])
        mqtt_credentials: (
            CommunicationConfigV3.MQTTCredentials
            | CommunicationConfigV3.MQTTSCredentials
            | None
        ) = None
        match mqtt_protocol:
            case cls.MQTTProtocol.MQTT:
                mqtt_credentials = cls.MQTTCredentials.from_dto(dto["mqtt_credentials"])
            case cls.MQTTProtocol.MQTTS:
                mqtt_credentials = cls.MQTTSCredentials.from_dto(
                    dto["mqtt_credentials"]
                )
            case _:
                raise NotImplementedError(mqtt_protocol)
        assert mqtt_credentials is not None
        return cls(
            mqtt_host=dto["mqtt_host"],
            mqtt_port=int(dto["mqtt_port"]),
            mqtt_credentials=mqtt_credentials,
            mqtt_protocol=mqtt_protocol,
            hardware_id=dto["hardware_id"],
            channel_id=dto["channel_id"],
        )
