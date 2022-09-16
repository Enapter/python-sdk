import json
import logging
import sys


def new(name="main", level="INFO"):
    logger = logging.getLogger(name)

    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stderr)
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
    logger.addHandler(handler)

    logger.named = lambda name: named(logger, name)

    return logger


def named(parent, name):
    child = logging.getLogger(f"{parent.name}.{name}")
    child.named = lambda name: named(child, name)
    return child
