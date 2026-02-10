from typing import Generator

import httpx


class Auth(httpx.Auth):

    def __init__(self, token: str | None = None, user: str | None = None) -> None:
        self.token = token
        self.user = user

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        if self.token is not None:
            request.headers["X-Enapter-Auth-Token"] = self.token
        if self.user is not None:
            request.headers["X-Enapter-Auth-User"] = self.user
        yield request
