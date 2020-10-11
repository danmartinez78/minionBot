import os
import sys
import time
import functools
sys.path.append(os.path.join(os.path.dirname(__file__), './uArm-Python-SDK/'))
from uarm.wrapper import SwiftAPI

class uarm:
    def __init__(self):
        self.swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
        self.swift.waiting_ready()
        device_info = self.swift.get_device_info()
        print(device_info)
        firmware_version = device_info['firmware_version']
        if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
            self.swift.set_speed_factor(0.0005)
        self.test()

    def test(self):
        self.swift.set_mode(0)
        self.swift.reset(wait=True, speed=10000)
        self.swift.set_position(x=200, speed=10000)
        self.swift.set_position(y=100)
        self.swift.set_position(z=100)
        self.swift.flush_cmd(wait_stop=True)

        self.swift.set_polar(stretch=200, speed=10000)
        self.swift.set_polar(rotation=90)
        self.swift.set_polar(height=150)
        print(self.swift.set_polar(stretch=200, rotation=90, height=150, wait=True))

        self.swift.flush_cmd()

        time.sleep(60)
        self.swift.disconnect()       
    
    def home(self):
        NotImplemented

    def move_to_pos(self, x, y, z, speed):
        pass

myarm = uarm()