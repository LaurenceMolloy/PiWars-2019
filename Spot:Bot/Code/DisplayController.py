import os
import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

class DisplayController:

    # Class Attributes
    i2cbus    = 1
    i2caddr   = '0x3C'
    height    = 128
    width     = 128
    imagepath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images'))

    def __init__(self, rotate=2):
        self.rotate = rotate
        self.configure()
        
    def configure(self):
        self.oled = sh1106(i2c(port    = self.__class__.i2cbus,
                               address = self.__class__.i2caddr),
                           rotate      = self.rotate,
                           height      = self.__class__.height,
                           width       = self.__class__.width)        

    def draw_screen(self,mode):
        image_path = os.path.abspath(os.path.join(self.__class__.imagepath, 'mode-' + str(mode) + '.png'))
        image = Image.open(image_path).convert(self.oled.mode)
        draw = ImageDraw.ImageDraw(image)
        self.oled.display(image)


