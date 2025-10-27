import os
from typing import MutableMapping, Optional


class Config:

    @classmethod
    def from_env(
        cls,
        env: MutableMapping[str, str] = os.environ,
        namespace: str = "ENAPTER_",
    ) -> "Config":
        prefix = namespace + "HTTP_API_"
        return cls(
            token=env[prefix + "TOKEN"],
            base_url=env.get(prefix + "BASE_URL"),
        )

    def __init__(self, token: str, base_url: Optional[str] = None) -> None:
        if not token:
            raise ValueError("token is missing")
        self.token = token
        if base_url is None:
            base_url = "https://api.enapter.com"
        self.base_url = base_url
