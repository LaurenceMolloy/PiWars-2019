
# Tell code about location of I2CSlave class file  
import sys
sys.path.append('/home/pi/Desktop/GIT/PiWars-2019/Spot:Bot/Code/')

import time         # for pauses in test code (time.sleep())
import signal       # for clean quitting with CTRL-C
import I2CSlave     # class for reading JSON data files written by I2C Master

# create the sensor data reading object
i2c = I2CSlave.I2CSlave()

# define the fixed/known order of turns for the maze
# 0 = LEFT, 1 = RIGHT
route = [0,0,1,1,0,0,0,1]

# threshold valuse for sensing wall opening in maze
# I recommend this is set to 1 maze width (60cm / 600mm)
distance_threshold = 600

# Register CTRL-C interrupt signal
def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# checks for distance > threshold value
# direction = 0 => check on left side
# direction = 1 => check on right side
# return values: 0 = no opening, 1 = opening detected
def test_for_opening(direction):
    d = direction
    sensor = 'unknown'
    i2c.read_json_data_file()
    if (direction == 0):
        sensor = 'distance-left'
    elif (direction == 1):
        sensor = 'distance-right'        
    else:
        return 0

    distance = i2c.get_sensor_data(sensor)

    if (int(distance['value']) > 10):
        opening = 1
    else:
        opening = 0

    print ("distance test: {0}\t{1}\t{2}\t{3}".format(sensor, d, distance['value'], opening))
    return opening


# roll forward a small amount (before testing for opening)
# empty for now - testing sensor logic in static mode
# hack this code later
def roll_forward():
    print ("FORWARD")
    pass;


# turn robot 90 degrees in a given direction
# just writes debug messages for now (for algorithm logic testing purposes)
def turn(direction):
    if (direction == 0):
        print ("turning LEFT")
    elif (direction == 1):
        print ("turning RIGHT")
    else:
        print ("HUH?!")

    # pause for testing purposes - simulates a slow turning process
    # allows us to replace obstacle before re-commencing distance tests
    time.sleep(5)


# our MAIN loop
while len(route):
    next_turn = route.pop(0)
    print (next_turn)
    print (route)
    while not test_for_opening(next_turn):
        roll_forward()
    turn(next_turn)
               
