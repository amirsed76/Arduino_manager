from datetime import datetime
from tkinter import *
from tkinter import messagebox
from plotting import Plot
import time
import threading
import json
import pandas as pd


class Setting:
    with open("settings.json", "r") as f:
        data = json.load(f)
        INFORMATION_PATH = data["INFORMATION_PATH"]
        PLOT_BASE_ADDRESS = data["PLOT_BASE_ADDRESS"]
        SAMPLING_PERIOD = data["SAMPLING_PERIOD"]
        COMMAND_PATH = data["COMMAND_PATH"]
        CSV_BASE_ADDRESS = data["CSV_BASE_ADDRESS"]


settings = Setting()


def write_command(on_time, first_time, second_time, third_time, off_time, cycle):
    info = {
        "date_time": str(datetime.now()),
        "on_time": on_time,
        "first_time": first_time,
        "second_time": second_time,
        "third_time": third_time,
        "off_time": off_time,
        "cycle": cycle
    }
    with open(settings.COMMAND_PATH, "w") as f:
        json.dump(info, f)


class GUI:
    def __init__(self):
        self.plot = None
        self.allow_plotting = False
        self.data = []
        self.window = Tk()
        self.window.title('Plotting in Tkinter')
        self.info_file = None

        x, y = 40, 40
        label_width, label_height = 100, 40
        padding = 10
        input_width, input_height = 30, 100

        time1_label = Label(self.window, text="on time: ").place(x=x, y=y)
        self.time1_input = Entry(self.window, width=input_width)
        self.time1_input.place(x=x + label_width + padding, y=y)

        new_y = y + label_height + padding
        time2_label = Label(self.window, text="first time: ").place(x=x, y=new_y)
        self.time2_input = Entry(self.window, width=input_width)
        self.time2_input.place(x=x + label_width + padding, y=new_y)

        new_y = y + 2 * (label_height + padding)
        time3_label = Label(self.window, text="second time: ").place(x=x, y=new_y)
        self.time3_input = Entry(self.window, width=input_width)
        self.time3_input.place(x=x + label_width + padding, y=new_y)

        new_y = y + 3 * (label_height + padding)
        time4_label = Label(self.window, text="third time: ").place(x=x, y=new_y)
        self.time4_input = Entry(self.window, width=input_width)
        self.time4_input.place(x=x + label_width + padding, y=new_y)

        new_y = y + 4 * (label_height + padding)
        time5_label = Label(self.window, text="off time: ").place(x=x, y=new_y)
        self.time5_input = Entry(self.window, width=input_width)
        self.time5_input.place(x=x + label_width + padding, y=new_y)

        new_y = y + 5 * (label_height + padding)
        cycle_label = Label(self.window, text="cycle: ").place(x=x, y=new_y)
        self.cycle_input = Entry(self.window, width=input_width)
        self.cycle_input.place(x=x + label_width + padding, y=new_y)

        new_y = y + 6 * (label_height + padding)
        button = Button(self.window, text="confirm", command=self.run_button, ).place(x=x, y=new_y)
        self.window.geometry(f"{x + label_width + padding + 200}x{new_y + 100}")

        self.window.resizable(False, False)
        self.window.mainloop()

    def plotting(self, start_plotting, end_plotting):
        self.allow_plotting = True
        self.window.withdraw()
        self.plot = Plot()
        self.plot.set_after_close(func=self.after_close_plot)
        index = 0
        self.plot.timer(max_time=end_plotting)
        start_time = time.time()
        data_gen = self.reading_data(on_time=start_plotting, off_time=end_plotting)
        while True:
            passed_time = time.time() - start_time
            if passed_time >= end_plotting:
                time.sleep(settings.SAMPLING_PERIOD)
                break

            elif passed_time >= start_plotting:
                try:
                    new_data = data_gen.__next__()
                    if new_data is not None:
                        # new_data = self.data[index]
                        for key, value in new_data.items():
                            self.plot.update_line(line_name=str(key), y=value)
                except StopIteration:
                    print("stop iteration")

                index += 1
            if not self.allow_plotting:
                print("plot has been finished")
                return
            self.plot.update_plot()

        now = datetime.now()
        time_str = f"{str(now).replace(':', '-').replace(' ', '-').replace('.', '-')}"
        self.plot.save(settings.PLOT_BASE_ADDRESS + time_str)
        pd.read_json(settings.INFORMATION_PATH).to_csv(settings.CSV_BASE_ADDRESS + time_str + ".csv")

    def read_file(self):
        while True:
            self.info_file.seek(0)
            self.data = json.load(self.info_file)
            time.sleep(settings.SAMPLING_PERIOD / 3)
            if not self.allow_plotting:
                return

    def reading_data(self, on_time, off_time):
        start_time = time.time()
        self.data = []
        read_file_thread = threading.Thread(target=self.read_file)
        self.info_file = open(settings.INFORMATION_PATH, "r")
        read_file_thread.start()
        index = 0

        while True:
            self.info_file.seek(0)
            if len(self.data) > index:
                new_item = self.data[index]
                cycle = new_item.pop("cycle")
                yield dict([(k + f'_{cycle}', v) for k, v in new_item.items()])
                index += 1
            else:
                yield None
                time.sleep(settings.SAMPLING_PERIOD / 3)
            if not self.allow_plotting:
                return

    def run_button(self):

        try:
            on_time = int(self.time1_input.get())
            first_time = int(self.time2_input.get())
            second_time = int(self.time3_input.get())
            third_time = int(self.time4_input.get())
            off_time = int(self.time5_input.get())
            cycle = int(self.cycle_input.get())

            if not (0 <= on_time <= first_time <= second_time <= third_time <= off_time) or cycle < 1:
                raise Exception("اعداد وارد شده معتبر نمیباشند")
        except Exception as e:
            messagebox.showerror('خطا', f"{e}")
            return

        write_command(first_time=first_time, second_time=second_time, third_time=third_time, cycle=cycle,
                      on_time=on_time, off_time=off_time)
        self.plotting(start_plotting=first_time, end_plotting=third_time*cycle)

    def after_close_plot(self, event):
        self.allow_plotting = False
        self.window.deiconify()


if __name__ == '__main__':
    GUI()
