from typing import Self

import httpx

from enapter.http.api import blueprints, commands, devices, sites, telemetry

from .auth import Auth
from .config import Config


class Client:

    def __init__(self, config: Config) -> None:
        self._config = config
        self._auth = Auth(token=self._config.token)
        self._headers = {}
        if self._config.allow_http:
            self._headers["X-Enapter-Allow-HTTP"] = "true"
        self._transport = httpx.AsyncHTTPTransport()

    def _new_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            auth=self._auth,
            headers=self._headers,
            base_url=self._config.base_url,
            transport=self._transport,
        )

    async def __aenter__(self) -> Self:
        await self._transport.__aenter__()
        return self

    async def __aexit__(self, *exc) -> None:
        await self._transport.__aexit__(*exc)

    @property
    def devices(self) -> devices.Client:
        return devices.Client(client=self._new_client())

    @property
    def sites(self) -> sites.Client:
        return sites.Client(client=self._new_client())

    @property
    def commands(self) -> commands.Client:
        return commands.Client(client=self._new_client())

    @property
    def blueprints(self) -> blueprints.Client:
        return blueprints.Client(client=self._new_client())

    @property
    def telemetry(self) -> telemetry.Client:
        return telemetry.Client(client=self._new_client())
