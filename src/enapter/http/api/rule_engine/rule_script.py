"""Rule script data model."""

import base64
import dataclasses
from typing import Any, Self

from .runtime_version import RuntimeVersion


@dataclasses.dataclass
class RuleScript:
    """Rule script information."""

    code: str
    runtime_version: RuntimeVersion

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        """Create a RuleScript from a Data Transfer Object."""
        code = base64.b64decode(dto["code"]).decode("utf-8")
        return cls(
            code=code,
            runtime_version=RuntimeVersion(dto["runtime_version"]),
        )

    def to_dto(self) -> dict[str, Any]:
        """Convert the RuleScript to a Data Transfer Object."""
        code = base64.b64encode(self.code.encode("utf-8")).decode("utf-8")
        return {
            "code": code,
            "runtime_version": self.runtime_version.value,
        }
