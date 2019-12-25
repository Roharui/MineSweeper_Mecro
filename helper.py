
from reader import Reader
import numpy as np
import pyautogui as auto
import matplotlib.pyplot as plt
import seaborn as sns
from random import randint
from time import sleep

XY1 = (1403, 180)
XY2 = (1801, 928)
COUNT = (16, 30)

X = int((XY2[0] - XY1[0]) / COUNT[0]) + 1
Y = int((XY2[1] - XY1[1]) / COUNT[1]) + 1

class Helper:

    class Calculater:
        def __init__(self):
            self.reader = Reader(XY1, XY2, COUNT)

        def pretreat(self):
            self.space = self.reader.read()
            sns.heatmap(self.space, annot=True)
            plt.show()
            self.canClick = np.zeros(self.space.shape) - 1
            self.mine = []

        def getNumber(self):
            a, b = np.where((self.space > 0) * (self.space < 6))
            return [[i, j] for i, j in zip(a, b)]

        def getEdge(self, loc):
            edge = []
            
            y, x = loc
            num = self.space[y, x]

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: continue
                    if y + i < 0 or x + j < 0: continue
                    try:
                        if self.space[y + i, x + j] == 6:
                            edge.append([y + i, x + j])
                        elif self.space[y + i, x + j] == 7:
                            num -= 1
                    except IndexError:
                        pass
            return (num, edge)

        def persent(self, loc):
            num, edge = self.getEdge(loc)

            mine = np.copy(self.canClick)
            
            for y, x in edge:
                if num == 0:
                    mine[y, x] = 0
                mine[y, x] = num / len(edge)

            self.mine.append(mine)

        def realPersent(self):
            mine = np.max(self.mine, axis=0)
            mine2 = np.all(self.mine, axis=0)
            self.mine = mine * mine2
            
        def clickWhere(self):
            a, b = np.where(self.mine == 1)
            c, d = np.where(self.mine == 0)
            r = [[i, j] for i, j in zip(a, b)] 
            l = [[i, j] for i, j in zip(c, d)]

            if len(r) == 0 and len(l) == 0:
                ac = np.abs(self.mine)
                a, b = np.where(ac == np.min(ac))
                l = [[a[0], b[0]]]

                #sns.heatmap(ac, annot=True)
                #plt.show()

            return (r, l)


        def do(self):
            self.pretreat()
            [self.persent(i) for i in self.getNumber()]
            self.realPersent()
            #sns.heatmap(self.mine, annot=True)
            #plt.show()

    def __init__(self):
        self.calc = self.Calculater()
        self.clickL([randint(0, COUNT[1]), randint(0, COUNT[0])])
    
    def do(self):
        self.home()
        self.calc.do()

        right, left = self.calc.clickWhere()

        for loc in right:
            self.clickR(loc)

        for loc in left:
            self.clickL(loc)

    def clickR(self, loc):
        y, x = loc
        self.home()
        auto.moveRel((x * X) + 3, (y * Y) + 3)
        auto.rightClick()
        
    def clickL(self, loc):
        y, x = loc
        self.home()
        auto.moveRel((x * X) + 3, (y * Y) + 3)
        auto.click()

    def home(self):
        auto.moveTo(x=XY1[0], y=XY1[1])

    def away(self):
        auto.moveTo(0, 0)

if __name__ == "__main__":
    h = Helper()
    for i in range(100):
        h.do()
        sleep(0.2)