import dataclasses
import os
from typing import MutableMapping, Self


@dataclasses.dataclass
class Config:

    base_url: str
    allow_http: bool = dataclasses.field(init=False)
    token: str | None = None
    user: str | None = None

    def __post_init__(self) -> None:
        self.allow_http = self.base_url.startswith("http://")

    @classmethod
    def from_env(
        cls, env: MutableMapping[str, str] = os.environ, namespace: str = "ENAPTER_"
    ) -> Self:
        prefix = namespace + "HTTP_API_"
        base_url = env.get(prefix + "BASE_URL", "https://api.enapter.com")
        return cls(
            base_url=base_url,
            token=env.get(prefix + "TOKEN"),
            user=env.get(prefix + "USER"),
        )
