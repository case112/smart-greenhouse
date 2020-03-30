import csv
import time
from get_dht_data import dht_data
with open('temphumdata.csv', 'a+', newline='') as csvfile:
    datawriter = csv.writer(csvfile)
    data = dht_data()          
    datawriter.writerow(data)
    
