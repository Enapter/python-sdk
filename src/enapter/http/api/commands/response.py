import dataclasses
import datetime
import enum
from typing import Any, Self


class ResponseState(enum.Enum):

    STARTED = "STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    ERROR = "ERROR"


@dataclasses.dataclass
class Response:

    state: ResponseState
    payload: dict[str, Any]
    received_at: datetime.datetime

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            state=ResponseState(dto["state"]),
            payload=dto.get("payload", {}),
            received_at=datetime.datetime.fromisoformat(dto["received_at"]),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "payload": self.payload,
            "received_at": self.received_at.isoformat(),
        }
