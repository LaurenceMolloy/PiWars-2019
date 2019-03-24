
from Adafruit_GPIO import I2C
import VL53L1X
from lsm303d import LSM303D

import json
from pprint import pprint
from math import atan, pi

import os
import time


from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

with open('i2c_config.json') as f:
    data = json.load(f)

pprint(data)

def tca_select(channel):
    """Select an individual channel."""
    if channel > 7:
        return
    tca.writeRaw8(1 << channel)

def distance(channel):
    """ Read the distance from the ToF.
    """
        
    #Activate sensor i2c channel
    tca_select(channel)
    
    #Open sensor to take reading
    tof.open() # Initialise the i2c bus and configure the sensor
    tof.start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
    distance_in_mm = tof.get_distance() # Grab the range in mm
    tof.stop_ranging() # Stop ranging

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

tca = I2C.get_i2c_device(address=0x70)
tof = VL53L1X.VL53L1X(i2c_address=0x29)
lsm = LSM303D(0x1d)

print ("hello")

test()
