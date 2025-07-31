import datetime

import json_log_formatter


class JSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
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

    def mutate_json_record(self, json_record):
        return json_record
