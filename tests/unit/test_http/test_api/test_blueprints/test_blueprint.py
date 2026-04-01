import datetime

from enapter.http.api.blueprints.blueprint import Blueprint


def test_blueprint_from_dto():
    dto = {
        "id": "bp_123",
        "created_at": "2023-01-01T12:00:00+00:00",
    }
    blueprint = Blueprint.from_dto(dto)
    assert blueprint.id == "bp_123"
    assert blueprint.created_at == datetime.datetime(
        2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
    )


def test_blueprint_to_dto():
    created_at = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    blueprint = Blueprint(id="bp_123", created_at=created_at)
    dto = blueprint.to_dto()
    assert dto == {
        "id": "bp_123",
        "created_at": "2023-01-01T12:00:00+00:00",
    }


def test_blueprint_roundtrip():
    dto = {
        "id": "bp_123",
        "created_at": "2023-01-01T12:00:00+00:00",
    }
    blueprint = Blueprint.from_dto(dto)
    assert blueprint.to_dto() == dto
