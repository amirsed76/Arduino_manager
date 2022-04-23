import json
from settings import Commands
import time
from datetime import datetime
import random

DATA = []


class ArduinoManager:
    def __init__(self, info_path, command_path):
        self.info_file = open(info_path, "r")
        self.command_file = open(command_path, "w")

    def get_data(self):
        # DATA.append({
        #            "MQ2": random.randint(0,1000),
        #            "MQ4": random.randint(0,1000),
        #            "MQ7": random.randint(0,1000),
        #            "MQ8": random.randint(0,1000),
        #            "MQ135": random.randint(0,1000),
        #            "MQ137": random.randint(0,1000)
        #        })
        # return DATA
        self.info_file.seek(0)
        return json.load(self.info_file)

    def write_command(self, command):
        now = datetime.now()
        command_data = {
            "command": command,
            "datetime": str(now)
        }
        self.command_file.truncate(0)
        self.info_file.seek(0)
        json.dump(command_data, self.command_file)

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
