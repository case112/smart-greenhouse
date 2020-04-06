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
- pip3 install python-decouple
- pip3 install pytz

## DHT22 temperature and humidity sensor library
- pip3 install adafruit-circuitpython-dht
- sudo apt-get install libgpiod2

## DS18B20 temperature sensor
- 

## Install Postgres client and Heroku CLI for DB connection
- sudo apt-get install libpq-dev
- pip install psycopg2-binary
- wget https://cli-assets.heroku.com/branches/stable/heroku-linux-arm.tar.gz
- mkdir -p /usr/local/lib /usr/local/bin
- sudo tar -xvzf heroku-linux-arm.tar.gz -C /usr/local/lib
- sudo ln -s /usr/local/lib/heroku/bin/heroku /usr/local/bin/heroku
- heroku update
- DB conn instructions https://github.com/EverWinter23/postgres-heroku

- heroku pg:psql --app appname
- SET TIMEZONE='posix/Europe/Tallinn';
- SHOW TIMEZONE;
- heroku pg:killall





Cloning git repository
- git init
- git remote add origin https://github.com/case112/smart-greenhouse.git
- git pull origin master 

Install instructions
DHT22:
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi 

DS18B20:
https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/

Chirp soil sensor:
https://github.com/ageir/chirp-rpi