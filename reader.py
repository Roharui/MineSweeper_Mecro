
import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False

import pyautogui as auto
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.models import model_from_json
import matplotlib.pyplot as plt

class Reader:
    path = "my_screenshot.png"

    def __init__(self, xy1, xy2, count):
        self.xy1 = xy1#(1403, 180)
        self.xy2 = xy2#(1801, 928)

        self.count = count#(16, 30)

        self.x = 16#int((self.xy2[0] - self.xy1[0]) / self.count[0]) + 1
        self.y = 16#int((self.xy2[1] - self.xy1[1]) / self.count[1]) + 1
        
        
        json_file = open("number_model (2).json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights('number_model (2).h5')
        
    
    def read(self):
        auto.screenshot(self.path, region=(self.xy1[0], self.xy1[1],
                                            self.xy2[0] - self.xy1[0],
                                             self.xy2[1] - self.xy1[1]))

        self.img = cv2.imread(self.path)
        lst = []
        for i in range(self.count[1]):
            for j in range(self.count[0]):
                _ = 1 - self.img[i * self.y:(i + 1) * self.y, j * self.x:(j + 1) * self.x]
                lst.append(_)

        self.lst = np.array(lst)
        lst = np.array(lst)
        c = self.model.predict(lst)
        return np.argmax(c, axis=1).reshape(self.count[1], self.count[0])

    def showT(self, locs):
        c = self.img.copy()
        for y, x in locs:
            c[y * self.y:(y + 1) * self.y, x * self.x:(x + 1) * self.x] = np.zeros((16, 16, 3))
        cv2.imshow("ori", c)
        cv2.waitKey(0)

    def show(self):
        lst = self.lst.reshape(self.count[1], self.count[0], self.y, self.x, 3)
        k = np.array([lst[1, 0]])
        cv2.imshow("ori", k[0])
        cv2.waitKey(0)
        np.save("xp\\9.npy", k)

class TESTReader:
    path = "my_screenshot.png"

    def __init__(self, xy1, xy2, count):
        self.xy1 = xy1#(1403, 180)
        self.xy2 = xy2#(1801, 928)

        self.count = count#(16, 30)
        
    
    def read(self):
        auto.screenshot(self.path, region=(self.xy1[0], self.xy1[1],
                                            self.xy2[0] - self.xy1[0],
                                             self.xy2[1] - self.xy1[1]))

        self.img = cv2.imread(self.path)
        cv2.imshow("ori", self.img)
        cv2.waitKey(0)

if __name__ == '__main__':
    
    x, y = (480, 256)
    startx, starty = (1360, 100)
    a = Reader((startx, starty), (startx + x, starty + y), (30, 16))
    while True:

        print(a.read())
        input()
    #a.show()
    