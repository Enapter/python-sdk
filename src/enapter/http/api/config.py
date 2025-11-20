import dataclasses
import os
from typing import MutableMapping, Self


@dataclasses.dataclass
class Config:

    token: str
    base_url: str
    allow_http: bool = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.allow_http = self.base_url.startswith("http://")

    @classmethod
    def from_env(
        cls, env: MutableMapping[str, str] = os.environ, namespace: str = "ENAPTER_"
    ) -> Self:
        prefix = namespace + "HTTP_API_"
        base_url = env.get(prefix + "BASE_URL", "https://api.enapter.com")
        return cls(token=env[prefix + "TOKEN"], base_url=base_url)
