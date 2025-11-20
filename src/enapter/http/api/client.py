from typing import Self

import httpx

from enapter.http.api import devices, sites

from .config import Config


class Client:

    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = self._new_client()

    def _new_client(self) -> httpx.AsyncClient:
        assert self._config.base_url is not None
        headers = {"X-Enapter-Auth-Token": self._config.token}
        if self._config.allow_http:
            headers["X-Enapter-Allow-HTTP"] = "true"
        return httpx.AsyncClient(
            headers=headers,
            base_url=self._config.base_url,
        )

    async def __aenter__(self) -> Self:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc) -> None:
        await self._client.__aexit__(*exc)

    @property
    def devices(self) -> devices.Client:
        return devices.Client(client=self._client)

    @property
    def sites(self) -> sites.Client:
        return sites.Client(client=self._client)
