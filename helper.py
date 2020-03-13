
from reader import Reader
import numpy as np
import pyautogui as auto
import matplotlib.pyplot as plt
import seaborn as sns
from random import randint
from time import sleep
from Combinate import Decart, combination

SIZEX, SIZEY = (480, 256)
XY1 = (1360, 100)
XY2 = (XY1[0] + SIZEX, XY1[1] + SIZEY)
COUNT = (30, 16)
RESET = (1594, 83)
MCOUNT = 99

X = 16#int((XY2[0] - XY1[0]) / COUNT[0]) + 1
Y = 16#int((XY2[1] - XY1[1]) / COUNT[1]) + 1
plt.ion()

class Helper:
    count_m = 0
    class Calculater:
        isDone = False
        dcart = Decart()
        def __init__(self, preant):
            self.reader = Reader(XY1, XY2, COUNT)
            self.preant = preant

            np.save('datax', [])
            np.save('datay', [])

        def pretreat(self):
            self.space = self.reader.read()
            self.canClick = np.zeros(self.space.shape) - 1
            self.mine = []

        def getNumber(self):
            a, b = np.where((self.space > 0) * (self.space < 7))
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
                        if self.space[y + i, x + j] == 7:
                            edge.append([y + i, x + j])
                        elif self.space[y + i, x + j] == 8:
                            num -= 1
                    except IndexError:
                        pass
            return (num, edge)

        def persent(self, loc):
            num, edge = self.getEdge(loc)

            mine = np.copy(self.canClick)
            
            for y, x in edge:
                mine[y, x] = num / len(edge)

            if edge:
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
                '''
                self.combinateEdge()
                self.find_ctd()
                for i in self.result:
                    self.reader.showT(i)
                
                auto.click(RESET)
                '''
                a, b = np.where(self.mine + self.space == 6)
                #print((MCOUNT - self.preant.count_m)/a.shape[0])
                #print(np.min(np.abs(self.mine)))
                if (MCOUNT - self.preant.count_m)/a.shape[0] > np.min(np.abs(self.mine)):
                    ac = np.abs(self.mine)
                    a, b = np.where(ac == np.min(ac))
                rand = randint(0, len(a) - 1)
                l = [[a[rand], b[rand]]]
                
            #self.save((r, l))
            
            return (r, l)
        
        def checkBoom(self):
            if np.where(self.space == 9)[0].shape[0] > 0:
                return True

        def combinateEdge(self):
            self.clst = [self.getEdge(x) for x in self.getNumber()]
            self.cdlst = []

            for num, edge in self.clst:
                self.cdlst.append(combination(edge, num))

        def find_ctd(self):
            result = self.cdlst[0]
            for i in range(1, len(self.clst)):
                self.dcart.setAB(self.clst[i - 1][1], self.clst[i][1])
                self.dcart.make(result, self.cdlst[i])
                result = self.dcart.data
            self.result = result

        def save(self, loc):
            datax = np.load('datax.npy')
            datay = np.load('datay.npy')
            
            datay_ = np.zeros(self.space.shape)
            right, left = loc

            for i in right:
                datay_[i[0], i[1]] = -1
            for i in left:
                datay_[i[0], i[1]] = 1

            print(datax.shape)

            if datax.shape[0] == 0:
                datax = self.space[np.newaxis]
                datay = datay_[np.newaxis]
            else:
                datax = np.append(datax, self.space[np.newaxis], axis=0)
                datay = np.append(datay, datay_[np.newaxis], axis=0)


            
            np.save('datax.npy', datax)
            np.save('datay.npy', datay)

        def do(self):
            self.pretreat()
            if self.checkBoom(): return True 
            [self.persent(i) for i in self.getNumber()]
            self.realPersent()
            #plt.clf()
            #sns.heatmap(self.mine, annot=False, cbar=False,  linewidths=.5, vmin=0, vmax=1)
            #plt.draw()
            #plt.pause(0.01)

    def __init__(self):
        self.calc = self.Calculater(self)
        auto.click(RESET)
        auto.click(RESET)
        self.clickL([randint(0, COUNT[1] - 1) , randint(0, COUNT[0] - 1)])
    
    def do(self):
        self.home()
        if self.calc.do(): return True

        right, left = self.calc.clickWhere()

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
    #sns.heatmap(np.zeros(COUNT))
    #plt.draw()
    #plt.pause(0.1)
    input("Start?")
    
    isDone = True

    while isDone:
        h = Helper()
        for i in range(1000):
            if MCOUNT - h.count_m == 0:
                isDone = False
                break
            print("%d번 턴"%i)
            if h.do():
                break
            sleep(0.05)
    