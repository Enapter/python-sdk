import logging
import os
import sys

from .json_formatter import JSONFormatter

LOGGER = logging.getLogger("enapter")
LEVEL = os.environ.get("ENAPTER_LOG_LEVEL")


def configure(level=LEVEL, stream=sys.stderr):
    if level is None:
        LOGGER.handlers = [logging.NullHandler()]
        return

    if isinstance(level, str):
        level = level.upper()

    LOGGER.setLevel(level)

    handler = logging.StreamHandler(stream)
    handler.formatter = JSONFormatter()

    LOGGER.handlers = [handler]


configure()

__all__ = [
    "JSONFormatter",
    "LEVEL",
    "LOGGER",
    "configure",
]
