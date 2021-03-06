from datetime import datetime, timedelta

import matplotlib.pyplot as plt

index = 0


class Plot:
    def __init__(self):
        plt.ion()
        self._figure = plt.figure(figsize=(7, 7))
        self._ax = self._figure.add_subplot(111)
        self._lines = dict()
        self.start_time = datetime.now()
        self.timer_max_time = None

    def update_line(self, line_name, y, x=None):
        if line_name not in self._lines.keys():
            global index
            x = 0 if x is None else x
            self._lines[line_name], = self._ax.plot([x], [y], 'o-', label=line_name)
            plt.legend(loc="upper right", labels=list(self._lines.keys()))

        else:
            line = self._lines[line_name]
            x = len(line.get_xdata()) if x is None else x

            xs, ys = list(line.get_xdata()) + [x], list(line.get_ydata()) + [y]
            self._lines[line_name], = self._ax.plot(xs, ys, 'o-', label=line_name)

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

    def update_title(self, axes):
        _time = datetime.now() - self.start_time
        if _time.seconds <= self.timer_max_time:
            axes.set_title(str(timedelta(seconds=_time.seconds)))
        else:
            axes.set_title(str(timedelta(seconds=self.timer_max_time)))
        axes.figure.canvas.draw()

    def timer(self, max_time=None):
        self.timer_max_time = max_time
        this_timer = self._figure.canvas.new_timer(interval=100)
        this_timer.add_callback(self.update_title, self._ax)
        this_timer.start()
