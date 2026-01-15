import enum


class Aggregation(enum.Enum):

    AUTO = "AUTO"
    AVG = "AVG"
    LAST = "LAST"
    MIN = "MIN"
    MAX = "MAX"
    BOOL_OR = "BOOL_OR"
