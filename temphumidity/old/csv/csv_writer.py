import csv
import time
import board
import adafruit_dht
from dht22_measure import get_dht22_data

def write_to_file(file_name, dht22_device, location):

    with open(file_name, 'a+', newline='') as csvfile:
        datawriter = csv.writer(csvfile)

        token = False
        while not token:
            try:
                data = get_dht22_data(dht22_device, location)
                datawriter.writerow(data)
                token = True
        
            except RuntimeError as error:
                print(error.args[0])

            time.sleep(2.0)
