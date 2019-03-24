from Adafruit_GPIO import I2C
from lsm303d import LSM303D
import VL53L1X

from pprint import pprint
from math import atan, pi

import os
import time
import json

#pprint(data)

class I2CMaster:

    # I2C Sensor Objects (Class Attributes)
    mux       = I2C.get_i2c_device(address=0x70)
    tof       = VL53L1X.VL53L1X(i2c_address=0x29)
    imu       = LSM303D(0x1d)

    # Class Data Files (input & output)
    i2c_config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config/i2c_config.json'))
    i2c_data_file   = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/data-i2c.json'))

    def __init__(self):
        self.load_config()

    def load_config(self,config=self.__class__.i2c_config_file):
        with open(config) as f:
            self.config = json.load(f)


    # Select an individual multiplexer channel
    def select_mux_channel(self, mux=self.__class__.mux, channel=0):    
        if channel > 7:
            return
        mux.writeRaw8(1 << channel)

    # Read the distance (in mm) from a specified ToF sensor
    def read_distance(self, tof=self.__class__.tof, mux=self.__class__.mux, channel=0):        
        #Activate the specified ToF sensor i2c channel
        select_mux_channel(mux, channel)
    
        #Open ToF sensor to take reading
        tof.open()                          # Initialise the i2c bus and configure the sensor
        tof.start_ranging(1)                # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
        distance_in_mm = tof.get_distance() # Grab the range in mm
        tof.stop_ranging()                  # Stop ranging

    return str(distance_in_mm)

def bearing(channel):
    """ Read the x, y & z values from the 6DoF.
    """

    #Activate sensor i2c channel
    tca_select(channel)
    
    #take readings
    t = lsm.temperature()
    m = lsm.magnetometer()
    a = lsm.accelerometer()


#Direction (y>0) = 90 - [arcTAN(x/y)]*180/¹
#Direction (y<0) = 270 - [arcTAN(x/y)]*180/¹
#Direction (y=0, x<0) = 180.0
#Direction (y=0, x>0) = 0.0

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

#    values = list(m) + list(a)

    print (m[1] * 180 / pi)
    return (("{:+06.2f} : {:+06.2f} : {:+06.2f}   ").format(*gaussvals))


    #x, y, z = lsm.accelerometer()
    #return str(x) + ", " + str(y) + ", " + str(z)

def null():
    pass

def test():
    """ Test sensors connected to multiplexer """
    for x in data['scan_loop']:
        mux_channel = data['sensors'][str(x)]['mux']
        print ("Opening MUX Channel " + str(mux_channel))
        readfn = data['sensors'][str(x)]['readfn']
        if readfn is not None:
            label = data['sensors'][str(x)]['name']
            print(label + ": {}".format(eval(readfn)(mux_channel)))


print ("hello")

test()
