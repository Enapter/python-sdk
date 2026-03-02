"""Rule Engine states."""

import enum


class EngineState(enum.Enum):
    """Enumeration of rule engine states."""

    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
