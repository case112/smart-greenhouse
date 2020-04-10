import time
import board
import adafruit_dht
from sense_temphum import sense_temphum

def get_data(device, location):

    token = False

    # Try to take measurement multiple times in case of RuntimeError
    while not token:
        try:
            data = sense_temphum(device, location)
            token = True
            print('Token True')
            
        except RuntimeError as error:
            print(error.args[0])

        time.sleep(2.0)

    return data