import asyncio
import contextlib

import pytest

import enapter


class Device(enapter.standalone.Device):

    async def run(self) -> None:
        pass

    async def cmd_test(self, value: int) -> dict:
        return {"echo": value}


async def test_device_command() -> None:
    device = Device()
    result = await device.execute_command("test", {"value": 42})
    assert result == {"result": {"echo": 42}}


async def test_device_command_not_implemented() -> None:
    device = Device()
    with pytest.raises(NotImplementedError):
        await device.execute_command("non_existing_command", {})


async def test_device_logging() -> None:
    device = Device()
    await device.logger.info("Test log message")
    async with contextlib.aclosing(device.stream_logs()) as stream:
        log = await asyncio.wait_for(stream.__anext__(), timeout=5)
        assert log.message == "Test log message"
