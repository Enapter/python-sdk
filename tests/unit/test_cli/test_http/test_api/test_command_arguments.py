import argparse

import pytest

from enapter.cli.http.api.command_arguments import parse_command_arguments


def test_parse_command_arguments_none():
    assert parse_command_arguments(None) == {}


def test_parse_command_arguments_valid_json():
    assert parse_command_arguments('{"foo": "bar", "baz": 1}') == {
        "foo": "bar",
        "baz": 1,
    }


def test_parse_command_arguments_invalid_json():
    with pytest.raises(argparse.ArgumentTypeError) as excinfo:
        parse_command_arguments("invalid json")
    assert "Decode JSON:" in str(excinfo.value)
