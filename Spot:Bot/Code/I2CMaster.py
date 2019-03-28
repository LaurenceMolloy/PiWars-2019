from Adafruit_GPIO import I2C
from lsm303d import LSM303D
import VL53L1X

from math import atan, pi

import os
import time
import datetime
import json

class I2CMaster:

    # I2C Sensor Objects (Class Attributes)
    mux       = I2C.get_i2c_device(address=0x70)
    tof       = VL53L1X.VL53L1X(i2c_address=0x29)
    imu       = LSM303D(0x1d)

    # Class Data Files (input & output)
    i2c_config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config/i2c_config.json'))
    i2c_data_file   = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/data-i2c.json'))

    def __init__(self):
        self.load_config(self.__class__.i2c_config_file)


    def load_config(self,config):
        with open(config) as c:
            self.config = json.load(c)


    # Select an individual multiplexer channel
    def select_mux_channel(self, channel=0):    
        mux = self.__class__.mux
        if channel > 7:
            return
        mux.writeRaw8(1 << channel)


    # Read the distance (in mm) from a specified ToF sensor
    def read_distance(self, channel=0):        
        # Activate the specified ToF sensor i2c channel
        self.select_mux_channel(channel)

        tof = self.__class__.tof
    
        # Open ToF sensor to take reading
        tof.open()                          # Initialise the i2c bus and configure the sensor
        tof.start_ranging(1)                # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
        distance_in_mm = tof.get_distance() # Grab the range in mm
        tof.stop_ranging()                  # Stop ranging
        
        return str(distance_in_mm)


    # Read x, y, & z gauss magnetic values from specified 6DoF sensor and convert to compass bearing
    def read_bearing(self, channel=0):
        # Activate the specified IMU (6DoF) sensor i2c channel
        self.select_mux_channel(channel)

        imu = self.__class__.imu

        # Take magnetometer readings
        m = imu.magnetometer()

        # Convert magnetometer reaqdings to a compass bearing
        gaussvals = list(m)
        compass = 0
        if m[2] > 0:
            compass = 90 - atan(m[1]/m[2]) * 180/pi
        elif m[2] <  0:
            compass = 270 - atan(m[1]/m[2]) * 180/pi
        elif m[2] ==  0 and m[1] < 0:
            compass   = 90
        elif m[2] ==  0 and m[1] > 0:
            compass = 0

        return (m[1] * 180 / pi)


    # Dummy NULL function 
    def null():
        pass

    # Test all sensors in scan loop
    def test_scan_loop(self):
        values = []
        for x in self.config['scan_loop']:
            mux_channel = self.config['sensors'][str(x)]['mux']
            #print ("Opening MUX Channel " + str(mux_channel))
            readfn = self.config['sensors'][str(x)]['readfn']
            if readfn is not None:
                label = str(self.config['sensors'][str(x)]['name'])
                ts_before = time.time()
                value = str(eval(readfn)(mux_channel))
                ts_after = time.time()

                # estimate reading time at the sensor (average of before & after)
                ts_mean = (ts_before/2) + (ts_after/2)

                # convert epoch to utc time
                ts_utc = str(datetime.datetime(1970,1,1) + datetime.timedelta(seconds=ts_after))

                print(label + ": {}".format(value))
                dict_object = dict(name=label, value=value, time=ts_utc)
                values.append(dict_object)
            sensor_sleep = self.config['timing']['sensor_sleep']
            time.sleep(sensor_sleep)

        self.write_to_file(values, self.__class__.i2c_data_file)


            
    def write_to_file(self, dict_object, file_path):
        try:
            # Get a file object with write permission.
            file_object = open(file_path, 'w')

            # Save dict data into the JSON file.
            json.dump(dict_object, file_object)

            print(file_path + " created. ")    
        except FileNotFoundError:
            print(file_path + " not found. ")    

