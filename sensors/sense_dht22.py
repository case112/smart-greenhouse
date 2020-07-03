### DHT22 SENSORS ###

##Greenhouse sensor1 - sensor_name = x
#adafruit_dht.DHT22(board.D17) 
##Greenhouse sensor2 - sensor_name = x
#adafruit_dht.DHT22(board.D22)
##Greenhouse cabinet sensor - sensor_name = x
#adafruit_dht.DHT22(board.D27)
##Outside sensor - sensor_name = x
#adafruit_dht.DHT22(board.D18)

import time
import board
import adafruit_dht
from datetime import datetime
from upload import upload
 

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


