import dataclasses
import enum
from typing import Any, Dict

from .message import Message


class LogSeverity(enum.Enum):

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclasses.dataclass
class Log(Message):

    timestamp: int
    message: str
    severity: LogSeverity
    persist: bool

    @classmethod
    def from_dto(cls, dto: Dict[str, Any]) -> "Log":
        return cls(
            timestamp=dto["timestamp"],
            message=dto["message"],
            severity=LogSeverity(dto["severity"]),
            persist=dto["persist"],
        )

    def to_dto(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "message": self.message,
            "severity": self.severity.value,
            "persist": self.persist,
        }
