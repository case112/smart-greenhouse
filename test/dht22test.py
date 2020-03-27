import time
import board
import adafruit_dht
 
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
 
    time.sleep(5.0)

print(
    "Average Temp: {:.1f} C    Average Humidity: {}% ".format(
        avg_temp/counter, avg_hum/counter
    )
)



