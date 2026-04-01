import collections
from typing import Self


class Labels(collections.UserDict):

    @classmethod
    def parse(cls, s: str) -> Self:
        if not s:
            return cls()
        return cls(kv.split("=") for kv in s.split(" ") if kv)

    @property
    def device(self) -> str:
        return self.data["device"]

    @property
    def telemetry(self) -> str:
        return self.data["telemetry"]
