import os
import sys
import time
import functools
sys.path.append(os.path.join(os.path.dirname(__file__), './uArm-Python-SDK/'))
from uarm.wrapper import SwiftAPI

class MinionArm:
    def __init__(self):
        self.swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
        self.swift.waiting_ready()
        device_info = self.swift.get_device_info()
        print(device_info)
        firmware_version = device_info['firmware_version']
        if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
             self.swift.set_speed_factor(0.0005)
        self.speed = 110000
        self.test()
        self.board = "right"

    def test(self):
        # self.swift.set_buzzer(frequency=1000, duration=0.5, wait=True)
        self.swift.reset(wait=True, speed=self.speed)
        self.move(1250, 0, 150, self.speed)
        print(self.swift.get_position())
        # self.swift.set_buzzer(frequency=1000, duration=0.5, wait=True)

    def home(self):
        print("going home")
        self.swift.set_position(x = 150 , y = 0, speed = self.speed * 0.5, wait=True)
        self.move(145, 0, 100, self.speed*1.5)
        time.sleep(2)
        # self.swift.set_buzzer(frequency=1000, duration=0.5, wait=True)

    def rest(self):
        print("going to rest position")
        self.swift.set_position(x = 150 , speed = self.speed * 0.5, wait=True)
        self.swift.set_position(x = 125 , y = 0, speed = self.speed * 0.5, wait=True)
        self.move(125, 0, 40, self.speed * 0.5)
        time.sleep(2)
        self.swift.set_buzzer(frequency=1000, duration=0.5)


    def move(self, x, y, z, speed):
        self.swift.set_position(x, y, z, speed, wait=True)

    def flip(self):
        print("flipping")
        # self.home()
        self.swift.set_buzzer(frequency=1000, duration=0.5, wait=True)
        if self.board == "right":
            self.flip_left()
            self.board = "left"
        else:
            self.flip_right()
            self.board = "right"
        self.home()
        self.swift.set_buzzer(frequency=500, duration=1.0, wait=True)

    def flip_left(self):
        self.move(180, 0, 150, self.speed)
        self.move(240, 0, 150, self.speed)
        # self.move(220, 10, 140, self.speed*.2)
        self.move(220, 40, 150, self.speed*.2)
        # self.move(220, 40, 110, self.speed*.2)
        # self.move(220, 60, 100, self.speed*.2)
        self.move(220, 50, 30, self.speed*.2)
        time.sleep(1)
        self.move(180, 50, 20, self.speed*.2)
        time.sleep(2)

    def flip_right(self):
        self.move(180, 0, 150, self.speed)
        self.move(240, -10, 150, self.speed)
        # self.move(220, -20, 140, self.speed*.2)
        self.move(220, -40, 150, self.speed*.2)
        # self.move(220, -50, 110, self.speed*.2)
        # self.move(220, -60, 100, self.speed*.2)
        self.move(220, -60, 20, self.speed*.2)
        self.move(180, -50, 20, self.speed*.2)
        time.sleep(2)

    def move_to_galton_cal_pos(self):
        self.move(180, 0, 150, self.speed)
        self.move(240, 0, 150, self.speed)
        wait = input("waiting")
        self.home()

    def disconnect(self):
        self.swift.disconnect()  