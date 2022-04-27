from datetime import datetime
from tkinter import *
from tkinter import messagebox
from plotting import Plot
import time
import settings
import threading
import json


def write_command(first_time, second_time, third_time, cycle):
    info = {
        "date_time": str(datetime.now()),
        "first_time": first_time,
        "second_time": second_time,
        "third_time": third_time,
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

                index += 1
            if not self.allow_plotting:
                print("it's ok")
                return
            self.plot.update_plot()
            time.sleep(settings.SAMPLING_PERIOD)

        now = datetime.now()
        self.plot.save(settings.PLOT_BASE_ADDRESS + f"{str(now).replace(':', '-').replace(' ', '-').replace('.', '-')}")

    def reading_data(self, time_getting):
        self.data = []
        for i in range(int(time_getting // settings.SAMPLING_PERIOD) + 1):
            # TODO read data
            self.data = self.arduino_manager.get_data()

    def run_button(self):

        try:
            on_time = int(self.time1_input.get())
            first_time = int(self.time2_input.get())
            second_time = int(self.time3_input.get())
            third_time = int(self.time4_input.get())
            off_time = int(self.time5_input.get())
            cycle = int(self.cycle_input.get())

            if not (0 < on_time < first_time < second_time < third_time < off_time) or cycle < 1:
                raise Exception("اعداد وارد شده معتبر نمیباشند")
        except Exception as e:
            messagebox.showerror('خطا', f"{e}")
            return

        write_command(first_time=first_time, second_time=second_time, third_time=third_time, cycle=cycle)

        arduino_thread = threading.Thread(target=self.arduino_manager.run, args=(start_time, pick_time, end_time))
        arduino_thread.daemon = True
        arduino_thread.start()

        data_thread = threading.Thread(target=self.reading_data, args=(start_time + pick_time + end_time,))
        data_thread.daemon = True
        data_thread.start()
        self.plotting(time_plotting=int(start_time + pick_time + end_time) + 1)

    def after_close_plot(self, event):
        self.allow_plotting = False
        self.window.deiconify()


if __name__ == '__main__':
    GUI()
