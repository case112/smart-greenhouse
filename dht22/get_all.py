import board
import adafruit_dht
from dht22_measure import get_dht22_data

#Greenhouse sensor1
get_dht22_data(adafruit_dht.DHT22(board.D17), 'Greenhouse1')

#Greenhouse sensor2
get_dht22_data(adafruit_dht.DHT22(board.D22), 'Greenhouse2')

#Greenhouse cabinet sensor
get_dht22_data(adafruit_dht.DHT22(board.D27), 'Cabinet')

#Outside sensor
get_dht22_data(adafruit_dht.DHT22(board.D18), 'Outside')