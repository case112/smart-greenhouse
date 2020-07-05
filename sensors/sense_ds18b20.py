## Sensor path might differ
## temp_sensor = '/sys/bus/w1/devices/28-03168b33a0ff/w1_slave'

## RUN
# water-1 = 6
# python3 sense_ds18b20.py sensor_name

import os
import time
from datetime import datetime
from upload import upload
import sys



def sense_ds18b20(sensor_name):
    data_list = []
    temperature = 0

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    temp_sensor = '/sys/bus/w1/devices/28-03168b33a0ff/w1_slave'

    t = open(temp_sensor, 'r')
    lines = t.readlines()
    t.close()
 
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string)/1000.0
        temperature = temp_c

    data_list.append(sensor_name)
    data_list.append(round(temperature, 1))
    data_list.append(None) # Humidity
    data_list.append(None) # Moisture
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(2)

    print(data_list)
    upload(data_list)

sensor_name = sys.argv[1]
sense_ds18b20(sensor_name)