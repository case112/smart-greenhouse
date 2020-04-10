import board
import adafruit_dht

from get_data import get_data
from upload import upload

#Greenhouse sensor1
data = get_data(adafruit_dht.DHT22(board.D17), 'Greenhouse1')
upload(data)

#Greenhouse sensor2
data = get_data(adafruit_dht.DHT22(board.D22), 'Greenhouse2')
upload(data)