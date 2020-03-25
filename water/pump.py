## Turns on the relay for the pump
##Chirp library from https://github.com/ageir/chirp-rpi must be included 

import RPi.GPIO as gpio
import datetime
import chirp
import time
import sys
import os
import MySQLdb
import json
import httplib
import socket

gpio.setmode(gpio.BCM)
gpio.setup(20, gpio.OUT, initial = gpio.HIGH)
time.sleep(2)


sensor20= "20"
sensor21= "21"

# These values needs to be calibrated for the percentage to work!
#For sensor 20
min_moist20 = 245
max_moist20 = 655

#For sensor 21
min_moist21 = 260
max_moist21 = 579

# Initialize the sensor
chirp20 = chirp.Chirp(address=0x20,
                    read_moist=True,
                    read_temp=True,
                    read_light=False,
                    min_moist=min_moist20,
                    max_moist=max_moist20,
                    temp_scale='celsius',
                    temp_offset=0)

# Initialize the sensor
chirp21 = chirp.Chirp(address=0x21,
                    read_moist=True,
                    read_temp=True,
                    read_light=True,
                    min_moist=min_moist21,
                    max_moist=max_moist21,
                    temp_scale='celsius',
                    temp_offset=0)

try:
    # Trigger the sensors and take measurements.
    chirp20.trigger()
    chirp21.trigger()

    moist20=chirp20.moist
    perc20=chirp20.moist_percent

    moist21=chirp21.moist
    perc21=chirp21.moist_percent


    time.sleep(5)
    # Trigger the sensors and take measurements.
    chirp20.trigger()
    chirp21.trigger()

    moist20=chirp20.moist
    perc20=chirp20.moist_percent

    moist21=chirp21.moist
    perc21=chirp21.moist_percent

    avg_moist= (perc20+perc21) / 2



try:
    if avg_moist < 29:     
    	print 'relay on'
    	gpio.output(20, False)
    	time.sleep(300)
    	print 'relay off'
    	gpio.output(20, True)
    else:
    	print 'No need to water'

except KeyboardInterrupt:
    print "CTRL+C pressed"

except:
    print "Other error occurred!"

finally:
    gpio.cleanup()
