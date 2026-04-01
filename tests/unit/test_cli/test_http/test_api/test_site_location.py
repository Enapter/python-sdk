import argparse

import pytest

from enapter.cli.http.api.site_location import parse_site_location


def test_parse_site_location_valid():
    assert parse_site_location("Berlin,52.52,13.405") == ("Berlin", 52.52, 13.405)


def test_parse_site_location_with_spaces():
    # Note: name strips whitespace, float() handles surrounding whitespace
    assert parse_site_location(" Berlin , 52.52 , 13.405 ") == (
        "Berlin",
        52.52,
        13.405,
    )


def test_parse_site_location_too_few_parts():
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        parse_site_location("Berlin,52.52")
    assert "Location must be in the format NAME,LATITUDE,LONGITUDE" in str(
        exc_info.value
    )


def test_parse_site_location_too_many_parts():
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        parse_site_location("Berlin,52.52,13.405,extra")
    assert "Location must be in the format NAME,LATITUDE,LONGITUDE" in str(
        exc_info.value
    )


def test_parse_site_location_invalid_latitude():
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        parse_site_location("Berlin,invalid,13.405")
    assert "Location must be in the format NAME,LATITUDE,LONGITUDE" in str(
        exc_info.value
    )


def test_parse_site_location_invalid_longitude():
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        parse_site_location("Berlin,52.52,invalid")
    assert "Location must be in the format NAME,LATITUDE,LONGITUDE" in str(
        exc_info.value
    )


def test_parse_site_location_empty():
    with pytest.raises(argparse.ArgumentTypeError) as exc_info:
        parse_site_location("")
    assert "Location must be in the format NAME,LATITUDE,LONGITUDE" in str(
        exc_info.value
    )
