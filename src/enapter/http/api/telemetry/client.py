import contextlib
import datetime
from typing import AsyncGenerator

import httpx

from enapter.http import api

from .data_type import DataType
from .latest_datapoint import LatestDatapoint
from .long_timeseries_stream import LongTimeseriesStream
from .raw_timeseries_stream import RawTimeseriesStream
from .selector import Selector
from .wide_timeseries import WideTimeseries


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def latest(
        self,
        attributes_by_device: dict[str, list[str]],
        relevance_interval: int | datetime.timedelta | None = None,
    ) -> dict[str, dict[str, LatestDatapoint | None]]:
        url = "v3/telemetry/latest"
        params = {
            f"devices[{device}]": ",".join(attributes)
            for device, attributes in attributes_by_device.items()
        }
        if relevance_interval is not None:
            if isinstance(relevance_interval, datetime.timedelta):
                relevance_interval = int(relevance_interval.total_seconds())
            params["relevance_interval"] = str(relevance_interval) + "s"
        response = await self._client.get(url, params=params)
        api.check_error(response)
        return {
            device: {
                attribute: (
                    LatestDatapoint.from_dto(datapoint)
                    if datapoint.get("timestamp") is not None
                    else None
                )
                for attribute, datapoint in datapoints.items()
            }
            for device, datapoints in response.json().get("telemetry", {}).items()
        }

    @contextlib.asynccontextmanager
    async def long_timeseries(
        self,
        from_: datetime.datetime,
        to: datetime.datetime,
        granularity: int | datetime.timedelta,
        selectors: list[Selector],
    ) -> AsyncGenerator[LongTimeseriesStream, None]:
        async with self.raw_timeseries(
            from_=from_, to=to, granularity=granularity, selectors=selectors
        ) as stream:
            yield LongTimeseriesStream.from_raw_stream(stream)

    async def wide_timeseries(
        self,
        from_: datetime.datetime,
        to: datetime.datetime,
        granularity: int | datetime.timedelta,
        selectors: list[Selector],
    ) -> WideTimeseries:
        async with self.raw_timeseries(
            from_=from_, to=to, granularity=granularity, selectors=selectors
        ) as stream:
            return await WideTimeseries.from_raw_stream(stream)

    @contextlib.asynccontextmanager
    async def raw_timeseries(
        self,
        from_: datetime.datetime,
        to: datetime.datetime,
        granularity: int | datetime.timedelta,
        selectors: list[Selector],
    ) -> AsyncGenerator[RawTimeseriesStream, None]:
        if to <= from_:
            raise ValueError("`to` must be greater than `from_`")
        if isinstance(granularity, datetime.timedelta):
            granularity = int(granularity.total_seconds())
        payload = {
            "from": from_.isoformat(),
            "to": to.isoformat(),
            "granularity": str(granularity) + "s",
            "telemetry": [selector.to_dto() for selector in selectors],
        }
        async with self._client.stream(
            "POST",
            "v3/telemetry/query_timeseries",
            headers={"Accept": "text/csv"},
            json=payload,
        ) as response:
            api.check_error(response)
            data_types = [
                DataType(dt.strip().upper())
                for dt in response.headers["X-Enapter-Timeseries-Data-Types"].split(",")
            ]
            lines = response.aiter_lines()
            yield await RawTimeseriesStream.new(data_types, lines)
