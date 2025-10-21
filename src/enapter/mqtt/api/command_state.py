import enum


class CommandState(enum.Enum):

    COMPLETED = "completed"
    ERROR = "error"
    LOG = "log"
