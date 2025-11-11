import dataclasses
from typing import Any, Self

from .mqtt_credentials import MQTTCredentials
from .mqtt_protocol import MQTTProtocol
from .mqtts_credentials import MQTTSCredentials
from .time_sync_protocol import TimeSyncProtocol


@dataclasses.dataclass
class CommunicationConfig:

    mqtt_host: str
    mqtt_port: int
    mqtt_credentials: MQTTCredentials | MQTTSCredentials
    mqtt_protocol: MQTTProtocol
    time_sync_protocol: TimeSyncProtocol
    time_sync_host: str
    time_sync_port: int
    hardware_id: str
    channel_id: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        mqtt_protocol = MQTTProtocol(dto["mqtt_protocol"])
        mqtt_credentials: MQTTCredentials | MQTTSCredentials | None = None
        match mqtt_protocol:
            case MQTTProtocol.MQTT:
                mqtt_credentials = MQTTCredentials.from_dto(dto["mqtt_credentials"])
            case MQTTProtocol.MQTTS:
                mqtt_credentials = MQTTSCredentials.from_dto(dto["mqtt_credentials"])
            case _:
                raise NotImplementedError(mqtt_protocol)
        assert mqtt_credentials is not None
        return cls(
            mqtt_host=dto["mqtt_host"],
            mqtt_port=int(dto["mqtt_port"]),
            mqtt_credentials=mqtt_credentials,
            mqtt_protocol=mqtt_protocol,
            time_sync_protocol=TimeSyncProtocol(dto["time_sync_protocol"].upper()),
            time_sync_host=dto["time_sync_host"],
            time_sync_port=int(dto["time_sync_port"]),
            hardware_id=dto["hardware_id"],
            channel_id=dto["channel_id"],
        )
