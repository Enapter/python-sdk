import enapter


def test_from_dto() -> None:
    assert enapter.mqtt.api.device.CommandResponse.from_dto(
        {
            "id": "bbe17a10-3107-47cb-b0ec-99648debade6",
            "state": "completed",
            "payload": {"foo": "bar"},
        }
    ) == enapter.mqtt.api.device.CommandResponse(
        id="bbe17a10-3107-47cb-b0ec-99648debade6",
        state=enapter.mqtt.api.device.CommandState.COMPLETED,
        payload={"foo": "bar"},
    )


def test_to_dto() -> None:
    assert enapter.mqtt.api.device.CommandResponse(
        id="bbe17a10-3107-47cb-b0ec-99648debade6",
        state=enapter.mqtt.api.device.CommandState.COMPLETED,
        payload={"foo": "bar"},
    ).to_dto() == {
        "id": "bbe17a10-3107-47cb-b0ec-99648debade6",
        "state": "completed",
        "payload": {"foo": "bar"},
    }
