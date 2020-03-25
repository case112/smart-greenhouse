###Class for the Chirp capacitive soil moisture sensor
###made by Catnip Electronics, Albertas Mickėnas

###References to used code for Chirp:
###https://github.com/Miceuz/i2c-moisture-sensor
###https://www.tindie.com/products/miceuz/i2c-soil-moisture-sensor/

###Python Class by Göran Lundberg. https://github.com/ageir/chirp

from __future__ import division
from datetime import datetime

import smbus
import sys
import time

class Chirp(object):
    def __init__(self, bus=1, address=0x20, min_moist=False, max_moist=False,
                 temp_scale='celsius', temp_offset=0, read_temp=True,
                 read_moist=True, read_light=True):
    
        self.bus_num = bus
        self.bus = smbus.SMBus(bus)
        self.busy_sleep = 0.01
        self.address = address
        self.min_moist = min_moist
        self.max_moist = max_moist
        self.temp_scale = temp_scale
        self.temp_offset = temp_offset
        self.read_temp = read_temp
        self.read_moist = read_moist
        self.read_light = read_light
        self.temp = False
        self.moist = False
        self.light = False
        self.temp_timestamp = datetime
        self.moist_timestamp = datetime
        self.light_timestamp = datetime

        # Register values
        self._GET_CAPACITANCE = 0x00  # (r) 2 bytes
        self._SET_ADDRESS = 0x01      # (w) 1
        self._GET_ADDRESS = 0x02      # (r) 1
        self._MEASURE_LIGHT = 0x03    # (w) 0
        self._GET_LIGHT = 0x04        # (r) 2
        self._GET_TEMPERATURE = 0x05  # (r) 2
        self._RESET = 0x06            # (w) 0
        self._GET_VERSION = 0x07      # (r) 1
        self._SLEEP = 0x08            # (w) 0
        self._GET_BUSY = 0x09         # (r) 1

    def trigger(self):

        if self.read_temp is True:
            self.temp = self._read_temp()
        if self.read_moist is True:
            self.moist = self._read_moist()
        if self.read_light is True:
            self.light = self._read_light()

    def get_reg(self, reg):

        val = self.bus.read_word_data(self.address, reg)
        # return swapped bytes (they come in wrong order)
        return (val >> 8) + ((val & 0xFF) << 8)

    @property
    def version(self):

        return self.bus.read_byte_data(self.address, self._GET_VERSION)

    @property
    def busy(self):
  
        busy = self.bus.read_byte_data(self.address, self._GET_BUSY)

        if busy == 1:
            return True
        else:
            return False

    def reset(self):
      
        self.bus.write_byte(self.address, self._RESET)

    def sleep(self):
      
        self.bus.write_byte(self.address, self._SLEEP)

    def wake_up(self, wake_time=1):

        self.wake_time = wake_time

        try:
            self.bus.read_byte_data(self.address, self._GET_VERSION)
        except OSError:
            pass
        finally:
            time.sleep(self.wake_time)

    @property
    def sensor_address(self):

        return self.bus.read_byte_data(self.address, self._GET_ADDRESS)

    @sensor_address.setter
    def sensor_address(self, new_addr):

        if isinstance(new_addr, int) and (new_addr >= 3 and new_addr <= 119):
            self.bus.write_byte_data(self.address, 1, new_addr)
            self.reset()
            self.address = new_addr
        else:
            raise ValueError('I2C address must be between 3-119 or 0x03-0x77.')

    @property
    def moist_percent(self):

        moisture = self.moist
        return self.moist_to_percent(moisture)

    def moist_to_percent(self, moisture):

        if (self.min_moist or self.max_moist) is False:
            raise ValueError('min_moist and max_moist must be defined.')
        else:
            return round((((moisture - self.min_moist) /
                           (self.max_moist - self.min_moist)) * 100), 1)

    def _read_moist(self):
   
        # This returns last reading, and triggers a new, discard old value
        measurement = self.get_reg(self._GET_CAPACITANCE)

        # Wait for sensor to finish measurement
        while self.busy:
            time.sleep(self.busy_sleep)
        self.moist_timestamp = datetime.now()

        # Retrieve the measurement just triggered
        measurement = self.get_reg(self._GET_CAPACITANCE)
        return measurement

    def _read_temp(self):

        # This returns last reading, and triggers a new, discard old value
        measurement = self.get_reg(self._GET_TEMPERATURE)

        # Wait for sensor to finish measurement
        while self.busy:
            time.sleep(self.busy_sleep)
        self.temp_timestamp = datetime.now()

        # Retrieve the measurement just triggered
        measurement = self.get_reg(self._GET_TEMPERATURE)

        # The chirp sensor returns an integer. But the return measurement is
        # actually a float with one decimal. Needs to be converted to float by
        # dividing by ten. And adjusted for temperature offset (if used).
        celcius = round(((measurement / 10) + self.temp_offset), 1)

        # Check which temperature scale to return the measurement in
        if self.temp_scale == 'celsius':
            return celcius
        elif self.temp_scale == 'farenheit':
            # °F = (°C × 9/5) + 32
            farenheit = (celcius * 9 / 5) + 32
            return farenheit
        elif self.temp_scale == 'kelvin':
            # K = °C + 273.15
            kelvin = celcius + 273.15
            return kelvin
        else:
            raise ValueError(
                '{} is not a valid temperature scale. Only celsius, farenheit \
                and kelvin are supported.'.format(self.temp_scale))

    def _read_light(self):
        
        # Trigger a measurement
        self.bus.write_byte(self.address, self._MEASURE_LIGHT)

        # Wait for sensor to finish measurement. Takes longer in low light.
        while self.busy:
            time.sleep(self.busy_sleep)
        self.light_timestamp = datetime.now()
        measurement = self.get_reg(self._GET_LIGHT)
        return measurement

    def __repr__(self):
        
        return '<Chirp sensor on bus {:d}, i2c addres {:d}>'.format(
            self.bus_num, self.address)


