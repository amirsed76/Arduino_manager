import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random


class Plot:
    def __init__(self, is_show=True):
        self.is_show = is_show
        self._line = None

        if self.is_show:
            self._init_window()

    def _init_window(self):
        self._figure = plt.fi
        axnext = self._figure.axes([0.87, 0.005, 0.1, 0.075])
        bnext = Button(self._figure, 'Next')
        bnext.on_clicked(self.next_func)
        plt.show()

    def _update_line(self, y, x=None):

        if self._line is None:
            ax = plt.axes([0.1, 0.1, 0.8, 0.8])

            x = 0 if x is None else x
            xs, ys = [x], [y]
            self._line, = ax.plot(xs, ys, 'b-')



        else:
            x = len(self._line.get_xdata()) if x is None else x
            xs, ys = list(self._line.get_xdata()) + [x], list(self._line.get_ydata()) + [y]
            self._line.set_data(xs, ys)
            print(self._line.get_ydata())

    def update_plot(self, y, x=None):
        self._update_line(y=y, x=x)
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()

    @staticmethod
    def save(file_path):
        plt.savefig(file_path)

    def next_func(self, event):
        i = random.randint(0, 10)
        self.update_plot(i)
        print("OOKKK")


if __name__ == '__main__':
    plot = Plot(True)
    plt.show()
