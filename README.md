# Smart Greenhouse

## Installation
- install latest version of Raspbian Lite/Desktop
- enable VNC or SSH for remote access
- enable I2C
- enable SPI
- enable 1-Wire
- make sure that you are using pip3, python3
- pip3 install RPI.GPIO
- pip3 install adafruit-blinka

## DHT22 temperature and humidity sensor library
- pip3 install adafruit-circuitpython-dht
- sudo apt-get install libgpiod2

## DS18B20 temperature sensor
- 

Cloning git repository
- git init
- git remote add origin https://github.com/case112/smart-greenhouse.git
- git pull origin master 

Install instructions
DHT22:
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi 

DS18B20:
https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
