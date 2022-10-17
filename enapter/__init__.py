__version__ = "0.4.0"

from . import async_, mdns, mqtt, types, vucm

__all__ = [
    "__version__",
    "async_",
    "mdns",
    "mqtt",
    "types",
    "vucm",
]

import json
import logging
import os
import sys

LOGGER = logging.getLogger(__package__)


def _init_logging():
    if LOGGER.handlers:
        return

    try:
        level = os.environ["ENAPTER_LOG_LEVEL"]
    except KeyError:
        LOGGER.addHandler(logging.NullHandler())
        return

    LOGGER.setLevel(level.upper())

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.formatter = logging.Formatter(
        json.dumps(
            {
                "time": "%(asctime)s",
                "level": "%(levelname).4s",
                "logger": "%(name)s",
                "message": "%(message)s",
            }
        )
    )
    LOGGER.addHandler(handler)


_init_logging()
