"""Rule states."""

import enum


class RuleState(enum.Enum):
    """Enumeration of rule states."""

    STARTED = "STARTED"
    STOPPED = "STOPPED"
