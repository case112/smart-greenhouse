import time
import board
import adafruit_dht
from dht22_measure import get_dht22_data

def get_data(device, location):

    token = False

    # Try to take measurement multiple times in case of RuntimeError
    while not token:
        try:
            get_dht22_data(device, location)
            token = True

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])

        time.sleep(2.0)
