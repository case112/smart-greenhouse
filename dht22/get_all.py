import board
import adafruit_dht
from get_data import get_data


#Greenhouse sensor1
get_data(adafruit_dht.DHT22(board.D17), 'Greenhouse1')

#Greenhouse sensor2
get_data(adafruit_dht.DHT22(board.D22), 'Greenhouse2')

#Greenhouse cabinet sensor
get_data(adafruit_dht.DHT22(board.D27), 'Cabinet')

#Outside sensor
get_data(adafruit_dht.DHT22(board.D18), 'Outside')