import random
import time
import json
import threading
import numpy as np
from settings import *
import datetime
from plotting import Plot


class Arduino:
    def __init__(self, info_path):
        self.info_path = info_path

    def get_data(self):
        with open(self.info_path, "r") as f:
            data = json.load(f)

        return data

    def start(self):
        pass

    def finish(self):
        pass

    def off_modules(self):
        pass


class Manager:
    def __init__(self, info_path, plot_base_address, start_time, pick_time, end_time):
        self.arduino = Arduino(info_path=info_path)
        self.plot = Plot(is_show=True)
        self.start_time = start_time
        self.pick_time = pick_time
        self.end_time = end_time
        self._finish = False
        self.plot_base_address = plot_base_address

    def plotting(self):
        while True:
            if self._finish:
                break

            time.sleep(0.5)
            # data = self.arduino.get_data()
            new_data = random.randint(0, 10)
            if new_data > 4:
                self.plot.update_plot(new_data)

            if self._finish:
                break

    def arduino_process(self):
        time.sleep(self.start_time)
        self.arduino.start()
        print("start board")
        time.sleep(self.pick_time)
        self.arduino.off_modules()
        print("off Modules")
        time.sleep(self.end_time)
        self.arduino.finish()
        print("finish board")
        self._finish = True

    def run(self):
        thread = threading.Thread(target=self.arduino_process)
        thread.start()
        self.plotting()
        now = datetime.datetime.now()
        self.plot.save(
            self.plot_base_address + f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}")


if __name__ == '__main__':
    first_time = int(input("first time? "))
    second_time = int(input("second time? "))
    third_time = int(input("third time? "))
    manager = Manager(info_path=INFORMATION_PATH, plot_base_address=PLOT_BASE_ADDRESS,
                      start_time=first_time,
                      pick_time=second_time, end_time=third_time)

    manager.run()
