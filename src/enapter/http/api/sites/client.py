from typing import AsyncContextManager, AsyncGenerator, List

import httpx

from enapter.http import api

from .location import Location
from .site import Site


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create(
        self, name: str, timezone: str, location: Location | None = None
    ) -> Site:
        url = "v3/sites"
        response = await self._client.post(
            url,
            json={
                "name": name,
                "timezone": timezone,
                "location": location.to_dto() if location is not None else None,
            },
        )
        await api.check_error(response)
        return Site.from_dto(response.json()["site"])

    async def get(self, site_id: str | None) -> Site:
        url = f"v3/sites/{site_id}" if site_id is not None else "v3/site"
        response = await self._client.get(url)
        await api.check_error(response)
        return Site.from_dto(response.json()["site"])

    def list(
        self, offset: int = 0, limit: int | None = None
    ) -> AsyncContextManager[AsyncGenerator[Site, None]]:
        async def fetch(current_offset: int) -> List[Site]:
            return await self._list(offset=current_offset)

        return api.paginate(fetch, offset=offset, limit=limit)

    async def _list(self, offset: int) -> List[Site]:
        url = "v3/sites"
        response = await self._client.get(url, params={"offset": offset})
        await api.check_error(response)
        payload = response.json()
        return [Site.from_dto(dto) for dto in payload.get("sites", [])]

    async def update(
        self,
        site_id: str | None,
        name: str | None = None,
        timezone: str | None = None,
        location: Location | None = None,
    ) -> Site:
        if name is None and timezone is None and location is None:
            return await self.get(site_id)
        url = f"v3/sites/{site_id}" if site_id is not None else "v3/site"
        response = await self._client.patch(
            url,
            json={
                "name": name,
                "timezone": timezone,
                "location": location.to_dto() if location is not None else None,
            },
        )
        await api.check_error(response)
        return Site.from_dto(response.json()["site"])

    async def delete(self, site_id: str) -> None:
        url = f"v3/sites/{site_id}"
        response = await self._client.delete(url)
        await api.check_error(response)
