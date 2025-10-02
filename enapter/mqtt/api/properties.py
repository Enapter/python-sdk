import dataclasses
from typing import Any, Dict

from .message import Message


@dataclasses.dataclass
class Properties(Message):

    timestamp: int
    values: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        if "timestamp" in self.values:
            raise ValueError("`timestamp` is reserved")

    @classmethod
    def from_dto(cls, dto: Dict[str, Any]) -> "Properties":
        timestamp = dto["timestamp"]
        values = {k: v for k, v in dto.items() if k != "timestamp"}
        return cls(timestamp=timestamp, values=values)

    def to_dto(self) -> Dict[str, Any]:
        return {"timestamp": self.timestamp, **self.values}
