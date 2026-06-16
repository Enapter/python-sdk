import enum


class AccessRole(enum.Enum):
    """Enumeration of access roles returned by the Enapter HTTP API."""

    READONLY = "READONLY"
    USER = "USER"
    OWNER = "OWNER"
    INSTALLER = "INSTALLER"
    SYSTEM = "SYSTEM"
    VENDOR = "VENDOR"
