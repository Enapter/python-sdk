import logging
import time
from typing import Optional

from enapter import mqtt

LOGGER = logging.getLogger(__name__)


class Logger:

    def __init__(self, channel: mqtt.api.DeviceChannel) -> None:
        self._channel = channel
        self._logger = self._new_logger(channel.hardware_id, channel.channel_id)

    @staticmethod
    def _new_logger(hardware_id, channel_id) -> logging.LoggerAdapter:
        extra = {"hardware_id": hardware_id, "channel_id": channel_id}
        return logging.LoggerAdapter(LOGGER, extra=extra)

    async def debug(self, msg: str, persist: Optional[bool] = None) -> None:
        self._logger.debug(msg)
        await self._log(msg, severity=mqtt.api.LogSeverity.DEBUG, persist=persist)

    async def info(self, msg: str, persist: Optional[bool] = None) -> None:
        self._logger.info(msg)
        await self._log(msg, severity=mqtt.api.LogSeverity.INFO, persist=persist)

    async def warning(self, msg: str, persist: Optional[bool] = None) -> None:
        self._logger.warning(msg)
        await self._log(msg, severity=mqtt.api.LogSeverity.WARNING, persist=persist)

    async def error(self, msg: str, persist: Optional[bool] = None) -> None:
        self._logger.error(msg)
        await self._log(msg, severity=mqtt.api.LogSeverity.ERROR, persist=persist)

    async def _log(
        self,
        msg: str,
        severity: mqtt.api.LogSeverity,
        persist: Optional[bool] = None,
    ) -> None:
        await self._channel.publish_log(
            mqtt.api.Log(
                message=msg,
                severity=severity,
                persist=persist if persist is not None else False,
                timestamp=int(time.time()),
            )
        )
