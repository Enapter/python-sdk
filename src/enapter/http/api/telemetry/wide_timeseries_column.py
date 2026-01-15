import dataclasses
from typing import Any

from .data_type import DataType
from .labels import Labels


@dataclasses.dataclass
class WideTimeseriesColumn:

    data_type: DataType
    labels: Labels
    values: list[Any]

    def __len__(self) -> int:
        return len(self.values)

    def to_dto(self) -> dict[str, Any]:
        return {
            "data_type": self.data_type.value.lower(),
            "labels": dict(self.labels),
            "values": self.values,
        }
