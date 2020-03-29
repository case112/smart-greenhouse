## Code for charging the greenhouse battery
#import RPi.GPIO as gpio
import time
import datetime

#gpio.setmode(gpio.BCM)

# Relay for activating the battery charger
#gpio.setup(12, gpio.OUT, initial = gpio.HIGH)
counter = 0
time.sleep(2)

try:
    #gpio.output(12, False)
    now = datetime.datetime.now()
    print('Battery charging', now.strftime("%Y-%m-%d %H:%M:%S"))
    ## Relay switches the charger on for time.sleep(seconds), if it gets done sooner the charger shuts itself off
    #gpio.output(12, True)
    time.sleep(10) #seconds
    now = datetime.datetime.now()
    print('Charger off', now.strftime("%Y-%m-%d %H:%M:%S"))

except KeyboardInterrupt:
    # exits when you press CTRL+C
    print("CTRL-C pressed")

except:
    print("Other error occurred!")

finally:
    #gpio.cleanup()
    print('som')