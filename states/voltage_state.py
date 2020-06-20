## Code for reading voltage with Arduino
#!/usr/bin/env python3
import serial

counter = 0
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

while counter < 3:
    if ser.in_waiting > 0:
        voltage = ser.readline().decode('utf-8').rstrip()
        print(voltage)
        counter += 1
