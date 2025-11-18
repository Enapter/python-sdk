import dataclasses
from typing import Any, Self

import enapter


@dataclasses.dataclass
class MyMessage(enapter.mqtt.api.device.Message):

    field1: str
    field2: int

    @classmethod
    def from_dto(cls, dto: dict[str, Any]) -> Self:
        return cls(
            field1=dto["field1"],
            field2=dto["field2"],
        )

    def to_dto(self) -> dict[str, Any]:
        return {
            "field1": self.field1,
            "field2": self.field2,
        }


def test_from_json() -> None:
    json_data = '{"field1": "value1", "field2": 42}'
    message = MyMessage.from_json(json_data)
    assert message.field1 == "value1"
    assert message.field2 == 42


def test_to_json() -> None:
    message = MyMessage(field1="value1", field2=42)
    json_data = message.to_json()
    expected_json = '{"field1": "value1", "field2": 42}'
    assert json_data == expected_json
