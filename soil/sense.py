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
            if chirpsense.temp > -3 and chirpsense.temp < 47 and chirpsense.moist > min_moist and chirpsense.moist < max_moist:
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
    
        time.sleep(4.0)

    data_list.append(sensor)
    data_list.append(round(avg_moist/counter, 1))
    data_list.append(round(avg_moist_percent/counter, 1))
    data_list.append(round(avg_temp/counter, 1))
    now = datetime.now()
    data_list.append(now.strftime("%Y-%m-%d %H:%M:%S"))

    print(data_list)
    
    return data_list