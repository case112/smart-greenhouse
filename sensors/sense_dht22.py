### DHT22 SENSORS ###
##Greenhouse sensor1 - sensor_name = 1
#adafruit_dht.DHT22(board.D17)
##Greenhouse sensor2 - sensor_name = 2
#adafruit_dht.DHT22(board.D22)
##Greenhouse cabinet sensor - sensor_name = 5
#adafruit_dht.DHT22(board.D27)
##Outside sensor - sensor_name = 7
#adafruit_dht.DHT22(board.D18)

## RUN
# python3 sense_dht22.py sensor_name

import time
import board
import adafruit_dht
import logging
import sys
from datetime import datetime
from upload import upload

logging.basicConfig(
    filename='sensors.log',
    format='\n[%(asctime)s] %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


def sense_dht22(sensor_name, device):

    counter = 0
    avg_temp = 0
    avg_hum = 0
    data_list = []
    
    # Initial measurement could be false
    temperature = device.temperature
    humidity = device.humidity
    time.sleep(2.0)

    # Try to take 3 measurements for better accuracy 
    while counter < 3:
        try:
            temperature = device.temperature
            humidity = device.humidity

            # Not counting false temperature spikes
            if temperature > -8 and temperature < 45 and humidity > 0 and humidity < 100:
                avg_temp += temperature
                avg_hum += humidity
                counter += 1
            
            print(
                "Temp: {:.1f} C    Humidity: {}% ".format(
                    temperature, humidity
                )
            )
    
        except RuntimeError as error: 
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            logging.error('RuntimeError@sense_dht22:', exc_info=error)

    
        time.sleep(4.0)

    data_list.append(sensor_name)
    data_list.append(round(avg_temp/counter, 1))
    data_list.append(round(avg_hum/counter, 1))
    data_list.append(None) # Moisture = None
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))

    print(
        "{}, Temp: {:.1f} C    Humidity: {:.1f}%, {}".format(
            sensor_name,
            avg_temp/counter,
            avg_hum/counter,
            now
        )
    )

    upload(data_list)


def call_dht22(sensor_name, device):

    token = False

    # Try to take measurement multiple times in case of RuntimeError
    while not token:
        try:
            data = sense_dht22(sensor_name, device)
            token = True
            print('Token True')
            
        except RuntimeError as error:
            print(error.args[0])

        time.sleep(2.0)




sensor_name = int(sys.argv[1])

if sensor_name == 1:
    device = adafruit_dht.DHT22(board.D17)
elif sensor_name == 2:
    device = adafruit_dht.DHT22(board.D22)
elif sensor_name == 5:
    device = adafruit_dht.DHT22(board.D27)
elif sensor_name == 7:
    device = adafruit_dht.DHT22(board.D18)

call_dht22(sensor_name, device)

