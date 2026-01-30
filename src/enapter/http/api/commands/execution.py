import dataclasses
import datetime
import enum
from typing import Any, Self

from .request import Request
from .response import Response


class ListExecutionsOrder(enum.Enum):

    CREATED_AT_ASC = "CREATED_AT_ASC"
    CREATED_AT_DESC = "CREATED_AT_DESC"


class ExecutionState(enum.Enum):

    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    UNSYNC = "UNSYNC"


@dataclasses.dataclass
class Execution:

    id: str
    state: ExecutionState
    created_at: datetime.datetime
    request: Request
    response: Response | None
    log: list[Response] | None

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            id=dto["id"],
            state=ExecutionState(dto["state"]),
            created_at=datetime.datetime.fromisoformat(dto["created_at"]),
            request=Request.from_dto(dto["request"]),
            response=(
                Response.from_dto(dto["response"])
                if dto.get("response") is not None
                else None
            ),
            log=(
                [Response.from_dto(item) for item in dto["log"]]
                if dto.get("log") is not None
                else None
            ),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "request": self.request.to_dto(),
            "response": self.response.to_dto() if self.response is not None else None,
            "log": (
                [item.to_dto() for item in self.log] if self.log is not None else None
            ),
        }
