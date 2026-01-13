from typing import Self

import fastmcp


class Client:

    def __init__(self, url: str) -> None:
        self._client = self._new_client(url)

    def _new_client(self, url: str) -> fastmcp.Client:
        return fastmcp.Client(transport=fastmcp.client.StreamableHttpTransport(url))

    async def __aenter__(self) -> Self:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc) -> None:
        await self._client.__aexit__(*exc)

    async def ping(self) -> bool:
        return await self._client.ping()
