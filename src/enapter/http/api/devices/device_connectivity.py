import dataclasses
import enum


class DeviceConnectivityStatus(enum.Enum):

    UNKNOWN = "UNKNOWN"
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


@dataclasses.dataclass
class DeviceConnectivity:

    status: DeviceConnectivityStatus

    @classmethod
    def from_dto(cls, dto: dict[str, str]) -> "DeviceConnectivity":
        return cls(status=DeviceConnectivityStatus(dto.get("status", "UNKNOWN")))

    def to_dto(self) -> dict[str, str]:
        return {"status": self.status.value}
