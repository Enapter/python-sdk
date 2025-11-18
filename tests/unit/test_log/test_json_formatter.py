import contextlib
import io
import json
import re
from typing import Generator

import enapter


def test_record_ends_with_newline() -> None:
    buf = io.StringIO()

    with configure_logging(level="info", stream=buf):
        enapter.log.LOGGER.info("hello")

    assert buf.getvalue().endswith("\n")


def test_record_fields() -> None:
    buf = io.StringIO()

    with configure_logging(level="info", stream=buf):
        enapter.log.LOGGER.info("hello")

    record = json.loads(buf.getvalue())

    time = record.pop("time")
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+", time) is not None

    assert record["level"] == "INFO"
    assert record["name"] == "enapter"
    assert record["message"] == "hello"


def test_exc_info() -> None:
    buf = io.StringIO()

    with configure_logging(level="info", stream=buf):
        try:
            raise RuntimeError("oops")
        except RuntimeError:
            enapter.log.LOGGER.exception("boom")

    record = json.loads(buf.getvalue())

    assert record["message"] == "boom"
    assert "Traceback (most recent call last)" in record["exc_info"]
    assert 'RuntimeError("oops")' in record["exc_info"]


def test_stack_info() -> None:
    buf = io.StringIO()

    with configure_logging(level="info", stream=buf):
        enapter.log.LOGGER.info("hello", stack_info=True)

    record = json.loads(buf.getvalue())

    assert record["message"] == "hello"
    assert "Stack (most recent call last)" in record["stack_info"]
    assert "test_stack_info" in record["stack_info"]


@contextlib.contextmanager
def configure_logging(*args, **kwargs) -> Generator[None, None, None]:
    enapter.log.configure(*args, **kwargs)
    try:
        yield
    finally:
        enapter.log.configure(level=None)
