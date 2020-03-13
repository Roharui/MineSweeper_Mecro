
import numpy as np
from reader import Reader
from Combinate import combination, Decart

SIZEX, SIZEY = (480, 256)
XY1 = (1358, 100)
XY2 = (XY1[0] + SIZEX, XY1[1] + SIZEY)
COUNT = (30, 16)

class Calculater:
    isDone = False
    dcart = Decart()
    def __init__(self, XY1, XY2, COUNT):
        self.reader = Reader(XY1, XY2, COUNT)
        #pass

    def pretreat(self):

        self.space = self.reader.read()
        '''
        self.space = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]
        self.space = np.array(self.space)
        '''
        ###

        self.clst = []

        for i in self.getNumber():
            self.clst.append(self.getEdge(i))

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
                    if self.space[y + i, x + j] == 0:
                        edge.append([y + i, x + j])
                    elif self.space[y + i, x + j] == 8:
                        num -= 1
                except IndexError:
                    pass
        return (num, edge)

    def combinateEdge(self):
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
    
    def clickWhere(self):
        return self.result[0]

    def do(self):
        self.pretreat()
        self.combinateEdge()
        self.find_ctd()

if __name__ == '__main__':
    a = Calculater(XY1, XY2, COUNT)
    a.do()
