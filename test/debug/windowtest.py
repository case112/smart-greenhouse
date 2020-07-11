import RPi.GPIO as gpio
import time
import datetime

temp1 = 0
temp2 = 0
hum1 = 0
hum2 = 0
temp_avg = 27
hum_avg = 0


print(temp_avg)



#Functions for window movement
def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(6, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(19, gpio.OUT)
    gpio.setup(5, gpio.OUT)
    gpio.setup(21, gpio.OUT, initial = gpio.HIGH) ## relay for motor controller


def closeWin(tf):
    closeLock()
    init()

    #closing pins
    gpio.output(21, False) ## relay for motor controller
    gpio.output(19, False)
    gpio.output(13, True)
    time.sleep(tf)
    gpio.cleanup()

def openWin(tf):
    openLock()
    init()
    
    #opening pins
    gpio.output(21, False) ## relay for motor controller
    gpio.output(19, True)
    gpio.output(13, False)
    time.sleep(tf)
    
    gpio.cleanup()

def openLock():
    init()

    #rises totally closed position GH window
    gpio.output(21, False) ## relay for motor controller
    gpio.output(19, True)
    gpio.output(13, False)
    gpio.output(5, False)
    time.sleep(2)
    
    gpio.cleanup()
    print("open clip opened")
    time.sleep(2)

def closeLock():
    init()

    #rises totally open position GH window
    gpio.output(21, False) ## relay for motor controller
    gpio.output(19, False)
    gpio.output(13, True)
    gpio.output(6, False)
    time.sleep(2)

    gpio.cleanup()
    print("close clip opened")
    time.sleep(2)

try:
    if temp_avg > 26:
        print("Open window")
        openWin(3)
    else:
        print("Close window")
        closeWin(3)
    
except KeyboardInterrupt:
    print("Keyboard interrupt")

except:
    print("Other error occurred!")

finally:
    gpio.cleanup()
