import dataclasses
import datetime
from typing import Any

from .gap_filling_method import GapFillingMethod


@dataclasses.dataclass
class GapFilling:

    method: GapFillingMethod
    look_around: datetime.timedelta

    def to_dto(self) -> dict[str, Any]:
        return {
            "method": self.method.value.lower(),
            "look_around": str(int(self.look_around.total_seconds())) + "s",
        }
