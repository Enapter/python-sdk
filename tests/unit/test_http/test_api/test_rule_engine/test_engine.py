from enapter.http.api.rule_engine.engine import Engine


def test_engine_from_dto():
    dto = {"id": "re_123", "state": "ACTIVE", "timezone": "UTC"}
    engine = Engine.from_dto(dto)
    assert engine.id == "re_123"
    assert engine.state == "ACTIVE"
    assert engine.timezone == "UTC"


def test_engine_to_dto():
    engine = Engine(id="re_123", state="SUSPENDED", timezone="UTC")
    dto = engine.to_dto()
    assert dto == {"id": "re_123", "state": "SUSPENDED", "timezone": "UTC"}
