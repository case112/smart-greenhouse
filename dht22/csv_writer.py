import csv
import time
from dht22.dht22_measure import get_dht22_data
with open('temphumdata.csv', 'a+', newline='') as csvfile:
    datawriter = csv.writer(csvfile)
    data = get_dht22_data(device='board.D27')         
    datawriter.writerow(data)
    
