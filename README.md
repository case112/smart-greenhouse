# Smart Greenhouse | [Smart Greenhouse Web App](https://github.com/case112/smart-greenhouse-web "GitHub Link") 

![Smart Greenhouse](https://ann-static.s3.amazonaws.com/media/uploads/2020/04/12/greenhouse.jpg)

## About

**Greenhouse automation with Raspberry Pi**

This is a write up of an automated greenhouse that regulates the inside temperature by automatically opening 2 windows on either side of the building. Addition to that it waters the plants as required. 

Raspberry Pi collects the data from the sensors, logs them to Postrges database that is being served with a [Django](https://github.com/case112/smart-greenhouse-web "GitHub Link")  application.

In addiditon to logging the Raspberry makes decisions according to the temperature measured inside the greenhouse. It opens the greenhouse windows when it gets too hot and closes them when it cools down. It also measures the soil moisture in order to know when to activate the water pump to water the plants.

### Main hardware components
- 1 - Raspberry Pi 2 Model B
- 1 - Arduino Nano
- 4 - DHT22 temperature and humidity sensors
- 1 - DS18B20 temperature sensor
- 2 - Chirp soil moisture sensors
- 2 - 5v to 3.3v logic converters
- 2 - 12V to 5V voltage regulators
- 1 - 4x 12V realy module
- 1 - Double BTS7960B DC 43A motor driver
- 6 - Stop swiches to get info about window movement/state and to stop over-extension
- 2 - DC motors for window movement
- 1 - DC water pump
- 1 - 12V battery
- 1 - 12V battery charger

### Software

The software consists of 4 main components.
- sensors - sensing and uploading the measurements
- states - measuring and uploading different values/states
- actions - makes decisions based on measured data (under works)
- logging errors and exceptions (under works)


# Installation

## Setting up Raspberry PI
- install latest version of Raspbian Lite/Desktop
- enable VNC or SSH for remote access
- enable I2C
- enable SPI
- make sure that you are using pip3, python3
- pip3 install RPI.GPIO
- pip3 install adafruit-blinka
- pip3 install python-decouple

## Setting up DHT22 temperature and humidity sensor
- pip3 install adafruit-circuitpython-dht
- sudo apt-get install libgpiod2

## Setting up DS18B20 temperature sensor
- enable 1-Wire

## Setting up Chirp soil sensor
- Download Chirp sensor class chirp.py from: https://github.com/ageir/chirp-rpi
- find out device address: i2cdetect -y 1

## Setting up Postgres client and Heroku CLI for DB connection (If using Heroku)
- sudo apt-get install libpq-dev
- pip install psycopg2-binary
- wget https://cli-assets.heroku.com/branches/stable/heroku-linux-arm.tar.gz
- mkdir -p /usr/local/lib /usr/local/bin
- sudo tar -xvzf heroku-linux-arm.tar.gz -C /usr/local/lib
- sudo ln -s /usr/local/lib/heroku/bin/heroku /usr/local/bin/heroku
- heroku update

## External inks to instructions:
- [DHT22](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi "Link")
- [DS18B20](https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/ "Link")
- [Chirp](https://github.com/ageir/chirp-rpi "Link")
- [Heroku Postgres Setup](https://github.com/EverWinter23/postgres-heroku "Link")

## Issues with 'lost address' on Chirp soil sensor
- One common issue is when sensors are hot plugged into the running bus -
the set-address command is not protected with any kind of
checksum and a stray communication on the bus might get interpreted as a
set-address command. If this is the case, bus scan would show the sensor
on another address but Raspberry Pi is not able to 'see' that new address.
- [Arduino sketch to set address on Chirp](https://gist.github.com/Miceuz/3f40a1614c749e04796a "Link")

## Todos:
- Log system, everyting to csv and then upload to db?
- actions
