from datetime import datetime

from random import uniform
from time import sleep


def nap(seconds):
    variation = 0.28
    variation *= uniform(1 - variation, 1 + (variation * (1 + variation)))
    if 0.9 > uniform(0, 1):
        seconds = seconds * uniform(1 - variation, 1 + variation)
    elif 0.8 > uniform(0, 1):
        seconds = seconds * uniform(2 * (1 - variation), 6 * (1 + variation))
    elif 0.7 > uniform(0, 1):
        seconds = seconds * uniform(6 * (1 - variation), 14 * (1 + variation))
    else:
        seconds = seconds * uniform(14 * (1 - variation), 60 * (1 + variation))
    sleep(seconds)
    return


def date_time_print(*output, sep=' ', end=''):
    if any(output):
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end=' | ')
        for i in output[:-1]:
            print(i, end=sep)
        if any(end):
            print(output[-1], end=end)
        else:
            print(output[-1])
    else:
        print()
