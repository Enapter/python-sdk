import pytest

import enapter


def test_from_dto() -> None:
    assert enapter.mqtt.api.device.Properties.from_dto(
        {
            "timestamp": 1625079600,
            "property1": "value1",
            "property2": 42,
            "property3": True,
        }
    ) == enapter.mqtt.api.device.Properties(
        timestamp=1625079600,
        values={
            "property1": "value1",
            "property2": 42,
            "property3": True,
        },
    )


def test_to_dto() -> None:
    assert enapter.mqtt.api.device.Properties(
        timestamp=1625079600,
        values={
            "property1": "value1",
            "property2": 42,
            "property3": True,
        },
    ).to_dto() == {
        "timestamp": 1625079600,
        "property1": "value1",
        "property2": 42,
        "property3": True,
    }


def test_reserved_timestamp_in_values() -> None:
    with pytest.raises(ValueError):
        enapter.mqtt.api.device.Properties(
            timestamp=1625079600,
            values={"timestamp": 1234567890},
        )
