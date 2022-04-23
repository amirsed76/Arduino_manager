from datetime import datetime

import matplotlib.pyplot as plt


class Plot:
    colors = ['blue', 'orange', 'purple', 'green', 'red', "brown", "pink", "gray", "olive", "cyan"]

    def __init__(self):
        plt.ion()
        self._figure = plt.figure(figsize=(7, 7))
        self._ax = self._figure.add_subplot(111)
        self._lines = dict()

    def update_line(self, line_name, y, x=None):
        if line_name not in self._lines.keys():
            x = 0 if x is None else x
            color = self.colors[len(self._lines.keys()) % len(self.colors)]
            self._lines[line_name], = self._ax.plot([x], [y], 'o-', label=line_name, color=color)
            plt.legend(loc="upper right")



        else:
            line = self._lines[line_name]
            x = len(line.get_xdata()) if x is None else x

            xs, ys = list(line.get_xdata()) + [x], list(line.get_ydata()) + [y]
            color = self.colors[list(self._lines.keys()).index(line_name) % len(self.colors)]
            self._lines[line_name], = self._ax.plot(xs, ys, 'o-', label=line_name, color=color)

    def update_plot(self):
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()

    @staticmethod
    def save(file_path):
        plt.savefig(file_path)

    def set_after_close(self, func):
        self._figure.canvas.mpl_connect('close_event', func)

    def close(self):
        plt.close(self._figure)

    @staticmethod
    def update_title(axes):
        axes.set_title(datetime.now())
        axes.figure.canvas.draw()

    def timer(self):
        timer = self._figure.canvas.new_timer(interval=100)
        timer.add_callback(self.update_title, self._ax)
        timer.start()
        plt.show()
