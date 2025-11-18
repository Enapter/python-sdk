import enapter


def test_from_dto() -> None:
    assert enapter.mqtt.api.device.CommandRequest.from_dto(
        {
            "id": "bbe17a10-3107-47cb-b0ec-99648debade6",
            "name": "do_stuff",
            "arguments": {"foo": "bar"},
        }
    ) == enapter.mqtt.api.device.CommandRequest(
        id="bbe17a10-3107-47cb-b0ec-99648debade6",
        name="do_stuff",
        arguments={"foo": "bar"},
    )


def test_from_dto_without_arguments() -> None:
    assert enapter.mqtt.api.device.CommandRequest.from_dto(
        {
            "id": "bbe17a10-3107-47cb-b0ec-99648debade6",
            "name": "do_stuff",
        }
    ) == enapter.mqtt.api.device.CommandRequest(
        id="bbe17a10-3107-47cb-b0ec-99648debade6",
        name="do_stuff",
        arguments={},
    )


def test_from_dto_with_null_arguments() -> None:
    assert enapter.mqtt.api.device.CommandRequest.from_dto(
        {
            "id": "bbe17a10-3107-47cb-b0ec-99648debade6",
            "name": "do_stuff",
            "arguments": None,
        }
    ) == enapter.mqtt.api.device.CommandRequest(
        id="bbe17a10-3107-47cb-b0ec-99648debade6",
        name="do_stuff",
        arguments={},
    )


def test_to_dto() -> None:
    assert enapter.mqtt.api.device.CommandRequest(
        id="bbe17a10-3107-47cb-b0ec-99648debade6",
        name="do_stuff",
        arguments={"foo": "bar"},
    ).to_dto() == {
        "id": "bbe17a10-3107-47cb-b0ec-99648debade6",
        "name": "do_stuff",
        "arguments": {"foo": "bar"},
    }


def test_new_response() -> None:
    assert enapter.mqtt.api.device.CommandRequest(
        id="bbe17a10-3107-47cb-b0ec-99648debade6",
        name="do_stuff",
        arguments={"foo": "bar"},
    ).new_response(
        state=enapter.mqtt.api.device.CommandState.COMPLETED, payload={"goo": "jar"}
    ) == enapter.mqtt.api.device.CommandResponse(
        id="bbe17a10-3107-47cb-b0ec-99648debade6",
        state=enapter.mqtt.api.device.CommandState.COMPLETED,
        payload={"goo": "jar"},
    )
