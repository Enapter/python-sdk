import enum
import json


class DataType(enum.Enum):

    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    STRING = "STRING"
    STRING_ARRAY = "STRING_ARRAY"
    BOOLEAN = "BOOLEAN"

    def parse_value(self, s: str) -> float | int | str | list[str] | bool | None:
        if not s:
            return None
        match self:
            case DataType.FLOAT:
                return float(s)
            case DataType.INTEGER:
                return int(s)
            case DataType.STRING:
                return s
            case DataType.STRING_ARRAY:
                return json.loads(s)
            case DataType.BOOLEAN:
                if s.lower() in ("true", "1"):
                    return True
                elif s.lower() in ("false", "0"):
                    return False
                else:
                    raise ValueError(f"invalid boolean value: {s}")
