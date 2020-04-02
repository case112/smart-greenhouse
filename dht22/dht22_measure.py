import time
import board
import adafruit_dht
from datetime import datetime
 

def get_dht22_data(device, location):
    # Initialize the dht device, with data pin connected to:
    dhtDevice = device

    counter = 0
    avg_temp = 0
    avg_hum = 0
    data_list = []
    
    # Initial measurement could be false
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    time.sleep(2.0)

    # Try to take 5 measurements for better accuracy 
    while counter < 5:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity

            # Not counting false temperature spikes
            if temperature > 1 and temperature < 45 and humidity > 0 and humidity < 100:
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

    data_list.append(location)
    data_list.append(round(avg_temp/counter, 1))
    data_list.append(round(avg_hum/counter, 1))
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))

    print(
                "{}, Temp: {:.1f} C    Humidity: {:.1f}% ".format(
                    location,
                    avg_temp/counter,
                    avg_hum/counter
                )
            )
    
    return data_list


