from datetime import datetime
from tkinter import *
from tkinter import messagebox
from plotting import Plot
import random
import time
import settings
import threading
from arduinomanager import ArduinoManager


class GUI:
    def __init__(self):
        self.plot = None
        self.allow_plotting = False
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

    def run_button(self):

        try:
            start_time = int(self.time1_input.get())
            pick_time = int(self.time2_input.get())
            end_time = int(self.time3_input.get())
        except Exception as e:
            messagebox.showerror('خطا', f"اعداد وارد شده معتبر نمیباشند\n{e}")
            return
        arduino_manager = ArduinoManager(info_path=settings.INFORMATION_PATH, command_path=settings.COMMAND_PATH)
        arduino_thread = threading.Thread(target=arduino_manager.run, args=(start_time, pick_time, end_time))
        arduino_thread.start()
        # TODO command to arduino for start and off Modules and finish

        self.allow_plotting = True
        self.window.withdraw()
        self.plot = Plot()
        self.plot.set_after_close(func=self.after_close_plot)
        for i in range(10):
            number1 = random.randint(0, 10)
            number2 = random.randint(0, 10)
            number3 = random.randint(0, 10)
            self.plot.update_line(line_name="a", y=number1)
            self.plot.update_line(line_name="b", y=number2)
            self.plot.update_line(line_name="c", y=number3)
            self.plot.update_plot()
            if not self.allow_plotting:
                return
            time.sleep(0.2)
        now = datetime.now()
        self.plot.save(
            settings.PLOT_BASE_ADDRESS + f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}")

        arduino_thread.join(timeout=start_time + pick_time + end_time + 2)
        # self.plot.close()

    def after_close_plot(self, event):
        self.allow_plotting = False
        self.window.deiconify()
        # self.__init__()


if __name__ == '__main__':
    GUI()