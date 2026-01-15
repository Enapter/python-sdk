import collections
from typing import Self


class Labels(collections.UserDict):

    @classmethod
    def parse(cls, s: str) -> Self:
        return cls(kv.split("=") for kv in s.split(" "))

    @property
    def device(self) -> str:
        return self.data["device"]

    @property
    def telemetry(self) -> str:
        return self.data["telemetry"]
