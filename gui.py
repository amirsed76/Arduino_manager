from datetime import datetime
from tkinter import *
from plotting import Plot
import random
import threading
import time
import matplotlib.pyplot as plt
import settings


# plot function is created for
# plotting the graph in
# tkinter window

class GUI:
    def __init__(self):
        self.plot = None
        self.allow_plotting = False
        self.window = Tk()
        self.window.title('Plotting in Tkinter')
        self.window.geometry("500x500")
        x, y = 40, 40
        label_width = 100
        label_height = 40
        padding = 10

        time1_label = Label(self.window, text="arduino start time: ").place(x=x, y=y)
        time1_label_input = Entry(self.window, width=30).place(x=x + label_width + padding, y=y)

        new_y = y + label_height + padding
        time2_label = Label(self.window, text="Modules off time: ").place(x=x, y=new_y)
        time2_label = Entry(self.window, width=30).place(x=x + label_width + padding, y=new_y)

        new_y = y + 2 * (label_height + padding)
        time3_label = Label(self.window, text="arduino off time: ").place(x=x, y=new_y)
        time3_label = Entry(self.window, width=30).place(x=x + label_width + padding, y=new_y)

        new_y = y + 3 * (label_height + padding)
        submit_button = Button(self.window, text="plot", command=self.plotting, ).place(x=x, y=new_y)

        self.window.mainloop()

    def plotting(self):
        self.allow_plotting = True
        self.window.withdraw()
        self.plot = Plot()
        self.plot.set_after_close(func=self.after_close_plot)
        for i in range(10):
            number = random.randint(0, 10)
            if not self.allow_plotting:
                return
            self.plot.update_plot(number)
            time.sleep(0.2)
        now = datetime.now()
        self.plot.save(
            settings.PLOT_BASE_ADDRESS + f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}")
        # self.plot.close()

    def after_close_plot(self, event):
        self.allow_plotting = False
        self.window.deiconify()
        # self.__init__()


if __name__ == '__main__':
    GUI()
