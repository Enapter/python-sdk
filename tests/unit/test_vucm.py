import asyncio
import contextlib

import enapter


class TestDevice:
    async def test_run_in_thread(self, fake):
        async with enapter.vucm.Device(channel=MockChannel(fake)) as device:
            assert not device._Device__thread_pool_executor._shutdown
            assert await device.run_in_thread(lambda: 42) == 42
        assert device._Device__thread_pool_executor._shutdown


class MockChannel:
    def __init__(self, fake):
        self.hardware_id = fake.hardware_id()
        self.channel_id = fake.channel_id()

    @contextlib.asynccontextmanager
    async def subscribe_to_command_requests(self, *args, **kwargs):
        await asyncio.Event().wait()
        yield
