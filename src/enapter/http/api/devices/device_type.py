import enum


class DeviceType(enum.Enum):

    LUA = "LUA"
    VIRTUAL_UCM = "VIRTUAL_UCM"
    HARDWARE_UCM = "HARDWARE_UCM"
    STANDALONE = "STANDALONE"
    GATEWAY = "GATEWAY"
