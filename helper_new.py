
import numpy as np
import pyautogui as auto
import matplotlib.pyplot as plt
import seaborn as sns
from time import sleep
from random import randint
from Calcuater import Calculater

SIZEX, SIZEY = (480, 256)
XY1 = (1358, 100)
XY2 = (XY1[0] + SIZEX, XY1[1] + SIZEY)
COUNT = (30, 16)
RESET = (1594, 83)
MCOUNT = 99

X = 16#int((XY2[0] - XY1[0]) / COUNT[0]) + 1
Y = 16#int((XY2[1] - XY1[1]) / COUNT[1]) + 1

class Helper:
    count_m = 0

    def __init__(self):
        self.calc = Calculater(XY1, XY2, COUNT)
        auto.click(RESET)
        auto.click(RESET)
        self.clickL([randint(0, COUNT[1] - 1) , randint(0, COUNT[0] - 1)])
    
    def do(self, lst):
        self.home()

        right = []

        left = lst

        for loc in right:
            self.clickR(loc)

        for loc in left:
            self.clickL(loc)

    def clickR(self, loc):
        self.count_m += 1
        y, x = loc
        print(f"x : {x}, y : {y} - Right")
        self.home()
        auto.moveRel((x * X) + 3, (y * Y) + 3)
        auto.rightClick()
        
    def clickL(self, loc):
        y, x = loc
        print(f"x : {x}, y : {y} - Left")
        self.home()
        auto.moveRel((x * X) + 3, (y * Y) + 3)
        auto.click()

    def home(self):
        auto.moveTo(x=XY1[0], y=XY1[1])

if __name__ == "__main__":
    a = Helper()
    a.do()
    