from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

class DisplayController:

    # Class Attribute
    i2cport = "1"
    i2caddr = "0x3C"
    
    # Initializer / Instance Attributes
    def __init__(self, rotate, height, width):
        self.rotate = rotate
        self.height = height
        self.width = width
        
    def configure(self):
        self.oled = sh1106(i2c(port=self.__class__.i2cport, address=self.__class__.i2caddr),
                           rotate=self.rotate,
                           height=self.height,
                           width=self.width)
    