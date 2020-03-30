import time
import board
import adafruit_dht
from datetime import datetime
 

def dht_data():

    # Initial the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT22(board.D27)

    counter = 0
    avg_temp = 0
    avg_hum = 0
    
    while counter < 10:
        try:
            # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            counter += 1
            avg_temp += temperature
            avg_hum += humidity
            
            print(
                "Temp: {:.1f} C    Humidity: {}% ".format(
                    temperature, humidity
                )
            )
    
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
    
        time.sleep(2.0)


    data_list = []
    data_list.append('Temphum cabinet')
    data_list.append(avg_temp/counter)
    data_list.append(avg_hum/counter)
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))
    return data_list



    #print(
    #    "Average Temp: {:.1f} C    Average Humidity: {}% ".format(
    #        avg_temp/counter, avg_hum/counter
    #    )
    #)



