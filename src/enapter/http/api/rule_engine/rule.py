"""Rule data model."""

import dataclasses
from typing import Any, Self

from .rule_script import RuleScript
from .rule_state import RuleState


@dataclasses.dataclass
class Rule:
    """Rule information."""

    id: str
    slug: str
    disabled: bool
    state: RuleState
    script: RuleScript

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        """Create a Rule from a Data Transfer Object."""
        return cls(
            id=dto["id"],
            slug=dto["slug"],
            disabled=dto["disabled"],
            state=RuleState(dto["state"]),
            script=RuleScript.from_dto(dto["script"]),
        )

    def to_dto(self) -> dict[str, Any]:
        """Convert the Rule to a Data Transfer Object."""
        return {
            "id": self.id,
            "slug": self.slug,
            "disabled": self.disabled,
            "state": self.state.value,
            "script": self.script.to_dto(),
        }
