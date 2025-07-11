import contextlib
import io
import json
import re

import enapter


class TestJSONFormat:
    def test_record_ends_with_newline(self):
        buf = io.StringIO()

        with self.configure(level="info", stream=buf):
            enapter.log.LOGGER.info("hello")

        assert buf.getvalue().endswith("\n")

    def test_record_fields(self):
        buf = io.StringIO()

        with self.configure(level="info", stream=buf):
            enapter.log.LOGGER.info("hello")

        record = json.loads(buf.getvalue())

        time = record.pop("time")
        assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+", time) is not None

        assert record["level"] == "INFO"
        assert record["name"] == "enapter"
        assert record["message"] == "hello"

    def test_exc_info(self):
        buf = io.StringIO()

        with self.configure(level="info", stream=buf):
            try:
                raise RuntimeError("oops")
            except RuntimeError:
                enapter.log.LOGGER.exception("boom")

        record = json.loads(buf.getvalue())

        assert record["message"] == "boom"
        assert "Traceback (most recent call last)" in record["exc_info"]
        assert 'RuntimeError("oops")' in record["exc_info"]

    def test_stack_info(self):
        buf = io.StringIO()

        with self.configure(level="info", stream=buf):
            enapter.log.LOGGER.info("hello", stack_info=True)

        record = json.loads(buf.getvalue())

        assert record["message"] == "hello"
        assert "Stack (most recent call last)" in record["stack_info"]
        assert "test_stack_info" in record["stack_info"]

    @staticmethod
    @contextlib.contextmanager
    def configure(*args, **kwargs):
        enapter.log.configure(*args, **kwargs)
        try:
            yield
        finally:
            enapter.log.configure(level=None)
