import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random

if __name__ == '__main__':
    plt.ion()
    figure = plt.figure(figsize=(5,5))
    ax = figure.add_subplot(111)
    line, = ax.plot([0], [1], 'b-')
    plt.pause(10)
