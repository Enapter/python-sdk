from enapter.http.api.rule_engine.engine import Engine


def test_engine_from_dto():
    dto = {"state": "active"}
    engine = Engine.from_dto(dto)
    assert engine.state == "active"


def test_engine_to_dto():
    engine = Engine(state="suspended")
    dto = engine.to_dto()
    assert dto == {"state": "suspended"}
