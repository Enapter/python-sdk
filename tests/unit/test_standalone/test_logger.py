import asyncio

import enapter


async def test_debug() -> None:
    queue = asyncio.Queue[enapter.standalone.Log]()
    logger = enapter.standalone.Logger(queue=queue)
    await logger.debug("Debug message", persist=True)
    log = await queue.get()
    assert log.severity == "debug"
    assert log.message == "Debug message"
    assert log.persist


async def test_info() -> None:
    queue = asyncio.Queue[enapter.standalone.Log]()
    logger = enapter.standalone.Logger(queue=queue)
    await logger.info("Info message", persist=False)
    log = await queue.get()
    assert log.severity == "info"
    assert log.message == "Info message"
    assert not log.persist


async def test_warning() -> None:
    queue = asyncio.Queue[enapter.standalone.Log]()
    logger = enapter.standalone.Logger(queue=queue)
    await logger.warning("Warning message", persist=True)
    log = await queue.get()
    assert log.severity == "warning"
    assert log.message == "Warning message"
    assert log.persist


async def test_error() -> None:
    queue = asyncio.Queue[enapter.standalone.Log]()
    logger = enapter.standalone.Logger(queue=queue)
    await logger.error("Error message", persist=False)
    log = await queue.get()
    assert log.severity == "error"
    assert log.message == "Error message"
    assert not log.persist


async def test_default_persist() -> None:
    queue = asyncio.Queue[enapter.standalone.Log]()
    logger = enapter.standalone.Logger(queue=queue)
    await logger.info("Default persist message")
    log = await queue.get()
    assert log.severity == "info"
    assert log.message == "Default persist message"
    assert not log.persist
