import datetime
import logging
from typing import Any, Dict

import json_log_formatter  # type: ignore


class JSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(
        self,
        message: str,
        extra: Dict[str, Any],
        record: logging.LogRecord,
    ) -> Dict[str, Any]:
        try:
            del extra["taskName"]
        except KeyError:
            pass

        json_record = {
            "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "level": record.levelname[:4],
            "name": record.name,
            **extra,
        }

        if record.stack_info is not None:
            json_record["stack_info"] = record.stack_info

        if record.exc_info is not None:
            json_record["exc_info"] = self.formatException(record.exc_info)

        json_record["message"] = message

        return json_record

    def mutate_json_record(self, json_record: Dict[str, Any]) -> Dict[str, Any]:
        return json_record
