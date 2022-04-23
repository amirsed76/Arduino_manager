import json
from settings import Commands
import time
from datetime import datetime


class ArduinoManager:
    def __init__(self, info_path, command_path):
        self.info_path = info_path
        self.command_path = command_path

    now = datetime.now()

    def get_data(self):
        with open(self.info_path, "r") as f:
            data = json.load(f)
        return data

    def write_command(self, command):
        now = datetime.now()
        command_data = {
            "command": command,
            "datetime": str(now)
        }

        with open(self.command_path, "w") as f:
            json.dump(command_data, f)

    def start(self):
        self.write_command(Commands.ON.value)

    def finish(self):
        self.write_command(Commands.OFF.value)

    def off_modules(self):
        self.write_command(Commands.OFF_MODULES.value)

    def run(self, time1, time2, time3):
        time.sleep(time1)
        self.start()
        time.sleep(time2)
        self.off_modules()
        time.sleep(time3)
        self.finish()
