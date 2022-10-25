import logging

from .. import mqtt

LOGGER = logging.getLogger(__name__)


class Logger:
    def __init__(self, channel):
        self._channel = channel
        self._logger = self._new_logger(channel.hardware_id, channel.channel_id)

    @staticmethod
    def _new_logger(hardware_id, channel_id):
        extra = {"hardware_id": hardware_id, "channel_id": channel_id}
        return logging.LoggerAdapter(LOGGER, extra=extra)

    async def debug(self, msg: str, persist: bool = False):
        self._logger.debug(msg)
        await self.log(msg, severity=mqtt.DeviceLogSeverity.DEBUG, persist=persist)

    async def info(self, msg: str, persist: bool = False):
        self._logger.info(msg)
        await self.log(msg, severity=mqtt.DeviceLogSeverity.INFO, persist=persist)

    async def warning(self, msg: str, persist: bool = False):
        self._logger.warning(msg)
        await self.log(msg, severity=mqtt.DeviceLogSeverity.WARNING, persist=persist)

    async def error(self, msg: str, persist: bool = False):
        self._logger.error(msg)
        await self.log(msg, severity=mqtt.DeviceLogSeverity.ERROR, persist=persist)

    async def log(
        self, msg: str, severity: mqtt.DeviceLogSeverity, persist: bool = False
    ):
        await self._channel.publish_logs(msg=msg, severity=severity, persist=persist)

    __call__ = log
