import time
import board
import adafruit_dht
from csv_writer import write_to_file

write_to_file('cabinet.csv', adafruit_dht.DHT22(board.D27))