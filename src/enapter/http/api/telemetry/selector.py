import dataclasses
import datetime
from typing import Any

from .aggregation import Aggregation
from .gap_filling import GapFilling
from .gap_filling_method import GapFillingMethod


@dataclasses.dataclass
class Selector:

    device: str
    attributes: list[str]
    aggregation: Aggregation | None = None
    gap_filling: GapFilling | None = None

    def __post_init__(self) -> None:
        if self.aggregation is None:
            self.aggregation = Aggregation.AUTO
        if self.gap_filling is None:
            self.gap_filling = GapFilling(
                method=GapFillingMethod.NONE, look_around=datetime.timedelta()
            )

    def to_dto(self) -> dict[str, Any]:
        assert self.aggregation is not None
        assert self.gap_filling is not None
        return {
            "device": self.device,
            "attribute": self.attributes,
            "aggregation": self.aggregation.value.lower(),
            "gap_filling": self.gap_filling.to_dto(),
        }
