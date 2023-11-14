import asyncio
import concurrent
import functools
import traceback
from typing import Optional, Set

import enapter

from .logger import Logger


class Device(enapter.async_.Routine):
    def __init__(
        self,
        channel,
        cmd_prefix="cmd_",
        task_prefix="task_",
        thread_pool_executor=None,
    ) -> None:
        self.__channel = channel

        self.__cmd_prefix = cmd_prefix
        self.__task_prefix = task_prefix

        if thread_pool_executor is None:
            thread_pool_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.__thread_pool_executor = thread_pool_executor

        self.log = Logger(channel=channel)
        self.alerts: Set[str] = set()

    async def send_telemetry(
        self, telemetry: Optional[enapter.types.JSON] = None
    ) -> None:
        if telemetry is None:
            telemetry = {}
        else:
            telemetry = telemetry.copy()

        telemetry.setdefault("alerts", list(self.alerts))

        await self.__channel.publish_telemetry(telemetry)

    async def send_properties(
        self, properties: Optional[enapter.types.JSON] = None
    ) -> None:
        if properties is None:
            properties = {}
        else:
            properties = properties.copy()

        await self.__channel.publish_properties(properties)

    async def run_in_thread(self, func, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.__thread_pool_executor, functools.partial(func, *args, **kwargs)
        )

    async def _run(self):
        self._stack.enter_context(self.__thread_pool_executor)

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
            return enapter.mqtt.CommandState.ERROR, {"reason": "unknown command"}

        try:
            return enapter.mqtt.CommandState.COMPLETED, await cmd(**req.args)
        except:
            return enapter.mqtt.CommandState.ERROR, {
                "traceback": traceback.format_exc()
            }
