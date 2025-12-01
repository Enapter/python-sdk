import dataclasses
import enum
from typing import Any


class DeviceCommunicationType(str, enum.Enum):

    MQTT_V1_PLAINTEXT = "MQTT_V1_PLAINTEXT"
    MQTT_V1_TLS = "MQTT_V1_TLS"
    MQTT_V1_LOCALHOST = "MQTT_V1_LOCALHOST"
    UCM_LUA = "UCM_LUA"
    UCM_EMBEDDED = "UCM_EMBEDDED"
    LINK = "LINK"


@dataclasses.dataclass
class DeviceCommunication:

    type: DeviceCommunicationType
    upstream_id: str | None
    hardware_id: str | None
    channel_id: str | None

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> "DeviceCommunication":
        return cls(
            type=DeviceCommunicationType(dto["type"]),
            upstream_id=dto.get("upstream_id"),
            hardware_id=dto.get("hardware_id"),
            channel_id=dto.get("channel_id"),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "type": self.type.value,
            "upstream_id": self.upstream_id,
            "hardware_id": self.hardware_id,
            "channel_id": self.channel_id,
        }
