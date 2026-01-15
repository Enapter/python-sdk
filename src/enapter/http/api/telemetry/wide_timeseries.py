import dataclasses
import datetime
from typing import Any, Self

from .raw_timeseries_stream import RawTimeseriesStream
from .wide_timeseries_column import WideTimeseriesColumn


@dataclasses.dataclass
class WideTimeseries:

    timestamps: list[datetime.datetime]
    columns: list[WideTimeseriesColumn]

    @classmethod
    async def from_raw_stream(cls, stream: RawTimeseriesStream) -> Self:
        rows = [row async for row in stream]
        timestamps = [row.timestamp for row in rows]
        columns = []
        for i in range(len(stream.data_types)):
            column = WideTimeseriesColumn(
                data_type=stream.data_types[i],
                labels=stream.labels[i],
                values=[row.values[i] for row in rows],
            )
            columns.append(column)
        return cls(timestamps, columns)

    def to_dto(self) -> dict[str, Any]:
        return {
            "timestamps": [timestamp.isoformat() for timestamp in self.timestamps],
            "columns": [column.to_dto() for column in self.columns],
        }
