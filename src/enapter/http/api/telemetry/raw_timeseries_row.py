import dataclasses
import datetime
from typing import Any


@dataclasses.dataclass
class RawTimeseriesRow:

    timestamp: datetime.datetime
    values: list[Any]
