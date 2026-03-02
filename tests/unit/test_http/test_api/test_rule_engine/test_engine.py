"""Unit tests for the Rule Engine data model."""

import enapter


def test_engine_from_dto():
    """Test creating an Engine from a DTO."""
    dto = {"id": "re_123", "state": "ACTIVE", "timezone": "UTC"}
    engine = enapter.http.api.rule_engine.Engine.from_dto(dto)
    assert engine.id == "re_123"
    assert engine.state == enapter.http.api.rule_engine.EngineState.ACTIVE
    assert engine.timezone == "UTC"


def test_engine_to_dto():
    """Test converting an Engine to a DTO."""
    engine = enapter.http.api.rule_engine.Engine(
        id="re_123",
        state=enapter.http.api.rule_engine.EngineState.SUSPENDED,
        timezone="UTC",
    )
    dto = engine.to_dto()
    assert dto == {"id": "re_123", "state": "SUSPENDED", "timezone": "UTC"}
