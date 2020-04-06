import time
import board
import adafruit_dht
from csv_writer import write_to_file

#Greenhouse sensor1
write_to_file('greenhouse1.csv', adafruit_dht.DHT22(board.D17), 'Greenhouse1')

#Greenhouse sensor2
write_to_file('greenhouse2.csv', adafruit_dht.DHT22(board.D22), 'Greenhouse2')

#Greenhouse cabinet sensor
write_to_file('cabinet.csv', adafruit_dht.DHT22(board.D27), 'Cabinet')

#Outside sensor
write_to_file('outside.csv', adafruit_dht.DHT22(board.D18), 'Outside')