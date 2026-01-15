import csv
import datetime
from typing import AsyncGenerator, AsyncIterator, Self

from .data_type import DataType
from .labels import Labels
from .raw_timeseries_row import RawTimeseriesRow


class RawTimeseriesStream:

    @classmethod
    async def new(cls, data_types: list[DataType], lines: AsyncIterator[str]) -> Self:
        first_line = await lines.__anext__()
        header = cls._parse_csv_record(first_line)
        assert header[0] == "ts"
        labels = [Labels.parse(kvs) for kvs in header[1:]]
        return cls(data_types=data_types, labels=labels, lines=lines)

    def __init__(
        self,
        data_types: list[DataType],
        labels: list[Labels],
        lines: AsyncIterator[str],
    ) -> None:
        self._data_types = data_types
        self._labels = labels
        self._lines = lines

    @property
    def data_types(self) -> list[DataType]:
        return self._data_types

    @property
    def labels(self) -> list[Labels]:
        return self._labels

    async def __aiter__(self) -> AsyncGenerator[RawTimeseriesRow, None]:
        async for line in self._lines:
            record = self._parse_csv_record(line)
            timestamp = datetime.datetime.fromtimestamp(
                int(record[0]), tz=datetime.timezone.utc
            )
            values = []
            for i, value_string in enumerate(record[1:]):
                data_type = self._data_types[i]
                value = data_type.parse_value(value_string)
                values.append(value)
            yield RawTimeseriesRow(timestamp=timestamp, values=values)

    @staticmethod
    def _parse_csv_record(line: str) -> list[str]:
        reader = csv.reader([line], delimiter=",")
        records = list(reader)
        assert len(records) == 1
        return records[0]
