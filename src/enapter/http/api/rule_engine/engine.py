import dataclasses
from typing import Any, Self


@dataclasses.dataclass
class Engine:

    state: str

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            state=dto["state"],
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "state": self.state,
        }
