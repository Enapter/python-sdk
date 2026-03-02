import httpx

from enapter.http import api

from .engine import Engine


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get(self, site_id: str | None = None) -> Engine:
        url = self._url(site_id)
        response = await self._client.get(url)
        await api.check_error(response)
        return Engine.from_dto(response.json()["engine"])

    async def suspend(self, site_id: str | None = None) -> Engine:
        url = f"{self._url(site_id)}/suspend"
        response = await self._client.post(url)
        await api.check_error(response)
        return Engine.from_dto(response.json()["engine"])

    async def resume(self, site_id: str | None = None) -> Engine:
        url = f"{self._url(site_id)}/resume"
        response = await self._client.post(url)
        await api.check_error(response)
        return Engine.from_dto(response.json()["engine"])

    def _url(self, site_id: str | None) -> str:
        if site_id is not None:
            return f"v3/sites/{site_id}/rule_engine"
        return "v3/site/rule_engine"
