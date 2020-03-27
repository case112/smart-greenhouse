## Code for charging the greenhouse battery
import RPi.GPIO as gpio
import time
import datetime

gpio.setmode(gpio.BCM)

# Relay for activating the battery charger
gpio.setup(12, gpio.OUT, initial = gpio.HIGH)
counter = 0
time.sleep(2)

try:
    print('Battery charging')
    gpio.output(12, False)
    ## Relay switches the charger on for time.sleep(seconds), if it gets done sooner the charger shuts itself off
    time.sleep(5000) #seconds
    print('Charger off')
    gpio.output(12, True)

except KeyboardInterrupt:
    # exits when you press CTRL+C
    print("CTRL-C pressed")

except:
    print("Other error occurred!")

finally:
    gpio.cleanup()

