import asyncio
import concurrent
import functools
import traceback
from typing import Any, Callable, Coroutine, Optional, Set

import enapter

from .logger import Logger

DEVICE_TASK_MARK = "_enapter_vucm_device_task"
DEVICE_COMMAND_MARK = "_enapter_vucm_device_command"

DeviceTaskFunc = Callable[[Any], Coroutine]
DeviceCommandFunc = Callable[..., Coroutine]


def device_task(func: DeviceTaskFunc) -> DeviceTaskFunc:
    setattr(func, DEVICE_TASK_MARK, True)
    return func


def device_command(func: DeviceCommandFunc) -> DeviceTaskFunc:
    setattr(func, DEVICE_COMMAND_MARK, True)
    return func


def is_device_task(func: DeviceTaskFunc) -> bool:
    return getattr(func, DEVICE_TASK_MARK, False) is True


def is_device_command(func: DeviceCommandFunc) -> bool:
    return getattr(func, DEVICE_COMMAND_MARK, False) is True


class Device(enapter.async_.Routine):
    def __init__(self, channel, thread_pool_workers: int = 1) -> None:
        self.__channel = channel

        self.__tasks = {}
        for name in dir(self):
            obj = getattr(self, name)
            if is_device_task(obj):
                self.__tasks[name] = obj

        self.__commands = {}
        for name in dir(self):
            obj = getattr(self, name)
            if is_device_command(obj):
                self.__commands[name] = obj

        self.__thread_pool_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=thread_pool_workers
        )

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

        for name, func in self.__tasks.items():
            tasks.add(asyncio.create_task(func(), name=name))

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
            cmd = self.__commands[req.name]
        except KeyError:
            return enapter.mqtt.api.CommandState.ERROR, {"reason": "unknown command"}

        try:
            return enapter.mqtt.api.CommandState.COMPLETED, await cmd(**req.args)
        except:
            return enapter.mqtt.api.CommandState.ERROR, {
                "traceback": traceback.format_exc()
            }
