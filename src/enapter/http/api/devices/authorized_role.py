import enum


class AuthorizedRole(enum.Enum):

    READONLY = "READONLY"
    USER = "USER"
    OWNER = "OWNER"
    INSTALLER = "INSTALLER"
    SYSTEM = "SYSTEM"
    VENDOR = "VENDOR"
