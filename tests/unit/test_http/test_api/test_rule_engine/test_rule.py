"""Unit tests for the Rule and RuleScript data models."""

import enapter


def test_rule_script_from_dto():
    """Test creating a RuleScript from a DTO."""
    dto = {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"}
    script = enapter.http.api.rule_engine.RuleScript.from_dto(dto)
    assert script.code == "print('hello')"
    assert script.runtime_version == enapter.http.api.rule_engine.RuntimeVersion.V3


def test_rule_script_to_dto():
    """Test converting a RuleScript to a DTO."""
    script = enapter.http.api.rule_engine.RuleScript(
        code="print('hello')",
        runtime_version=enapter.http.api.rule_engine.RuntimeVersion.V3,
    )
    dto = script.to_dto()
    assert dto == {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"}


def test_rule_script_with_exec_interval():
    """Test RuleScript with exec_interval."""
    dto = {
        "code": "cHJpbnQoJ3YxJyk=",
        "runtime_version": "V1",
        "exec_interval": "1m",
    }
    script = enapter.http.api.rule_engine.RuleScript.from_dto(dto)
    assert script.code == "print('v1')"
    assert script.runtime_version == enapter.http.api.rule_engine.RuntimeVersion.V1
    assert script.exec_interval == "1m"

    dto_back = script.to_dto()
    assert dto_back == dto


def test_rule_from_dto():
    """Test creating a Rule from a DTO."""
    dto = {
        "id": "rule_123",
        "slug": "test-rule",
        "disabled": False,
        "state": "STARTED",
        "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
    }
    rule = enapter.http.api.rule_engine.Rule.from_dto(dto)
    assert rule.id == "rule_123"
    assert rule.slug == "test-rule"
    assert rule.disabled is False
    assert rule.state == enapter.http.api.rule_engine.RuleState.STARTED
    assert rule.script.code == "print('hello')"
    assert rule.script.runtime_version == enapter.http.api.rule_engine.RuntimeVersion.V3


def test_rule_to_dto():
    """Test converting a Rule to a DTO."""
    script = enapter.http.api.rule_engine.RuleScript(
        code="print('hello')",
        runtime_version=enapter.http.api.rule_engine.RuntimeVersion.V3,
    )
    rule = enapter.http.api.rule_engine.Rule(
        id="rule_123",
        slug="test-rule",
        disabled=True,
        state=enapter.http.api.rule_engine.RuleState.STOPPED,
        script=script,
    )
    dto = rule.to_dto()
    assert dto == {
        "id": "rule_123",
        "slug": "test-rule",
        "disabled": True,
        "state": "STOPPED",
        "script": {"code": "cHJpbnQoJ2hlbGxvJyk=", "runtime_version": "V3"},
    }
