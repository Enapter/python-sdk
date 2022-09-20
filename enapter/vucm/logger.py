from .. import mqtt


class Logger:
    def __init__(self, channel):
        self.__channel = channel

    async def debug(self, msg: str, persist: bool = False):
        await self.log(msg, severity=mqtt.DeviceLogSeverity.DEBUG, persist=persist)

    async def info(self, msg: str, persist: bool = False):
        await self.log(msg, severity=mqtt.DeviceLogSeverity.INFO, persist=persist)

    async def warning(self, msg: str, persist: bool = False):
        await self.log(msg, severity=mqtt.DeviceLogSeverity.WARNING, persist=persist)

    async def error(self, msg: str, persist: bool = False):
        await self.log(msg, severity=mqtt.DeviceLogSeverity.ERROR, persist=persist)

    async def log(
        self, msg: str, severity: mqtt.DeviceLogSeverity, persist: bool = False
    ):
        await self.__channel.publish_logs(msg=msg, severity=severity, persist=persist)

    __call__ = log
