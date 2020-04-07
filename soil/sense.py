import chirp
import time
from datetime import datetime

def sense(sensor, min, max, address):

    # The highest and lowest calibrated values
    min_moist = min
    max_moist = max

    counter = 0
    avg_moist = 0
    avg_moist_percent = 0
    avg_temp = 0
    data_list = []

    # Initialize the sensor.
    chirp = chirp.Chirp(address,
                        read_moist=True,
                        read_temp=True,
                        read_light=False,
                        min_moist=min_moist,
                        max_moist=max_moist,
                        temp_scale='celsius',
                        temp_offset=0)

    # First measurement could be false
    try:
        chirp.trigger()
        print(
            "First pull: Moisture value: {}, Moisture: {}%  Temp: {}% ".format(
                chirp.moist_percent,
                chirp.moist,
                chirp.temp
            )
        )

    except RuntimeError as error:
            print(error.args[0])


    # Try to take 3 measurements for better accuracy 
    while counter < 3:
        try:
            chirp.trigger()

            # Not counting false data spikes
            if chirp.temp > -3 and chirp.temp < 47 and chirp.moist > min_moist and chirp.moist < max_moist:
                avg_moist += chirp.moist
                avg_moist_percent += chirp.moist_percent
                avg_temp += chirp.temp
                counter += 1
            
            print(
                "Moisture value: {}, Moisture: {}%  Temp: {}% ".format(
                    chirp.moist_percent,
                    chirp.moist,
                    chirp.temp
                )
            )
    
        except RuntimeError as error:
            print(error.args[0])
    
        time.sleep(4.0)

    data_list.append(sensor)
    data_list.append(round(avg_moist/counter, 1))
    data_list.append(round(avg_moist_percent/counter, 1))
    data_list.append(round(avg_temp/counter, 1))
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))

    print(data_list)
    
    return data_list