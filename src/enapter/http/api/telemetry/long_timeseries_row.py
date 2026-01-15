import dataclasses
import datetime
from typing import Any


@dataclasses.dataclass
class LongTimeseriesRow:

    timestamp: datetime.datetime
    device_id: str
    values: dict[str, Any]

    def to_dto(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "device_id": self.device_id,
            "values": self.values,
        }
