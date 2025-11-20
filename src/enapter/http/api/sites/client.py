from typing import AsyncGenerator

import httpx

from enapter import async_
from enapter.http import api

from .site import Site


class Client:

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def create(self, name: str) -> Site:
        url = "v3/sites"
        response = await self._client.post(url, json={"name": name})
        api.check_error(response)
        return Site.from_dto(response.json()["site"])

    async def get(self, site_id: str) -> Site:
        url = f"v3/sites/{site_id}"
        response = await self._client.get(url)
        api.check_error(response)
        return Site.from_dto(response.json()["site"])

    @async_.generator
    async def list(self) -> AsyncGenerator[Site, None]:
        url = "v3/sites"
        limit = 50
        offset = 0
        while True:
            response = await self._client.get(
                url, params={"limit": limit, "offset": offset}
            )
            api.check_error(response)
            payload = response.json()
            if not payload["sites"]:
                return
            for dto in payload["sites"]:
                yield Site.from_dto(dto)
            offset += limit

    async def update(self, site_id: str, name: str | None = None) -> Site:
        if name is None:
            return await self.get(site_id)
        url = f"v3/sites/{site_id}"
        response = await self._client.patch(url, json={"name": name})
        api.check_error(response)
        return Site.from_dto(response.json()["site"])

    async def delete(self, site_id: str) -> None:
        url = f"v3/sites/{site_id}"
        response = await self._client.delete(url)
        api.check_error(response)
