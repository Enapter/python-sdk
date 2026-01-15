import collections
import dataclasses
from typing import AsyncIterator, Self

from .long_timeseries_row import LongTimeseriesRow
from .raw_timeseries_stream import RawTimeseriesStream


@dataclasses.dataclass
class LongTimeseriesStream:

    index: dict[str, dict[str, int]]
    raw_stream: RawTimeseriesStream

    @classmethod
    def from_raw_stream(cls, stream: RawTimeseriesStream) -> Self:
        index: dict[str, dict[str, int]] = collections.defaultdict(dict)
        for i in range(len(stream.data_types)):
            labels = stream.labels[i]
            index[labels.device][labels.telemetry] = i
        return cls(index, stream)

    async def __aiter__(self) -> AsyncIterator[LongTimeseriesRow]:
        async for row in self.raw_stream:
            for device_id, attributes in self.index.items():
                values = {}
                for attribute, i in attributes.items():
                    value = row.values[i]
                    if value is not None:
                        values[attribute] = value
                if values:
                    yield LongTimeseriesRow(
                        timestamp=row.timestamp, device_id=device_id, values=values
                    )
