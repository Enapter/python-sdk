import abc
import asyncio
import traceback
from typing import Set

from .. import async_, mqtt


class Device(async_.Routine):

    CMD_PREFIX = "cmd_"

    def __init__(self, channel):
        self._channel = channel

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
                await self._channel.publish_logs(f"{task!r} failed: {e!r}", "error")
            except:
                pass
            raise

    async def __process_command_requests(self):
        async with self._channel.subscribe_to_command_requests() as reqs:
            async for req in reqs:
                state, payload = await self.__execute_command(req)
                resp = req.new_response(state, payload)
                await self._channel.publish_command_response(resp)

    async def __execute_command(self, req):
        try:
            cmd = getattr(self, self.CMD_PREFIX + req.name)
        except AttributeError:
            return mqtt.CommandState.ERROR, {"reason": "unknown command"}

        try:
            return mqtt.CommandState.COMPLETED, await cmd(**req.args)
        except:
            return mqtt.CommandState.ERROR, {"traceback": traceback.format_exc()}
