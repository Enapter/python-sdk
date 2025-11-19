import asyncio
import contextlib

import pytest

import enapter


async def test_properties_sender() -> None:
    ucm = enapter.standalone.UCM()
    async with asyncio.TaskGroup() as tg:
        run_task = tg.create_task(ucm.run())
        async with contextlib.aclosing(ucm.stream_properties()) as stream:
            properties = await asyncio.wait_for(stream.__anext__(), timeout=5)
            assert properties["virtual"] is True
            assert properties["lua_api_ver"] == 1
        run_task.cancel()


async def test_telemetry_sender() -> None:
    ucm = enapter.standalone.UCM()
    async with asyncio.TaskGroup() as tg:
        run_task = tg.create_task(ucm.run())
        async with contextlib.aclosing(ucm.stream_telemetry()) as stream:
            telemetry = await asyncio.wait_for(stream.__anext__(), timeout=5)
            assert telemetry == {}
        run_task.cancel()


async def test_cmd_reboot_not_implemented() -> None:
    ucm = enapter.standalone.UCM()
    with pytest.raises(NotImplementedError):
        await ucm.cmd_reboot()


async def test_cmd_upload_lua_script_not_implemented() -> None:
    ucm = enapter.standalone.UCM()
    with pytest.raises(NotImplementedError):
        await ucm.cmd_upload_lua_script()
