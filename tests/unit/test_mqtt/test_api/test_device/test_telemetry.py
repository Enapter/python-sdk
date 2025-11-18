import pytest

import enapter


def test_from_dto() -> None:
    assert enapter.mqtt.api.device.Telemetry.from_dto(
        {
            "timestamp": 1625079600,
            "alerts": ["foo"],
            "attribute1": "value1",
            "attribute2": 42,
            "attribute3": True,
        }
    ) == enapter.mqtt.api.device.Telemetry(
        timestamp=1625079600,
        alerts=["foo"],
        values={
            "attribute1": "value1",
            "attribute2": 42,
            "attribute3": True,
        },
    )


def test_to_dto() -> None:
    assert enapter.mqtt.api.device.Telemetry(
        timestamp=1625079600,
        alerts=["bar"],
        values={
            "attribute1": "value1",
            "attribute2": 42,
            "attribute3": True,
        },
    ).to_dto() == {
        "timestamp": 1625079600,
        "alerts": ["bar"],
        "attribute1": "value1",
        "attribute2": 42,
        "attribute3": True,
    }


def test_to_dto_with_empty_alerts() -> None:
    assert enapter.mqtt.api.device.Telemetry(
        timestamp=1625079600,
        alerts=[],
        values={},
    ).to_dto() == {
        "timestamp": 1625079600,
        "alerts": [],
    }


def test_to_dto_with_none_alerts() -> None:
    assert enapter.mqtt.api.device.Telemetry(
        timestamp=1625079600,
        alerts=None,
        values={},
    ).to_dto() == {
        "timestamp": 1625079600,
        "alerts": None,
    }


def test_reserved_timestamp_in_values() -> None:
    with pytest.raises(ValueError):
        enapter.mqtt.api.device.Telemetry(
            timestamp=1625079600,
            alerts=[],
            values={"timestamp": 1234567890},
        )


def test_reserved_alerts_in_values() -> None:
    with pytest.raises(ValueError):
        enapter.mqtt.api.device.Telemetry(
            timestamp=1625079600,
            alerts=[],
            values={"alerts": ["alert1"]},
        )
