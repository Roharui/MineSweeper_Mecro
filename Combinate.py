
result = []

def combination2(n, r, l):
    global result
    if r == 0:
        result.append(l)
        return
    if len(n) == r:
        result.append(l + n)
        return
    for num, i in enumerate(n):
        combination2(n[num + 1:], r - 1, l + [i])

def combination(n, r):
    global result
    result = []
    combination2(n, r, [])
    return result

class Decart:
    def __init__(self):
        self.a = []
        self.b = []

        self.ac = 0
        self.bc = 0

        self.data = []

    def make(self, a, b):
        self.ac += len(a[0])
        self.bc = len(b[0])
        for i in a:
            for j in b:
                data = self.times(i, j)
                if self.isCTD(data) and not data in self.data:
                    self.data.append(data)

    def setAB(self, a, b):
        if not self.a:
            self.a = a
        else:
            self.a = self.times(self.a, self.b)
        self.b = b

    def times(self, a, b):
        for i in a:
            try:
                b.remove(i)
            except ValueError:
                pass
        return a + b

    def getElse(self, selected):
        result = list(self.a[:])
        for i in selected:
            result.remove(i)
        return result

    def isCTD(self, data):
        c1 = 0
        c2 = 0

        for i in data:
            if i in self.a:
                c1 += 1
            if i in self.b:
                c2 += 1
        
        return ((self.ac == c1) and (self.bc == c2))
        