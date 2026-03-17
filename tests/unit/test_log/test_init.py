import io
import logging

import enapter


def test_configure_level_none():
    enapter.log.configure(level=None)
    assert len(enapter.log.LOGGER.handlers) == 1
    assert isinstance(enapter.log.LOGGER.handlers[0], logging.NullHandler)


def test_configure_level_str():
    enapter.log.configure(level="DEBUG")
    assert enapter.log.LOGGER.level == logging.DEBUG
    assert len(enapter.log.LOGGER.handlers) == 1
    handler = enapter.log.LOGGER.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert isinstance(handler.formatter, enapter.log.JSONFormatter)


def test_configure_level_int():
    enapter.log.configure(level=logging.INFO)
    assert enapter.log.LOGGER.level == logging.INFO
    assert len(enapter.log.LOGGER.handlers) == 1
    handler = enapter.log.LOGGER.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert isinstance(handler.formatter, enapter.log.JSONFormatter)


def test_configure_custom_stream():
    stream = io.StringIO()
    enapter.log.configure(level=logging.INFO, stream=stream)
    assert len(enapter.log.LOGGER.handlers) == 1
    handler = enapter.log.LOGGER.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert handler.stream is stream
