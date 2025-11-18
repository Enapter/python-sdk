import enapter


def test_from_dto() -> None:
    assert enapter.mqtt.api.device.Log.from_dto(
        {
            "timestamp": 1625079600,
            "message": "System started",
            "severity": "info",
            "persist": True,
        }
    ) == enapter.mqtt.api.device.Log(
        timestamp=1625079600,
        message="System started",
        severity=enapter.mqtt.api.device.LogSeverity.INFO,
        persist=True,
    )


def test_to_dto() -> None:
    assert enapter.mqtt.api.device.Log(
        timestamp=1625079600,
        message="System started",
        severity=enapter.mqtt.api.device.LogSeverity.WARNING,
        persist=False,
    ).to_dto() == {
        "timestamp": 1625079600,
        "message": "System started",
        "severity": "warning",
        "persist": False,
    }
