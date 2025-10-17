import dataclasses
from typing import Any, Dict, List, Optional

from .message import Message


@dataclasses.dataclass
class Telemetry(Message):

    timestamp: int
    alerts: Optional[List[str]] = None
    values: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        if "timestamp" in self.values:
            raise ValueError("`timestamp` is reserved")
        if "alerts" in self.values:
            raise ValueError("`alerts` is reserved")

    @classmethod
    def from_dto(cls, dto: Dict[str, Any]) -> "Telemetry":
        dto = dto.copy()
        timestamp = dto.pop("timestamp")
        alerts = dto.pop("alerts", None)
        return cls(timestamp=timestamp, alerts=alerts, values=dto)

    def to_dto(self) -> Dict[str, Any]:
        return {"timestamp": self.timestamp, "alerts": self.alerts, **self.values}
