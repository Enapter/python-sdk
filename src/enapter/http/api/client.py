from typing import Self

import httpx

from enapter.http.api import blueprints, commands, devices, sites, telemetry

from .auth import Auth
from .config import Config


class Client:

    def __init__(self, config: Config) -> None:
        self._config = config
        self._auth = Auth(token=self._config.token, user=self._config.user)
        self._headers = {}
        if self._config.allow_http:
            self._headers["X-Enapter-Allow-HTTP"] = "true"
        self._transport = httpx.AsyncHTTPTransport()

    def _new_client(self, auth: Auth | None) -> httpx.AsyncClient:
        auth = auth if auth is not None else self._auth
        return httpx.AsyncClient(
            auth=auth,
            headers=self._headers,
            base_url=self._config.base_url,
            transport=self._transport,
        )

    async def __aenter__(self) -> Self:
        await self._transport.__aenter__()
        return self

    async def __aexit__(self, *exc) -> None:
        await self._transport.__aexit__(*exc)

    def devices(self, auth: Auth | None = None) -> devices.Client:
        return devices.Client(client=self._new_client(auth=auth))

    def sites(self, auth: Auth | None = None) -> sites.Client:
        return sites.Client(client=self._new_client(auth=auth))

    def commands(self, auth: Auth | None = None) -> commands.Client:
        return commands.Client(client=self._new_client(auth=auth))

    def blueprints(self, auth: Auth | None = None) -> blueprints.Client:
        return blueprints.Client(client=self._new_client(auth=auth))

    def telemetry(self, auth: Auth | None = None) -> telemetry.Client:
        return telemetry.Client(client=self._new_client(auth=auth))
