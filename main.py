from datetime import datetime
from tkinter import *
from tkinter import messagebox
from plotting import Plot
import random
import time
import settings
import threading
from arduinomanager import ArduinoManager
import matplotlib.pyplot as plt


class GUI:
    def __init__(self):
        self.plot = None
        self.allow_plotting = False
        self.arduino_manager = ArduinoManager(info_path=settings.INFORMATION_PATH, command_path=settings.COMMAND_PATH)
        self.data = []
        self.window = Tk()
        self.window.title('Plotting in Tkinter')
        x, y = 40, 40
        label_width, label_height = 100, 40
        padding = 10
        input_width, input_height = 30, 100

        time1_label = Label(self.window, text="arduino start time: ").place(x=x, y=y)
        self.time1_input = Entry(self.window, width=input_width)
        self.time1_input.place(x=x + label_width + padding, y=y)

        new_y = y + label_height + padding
        time2_label = Label(self.window, text="Modules off time: ").place(x=x, y=new_y)
        self.time2_input = Entry(self.window, width=input_width)
        self.time2_input.place(x=x + label_width + padding, y=new_y)

        new_y = y + 2 * (label_height + padding)
        time3_label = Label(self.window, text="arduino off time: ").place(x=x, y=new_y)
        self.time3_input = Entry(self.window, width=input_width)
        self.time3_input.place(x=x + label_width + padding, y=new_y)

        new_y = y + 3 * (label_height + padding)
        button = Button(self.window, text="plot", command=self.run_button, ).place(x=x, y=new_y)
        self.window.geometry(f"{x + label_width + padding + 200}x{new_y + 100}")
        self.window.resizable(False, False)

        self.window.mainloop()

    def plotting(self, time_plotting: int):
        self.allow_plotting = True
        self.window.withdraw()
        self.plot = Plot()
        self.plot.set_after_close(func=self.after_close_plot)
        index = 0
        self.plot.timer(max_time=time_plotting)
        for i in range(int(time_plotting // settings.SAMPLING_PERIOD) + 1):
            if len(self.data) > index:
                new_data = self.data[index]
                for key, value in new_data.items():

                    self.plot.update_line(line_name=key, y=value)
                    if not self.allow_plotting:
                        return
                index += 1
            self.plot.update_plot()
            time.sleep(settings.SAMPLING_PERIOD)

        now = datetime.now()
        self.plot.save(settings.PLOT_BASE_ADDRESS + f"{str(now).replace(':', '-').replace(' ', '-').replace('.', '-')}")

    def reading_data(self, time_getting):
        self.data = []
        for i in range(int(time_getting // settings.SAMPLING_PERIOD) + 1):
            self.data = self.arduino_manager.get_data()

    def run_button(self):

        try:
            start_time = int(self.time1_input.get())
            pick_time = int(self.time2_input.get())
            end_time = int(self.time3_input.get())
        except Exception as e:
            messagebox.showerror('خطا', f"اعداد وارد شده معتبر نمیباشند\n{e}")
            return
        arduino_thread = threading.Thread(target=self.arduino_manager.run, args=(start_time, pick_time, end_time))
        arduino_thread.start()

        data_thread = threading.Thread(target=self.reading_data, args=(start_time + pick_time + end_time,))
        data_thread.start()
        self.plotting(time_plotting=int(start_time + pick_time + end_time) + 1)

    def after_close_plot(self, event):
        self.allow_plotting = False
        self.window.deiconify()


if __name__ == '__main__':
    GUI()
