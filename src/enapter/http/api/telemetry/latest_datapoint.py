import dataclasses
import datetime
from typing import Any, Self


@dataclasses.dataclass
class LatestDatapoint:

    timestamp: datetime.datetime
    value: Any

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            timestamp=datetime.datetime.fromtimestamp(dto["timestamp"]),
            value=dto.get("value"),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "timestamp": int(self.timestamp.timestamp()),
            "value": self.value,
        }
