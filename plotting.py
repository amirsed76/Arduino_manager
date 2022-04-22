import matplotlib.pyplot as plt
import time

class Plot:
    def __init__(self):
        self._init_line()

    def _init_line(self):
        plt.ion()
        self._figure = plt.figure(figsize=(7,7))
        self._ax = self._figure.add_subplot(111)
        self._line, = self._ax.plot([], [], 'b-')

    def _update_line(self, y, x=None):
        if x is None:
            x = len(self._line.get_xdata())

        xs, ys = list(self._line.get_xdata()) + [x], list(self._line.get_ydata()) + [y]
        self._line, = self._ax.plot(xs, ys, 'b-')

    def update_plot(self, y, x=None):
        self._update_line(y=y, x=x)
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()

    @staticmethod
    def save(file_path):
        plt.savefig(file_path)

    def set_after_close(self, func):
        self._figure.canvas.mpl_connect('close_event', func)

    def close(self):
        plt.close()
