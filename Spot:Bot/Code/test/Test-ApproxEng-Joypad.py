from time import sleep
from approxeng.input.selectbinder import ControllerResource

import DisplayController

def readJoystick(joystick):
    battery = joystick.battery_level
    if (battery is not None):
        return battery
    else:
        return 0

oled = DisplayController.DisplayController(2,128,128)
oled.configure()

while True:
    try:
        with ControllerResource() as joystick:
            print('Found a joystick and connected')
            while joystick.connected:
                print ("Battery Level = " + str(readJoystick(joystick)))
                # Do stuff with your joystick here!
                # ....
                # ....
                sleep(0.1)
        # Joystick disconnected...
        print('Connection to joystick lost')
    except IOError:
        # No joystick found, wait for a bit before trying again
        print('Unable to find any joysticks')
        sleep(1.0)