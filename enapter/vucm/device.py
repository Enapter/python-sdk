import asyncio
import traceback
from typing import Optional, Set

from .. import async_, mqtt, types
from .logger import Logger


class Device(async_.Routine):
    def __init__(self, channel, cmd_prefix="cmd_", task_prefix="task_") -> None:
        self.__channel = channel

        self.__cmd_prefix = cmd_prefix
        self.__task_prefix = task_prefix

        self.log = Logger(channel=channel)
        self.alerts: Set[str] = set()

    async def send_telemetry(self, telemetry: Optional[types.JSON] = None) -> None:
        if telemetry is None:
            telemetry = {}
        else:
            telemetry = telemetry.copy()

        telemetry.setdefault("alerts", list(self.alerts))

        await self.__channel.publish_telemetry(telemetry)

    async def send_properties(self, properties: Optional[types.JSON] = None) -> None:
        if properties is None:
            properties = {}
        else:
            properties = properties.copy()

        await self.__channel.publish_properties(properties)

    async def _run(self):
        tasks = set()

        for name in dir(self):
            if name.startswith(self.__task_prefix):
                task_func = getattr(self, name)
                name_without_prefix = name[len(self.__task_prefix) :]
                tasks.add(asyncio.create_task(task_func(), name=name_without_prefix))

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
                await self.log.error(f"device task {task.get_name()!r} failed: {e!r}")
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
