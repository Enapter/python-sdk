import datetime

import httpx

from enapter.http import api

from .latest_datapoint import LatestDatapoint


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
