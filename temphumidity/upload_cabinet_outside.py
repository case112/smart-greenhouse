import board
import adafruit_dht
import time

from get_data import get_data
from upload import upload

time.sleep(20)

#Greenhouse cabinet sensor
data = get_data(adafruit_dht.DHT22(board.D27), 'Cabinet')
upload(data)

#Outside sensor
data = get_data(adafruit_dht.DHT22(board.D18), 'Outside')
upload(data)