import chirp
import logging
import time
from datetime import datetime
from upload import upload
import sys

logging.basicConfig(
    filename='sensors.log',
    format='\n[%(asctime)s] %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

def sense_chirp(sensor_name, min_moist, max_moist, address):

    # The highest and lowest calibrated values
    #min_moist = min
    #max_moist = max

    counter = 0
    avg_moist = 0
    avg_moist_percent = 0
    avg_temp = 0
    data_list = []

    # Initialize the sensor.
    chirpsense = chirp.Chirp(address=address,
                        read_moist=True,
                        read_temp=True,
                        read_light=True,
                        min_moist=min_moist,
                        max_moist=max_moist,
                        temp_scale='celsius',
                        temp_offset=0)

    # First measurement could be false
    try:
        chirpsense.trigger()
        print(
            "First pull: Moisture value: {}, Moisture: {}%  Temp: {}C ".format(
                chirpsense.moist,
                chirpsense.moist_percent,
                chirpsense.temp
            )
        )

    except RuntimeError as error:
            print(error.args[0])


    # Try to take 3 measurements for better accuracy 
    while counter < 3:
        try:
            chirpsense.trigger()

            # Not counting false data spikes
            if chirpsense.temp > -8 and chirpsense.temp < 47 and chirpsense.moist > min_moist and chirpsense.moist < max_moist:
                avg_moist += chirpsense.moist
                avg_moist_percent += chirpsense.moist_percent
                avg_temp += chirpsense.temp
                counter += 1
            else:
                counter += 0.3
            
            print(
                "Moisture value: {}, Moisture: {}%  Temp: {}C ".format(
                    chirpsense.moist,
                    chirpsense.moist_percent,
                    chirpsense.temp
                )
            )
    
        except RuntimeError as error:
            print(error.args[0])
            logging.error('RuntimeError@sense_chirp:', exc_info=error)
    
        time.sleep(4.0)

    data_list.append(sensor_name)
    data_list.append(round(avg_temp/counter, 1))
    #data_list.append(int(avg_moist/counter)) #Moisture value
    data_list.append(None) #Humidity
    data_list.append(round(avg_moist_percent/counter, 1))
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))

    print(data_list)

    upload(data_list)

sensor_name = int(sys.argv[1])

if sensor_name == 3:
    min_moist = 200
    max_moist = 840
    address = 0x45
else:
    #same values for now
    min_moist = 200
    max_moist = 840
    address = 0x24

sense_chirp(sensor_name, min_moist, max_moist, address)