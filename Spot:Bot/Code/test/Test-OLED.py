import time
from Adafruit_GPIO import I2C
import DisplayController
import json

config_file = "i2c_config.json"

def tca_select(channel):
    """Select an individual channel."""
    if channel > 7:
        return
    tca.writeRaw8(1 << channel)

def connect_oled():
    with open('i2c_config.json') as f:
        data = json.load(f)
    for x in data['sensors'].keys():
        s_type = data['sensors'][str(x)]['type']
        s_mux  = data['sensors'][str(x)]['mux']
        print ("TYPE: " + str(s_type) + " MUX: " + str(s_mux))
        if s_type == "oled" and s_mux is not None:
            print ("Opening MUX Channel " + str(s_mux))
            tca_select(s_mux)

#tca = I2C.get_i2c_device(address=0x70)
#connect_oled()

oled = DisplayController.DisplayContrtoller(rotate=3)
oled.configure()

while True:
    i = 1
    while i < 5:
        oled.draw_screen(i)
        i += 1
        time.sleep (2)
