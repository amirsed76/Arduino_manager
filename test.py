import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time


if __name__ == '__main__':
    with open("information.json","r") as f:
        while True:
            time.sleep(1)
            print("_______")
            print(f.read())  # read again
            f.seek(0)  # offset of 0
