import RPi.GPIO as gpio
import time
import sys
from datetime import datetime
from upload import upload

#Window 1 = gpio(16)
#Window 2 = gpio(24)


def window_state(state_name, window_gpio):

    counter = 0
    value = 0
    data_list = []

    while counter < 5:
        gpio.setmode(gpio.BCM)
        gpio.setup(window_gpio, gpio.IN, gpio.PUD_UP)
        gpio.setup(window_gpio, gpio.IN, gpio.PUD_UP)

        if gpio.input(window_gpio) == 1:
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

    data_list.append(state_name)
    data_list.append(position)
    data_list.append(None) #Value
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    print(data_list)

    upload(data_list)

state_name = int(sys.argv[1])

if state_name == 8:
    window_gpio = 16
if state_name == 9:
    window_gpio = 24

window_state(state_name, window_gpio)