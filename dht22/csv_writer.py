import csv
import time
import board
import adafruit_dht
from dht22_measure import get_dht22_data

def write_to_file(file_name, dht22_device):

    with open(file_name, 'a+', newline='') as csvfile:
        datawriter = csv.writer(csvfile)
        data = get_dht22_data(dht22_device)         
        datawriter.writerow(data)
    