if __name__ == "__main__":
    # Python 2.6 required.
    if (sys.version_info < (2, 6)):
        python_version = ".".join(map(str, sys.version_info[:3]))
        print('Python version 2.6 or higher required, you are using \
            {}'.format(python_version))
        sys.exit()

    # Prints usage information.
    def print_usage():
        print('Usage:\n')
        print('{} <address> [[set] [new address]]\n'.format(sys.argv[0]))
        print('Examples:\n')
        print('Run continous measurements.')
        print('{} 0x20\n'.format(sys.argv[0]))
        print('Change the I2C address of the sensor on address 0x20 to 0x21')
        print('{} 0x20 set 0x21'.format(sys.argv[0]))
        print(len(sys.argv))
        sys.exit()

    # Check command line argument for I2C address. (In hex, ie 0x20)
    if (len(sys.argv) == 1) or (len(sys.argv) >= 5):
        print_usage()
    if len(sys.argv) >= 2:
        if sys.argv[1].startswith("0x"):
            addr = int(sys.argv[1], 16)
        else:
            print_usage()

    # Variables for calibrated max and min values. These need to be adjusted!
    # These are only needed if you plan to use moist_percent.
    # If these values are not adjusted for your sensor the value for
    # moist_percent might go below 0% and above 100%
    min_moist = 240
    max_moist = 750

    highest_measurement = False
    lowest_measurement = False

    # Initialize the sensor.
    chirp = Chirp(address=addr,
                  read_moist=True,
                  read_temp=True,
                  read_light=True,
                  min_moist=min_moist,
                  max_moist=max_moist,
                  temp_scale='celsius',
                  temp_offset=0)

    # Check command line arguments if user wants to change the I2C address.
    if len(sys.argv) >= 3:
        if sys.argv[2] == 'set':

            if sys.argv[3].startswith("0x"):
                new_addr = int(sys.argv[3], 16)
            else:
                new_addr = int(sys.argv[3])
            # Set new address, also resets the sensor.
            chirp.sensor_address = new_addr
            print('Chirp I2C address changed to {}'.format(hex(new_addr)))
            sys.exit()
        else:
            print_usage()

    # Check which temperature sign to use.
    if chirp.temp_scale == 'celsius':
        scale_sign = '°C'
    elif chirp.temp_scale == 'farenheit':
        scale_sign = '°F'
    elif chirp.temp_scale == 'kelvin':
        scale_sign = 'K'

    print('Chirp soil moisture sensor.\n')
    print('Firmware version:   {}'.format(hex(chirp.version)))
    print('I2C address:        {}\n'.format(chirp.sensor_address))
    print('Press Ctrl-C to exit.\n')
    print('Moisture  | Temp   | Brightness')
    print('-' * 31)

    try:
        # Endless loop, taking measurements.
        while True:
            # Trigger the sensors and take measurements.
            chirp.trigger()
            output = '{:d} {:4.1f}% | {:3.1f}{} | {:d}'
            output = output.format(chirp.moist, chirp.moist_percent,
                                   chirp.temp, scale_sign, chirp.light)
            print(output)
            # Adjust max and min measurement variables, used for calibrating
            # the sensor and allow using moisture percentage.
            if highest_measurement is not False:
                if chirp.moist > highest_measurement:
                    highest_measurement = chirp.moist
            else:
                highest_measurement = chirp.moist
            if lowest_measurement is not False:
                if chirp.moist < lowest_measurement:
                    lowest_measurement = chirp.moist
            else:
                lowest_measurement = chirp.moist
            time.sleep(10)
    except KeyboardInterrupt:
        print('\nCtrl-C Pressed! Exiting.\n')
    finally:
        print('Lowest moisture measured:  {}'.format(lowest_measurement))
        print('Highest moisture measured: {}'.format(highest_measurement))
        print('Bye!')
