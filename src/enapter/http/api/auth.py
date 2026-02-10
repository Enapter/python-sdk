from typing import Generator

import httpx


class Auth(httpx.Auth):

    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["X-Enapter-Auth-Token"] = self.token
        yield request
