import csv
import time
import board
import adafruit_dht
from get_data import get_data

def write_to_file(file_name, dht22_device, location):

    with open(file_name, 'a+', newline='') as csvfile:
        datawriter = csv.writer(csvfile)
        data = get_data(dht22_device, location)         
        datawriter.writerow(data)
    

