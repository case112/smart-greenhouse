import RPi.GPIO as gpio
import time
from datetime import datetime


def state():

    counter = 0
    value = 0
    data_list = []
    sensor = 'S1-2'

    while counter < 5:
        gpio.setmode(gpio.BCM)
        gpio.setup(16, gpio.IN, gpio.PUD_UP)
        gpio.setup(24, gpio.IN, gpio.PUD_UP)

        if gpio.input(16) == 1 and gpio.input(24) == 1:
            print("window open")
        else:
            print("window closed")
            value += 1

        gpio.cleanup()
        counter += 1
        time.sleep(2.0)

    if value >= 4:
        position = False
    else:
        position = True

    data_list.append(sensor)
    data_list.append(position)
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    return data_list


