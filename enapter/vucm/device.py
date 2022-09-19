import abc
import asyncio
import traceback
from typing import Optional, Set

from .. import async_, mqtt, types
from .logger import Logger


class Device(async_.Routine):
    def __init__(self, channel, cmd_prefix="cmd_") -> None:
        self.__channel = channel
        self.__cmd_prefix = cmd_prefix

        self.log = Logger(channel=channel)
        self.alerts: Set[str] = set()

    async def send_telemetry(self, telemetry: Optional[types.JSON] = None) -> None:
        if telemetry is None:
            telemetry = {}

        telemetry.setdefault("alerts", list(self.alerts))

        await self.__channel.publish_telemetry(telemetry)

    async def send_properties(self, properties: Optional[types.JSON] = None) -> None:
        if properties is None:
            properties = {}

        await self.__channel.publish_properties(properties)

    @abc.abstractmethod
    async def _create_tasks(self) -> Set[asyncio.Task]:
        raise NotImplementedError

    async def _run(self):
        tasks = await self._create_tasks()

        for maybe_task in tasks:
            if not isinstance(maybe_task, asyncio.Task):
                tasks.remove(maybe_task)
                task = asyncio.create_task(maybe_task)
                tasks.add(task)

        tasks.add(
            asyncio.create_task(
                self.__process_command_requests(), name="command_requests_processor"
            )
        )

        self._started.set()

        try:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        except asyncio.CancelledError:
            pass

        finally:
            for task in tasks:
                task.cancel()
                self._stack.push_async_callback(self.__wait_task, task)

    async def __wait_task(self, task):
        try:
            await task
        except asyncio.CancelledError:
            pass
        except Exception as e:
            try:
                await self.__channel.publish_logs(f"{task!r} failed: {e!r}", "error")
            except:
                pass
            raise

    async def __process_command_requests(self):
        async with self.__channel.subscribe_to_command_requests() as reqs:
            async for req in reqs:
                state, payload = await self.__execute_command(req)
                resp = req.new_response(state, payload)
                await self.__channel.publish_command_response(resp)

    async def __execute_command(self, req):
        try:
            cmd = getattr(self, self.__cmd_prefix + req.name)
        except AttributeError:
            return mqtt.CommandState.ERROR, {"reason": "unknown command"}

        try:
            return mqtt.CommandState.COMPLETED, await cmd(**req.args)
        except:
            return mqtt.CommandState.ERROR, {"traceback": traceback.format_exc()}
