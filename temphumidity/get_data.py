import time
import board
import adafruit_dht
from dht22_measure import dht22_measure

def get_data(device, location):

    token = False

    # Try to take measurement multiple times in case of RuntimeError
    while not token:
        try:
            data = dht22_measure(device, location)
            token = True
            print('Token True')
            
        except RuntimeError as error:
            print(error.args[0])

        time.sleep(2.0)

    return data