## Code for reading voltage with Arduino
#!/usr/bin/env python3
import serial
import time
from datetime import datetime
from upload import upload
import sys

# RUN
#state_name = 10
# python3 voltage_state.py 10


counter = 0
data_list = []
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

def voltage_state(state_name):

    while counter < 3:
        if ser.in_waiting > 0:
            voltage = ser.readline().decode('utf-8').rstrip()
            print(voltage)
            counter += 1
            time.sleep(2.0)

    data_list.append(state_name)
    data_list.append(None) #State
    data_list.append(voltage)
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    print(data_list)

    upload(data_list)
    
state_name = sys.argv[1]

voltage_state(state_name)