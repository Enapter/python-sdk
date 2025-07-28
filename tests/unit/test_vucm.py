import asyncio
import contextlib

import enapter


class TestDevice:
    async def test_run_in_thread(self, fake):
        async with enapter.vucm.Device(channel=MockChannel(fake)) as device:
            assert not device._Device__thread_pool_executor._shutdown
            assert await device.run_in_thread(lambda: 42) == 42
        assert device._Device__thread_pool_executor._shutdown

    async def test_task_marks(self, fake):
        class MyDevice(enapter.vucm.Device):
            async def task_foo(self):
                pass

            @enapter.vucm.device_task
            async def task_bar(self):
                pass

            @enapter.vucm.device_task
            async def baz(self):
                pass

            @enapter.vucm.device_task
            async def goo(self):
                pass

        async with MyDevice(channel=MockChannel(fake)) as device:
            tasks = device._Device__tasks
            assert len(tasks) == 3
            assert "task_foo" not in tasks
            assert "task_bar" in tasks
            assert "baz" in tasks
            assert "goo" in tasks

    async def test_command_marks(self, fake):
        class MyDevice(enapter.vucm.Device):
            async def cmd_foo(self):
                pass

            async def cmd_foo2(self, a, b, c):
                pass

            @enapter.vucm.device_command
            async def cmd_bar(self):
                pass

            @enapter.vucm.device_command
            async def cmd_bar2(self, a, b, c):
                pass

            @enapter.vucm.device_command
            async def baz(self):
                pass

            @enapter.vucm.device_command
            async def baz2(self, a, b, c):
                pass

            @enapter.vucm.device_command
            async def goo(self):
                pass

        async with MyDevice(channel=MockChannel(fake)) as device:
            commands = device._Device__commands
            assert len(commands) == 5
            assert "cmd_foo" not in commands
            assert "cmd_foo2" not in commands
            assert "cmd_bar" in commands
            assert "cmd_bar2" in commands
            assert "baz" in commands
            assert "baz2" in commands
            assert "goo" in commands

    async def test_task_and_commands_marks(self, fake):
        class MyDevice(enapter.vucm.Device):
            @enapter.vucm.device_task
            async def foo_task(self):
                pass

            @enapter.vucm.device_task
            async def bar_task(self):
                pass

            @enapter.vucm.device_command
            async def foo_command(self):
                pass

            @enapter.vucm.device_command
            async def bar_command(self):
                pass

        async with MyDevice(channel=MockChannel(fake)) as device:
            tasks = device._Device__tasks
            assert len(tasks) == 2
            assert "foo_task" in tasks
            assert "bar_task" in tasks
            assert "foo_command" not in tasks
            assert "bar_command" not in tasks
            commands = device._Device__commands
            assert "foo_task" not in commands
            assert "bar_task" not in commands
            assert "foo_command" in commands
            assert "bar_command" in commands


class MockChannel:
    def __init__(self, fake):
        self.hardware_id = fake.hardware_id()
        self.channel_id = fake.channel_id()

    @contextlib.asynccontextmanager
    async def subscribe_to_command_requests(self, *args, **kwargs):
        await asyncio.Event().wait()
        yield
