import pytest

from enapter.http.api.telemetry.data_type import DataType


def test_parse_value_empty() -> None:
    assert DataType.FLOAT.parse_value("") is None
    assert DataType.INTEGER.parse_value("") is None
    assert DataType.STRING.parse_value("") is None
    assert DataType.STRING_ARRAY.parse_value("") is None
    assert DataType.BOOLEAN.parse_value("") is None


def test_parse_value_float() -> None:
    assert DataType.FLOAT.parse_value("1.5") == 1.5
    assert DataType.FLOAT.parse_value("-3.14") == -3.14
    with pytest.raises(ValueError):
        DataType.FLOAT.parse_value("invalid")


def test_parse_value_integer() -> None:
    assert DataType.INTEGER.parse_value("42") == 42
    assert DataType.INTEGER.parse_value("-7") == -7
    with pytest.raises(ValueError):
        DataType.INTEGER.parse_value("invalid")


def test_parse_value_string() -> None:
    assert DataType.STRING.parse_value("hello") == "hello"


def test_parse_value_string_array() -> None:
    assert DataType.STRING_ARRAY.parse_value('["a", "b"]') == ["a", "b"]
    with pytest.raises(ValueError):
        DataType.STRING_ARRAY.parse_value("invalid")


def test_parse_value_boolean() -> None:
    assert DataType.BOOLEAN.parse_value("True") is True
    assert DataType.BOOLEAN.parse_value("true") is True
    assert DataType.BOOLEAN.parse_value("1") is True
    assert DataType.BOOLEAN.parse_value("False") is False
    assert DataType.BOOLEAN.parse_value("false") is False
    assert DataType.BOOLEAN.parse_value("0") is False
    with pytest.raises(ValueError, match="invalid boolean value"):
        DataType.BOOLEAN.parse_value("invalid")
