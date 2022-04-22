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

        # button that displays the plot
        plot_button = Button(master=self.window,
                             command=self.plotting,
                             height=2,
                             width=10,
                             text="Plot")
        plot_button.pack()

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
