import dataclasses
from typing import Any, Self


@dataclasses.dataclass
class Request:

    name: str
    arguments: dict[str, Any]
    manifest_name: str | None = None

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            name=dto["name"],
            arguments=dto["arguments"],
            manifest_name=dto.get("manifest_name"),
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "arguments": self.arguments,
            "manifest_name": self.manifest_name,
        }
