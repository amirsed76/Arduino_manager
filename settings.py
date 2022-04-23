import enum

INFORMATION_PATH = "information.json"
PLOT_BASE_ADDRESS = "plots/"
SAMPLING_PERIOD = 0.1
COMMAND_PATH = "command.json"


class Commands(enum.Enum):
    ON = "ON"
    OFF_MODULES = "OFF_MODULES"
    OFF = "OFF"
