import sys
sys.path.append('/home/pi/Desktop/GIT/PiWars-2019/Spot:Bot/Code/')

import signal
import I2CMaster

def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

i2c = I2CMaster.I2CMaster()

while True:
    i2c.test_scan_loop()
