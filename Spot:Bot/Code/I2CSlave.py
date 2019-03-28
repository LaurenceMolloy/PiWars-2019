import os
import time
import json

class I2CSlave:

    # Class Data Files (input & output)
    i2c_config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config/i2c_config.json'))
    data_file   = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/data-i2c.json'))

    def __init__(self):
        self.load_config()
        self.read_json_data_file()

    def load_config(self):
        with open(self.__class__.i2c_config_file) as c:
            self.config = json.load(c)

    # Read latest sensors data written to JSON file
    def read_json_data_file(self):
        with open(self.__class__.data_file) as c:
            self.data = json.load(c)
            time.sleep(self.config['timing']['loop_sleep'])

    # Test all sensors in scan loop
    def get_sensor_data(self,sensor_name):
        for sensor in self.data:
            if sensor['name'] == sensor_name:
                return sensor
        return None
