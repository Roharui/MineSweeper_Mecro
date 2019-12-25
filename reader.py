
import tensorflow.python.util.deprecation as deprecation
deprecation._PRINT_DEPRECATION_WARNINGS = False

import pyautogui as auto
import cv2
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.models import model_from_json
import matplotlib.pyplot as plt

class Reader:
    path = "my_screenshot.png"

    def __init__(self, xy1, xy2, count):
        self.xy1 = xy1#(1403, 180)
        self.xy2 = xy2#(1801, 928)

        self.count = count#(16, 30)

        self.x = int((self.xy2[0] - self.xy1[0]) / self.count[0]) + 1
        self.y = int((self.xy2[1] - self.xy1[1]) / self.count[1]) + 1
        
        json_file = open("number_model.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights('number_model.h5')
    
    def read(self):
        auto.screenshot(self.path, region=(self.xy1[0], self.xy1[1],
                                            self.xy2[0] - self.xy1[0],
                                             self.xy2[1] - self.xy1[1]))

        self.img = cv2.imread(self.path)
        lst = []
        for i in range(self.count[1]):
            for j in range(self.count[0]):
                _ = 1 - self.img[i * self.y + 2:(i + 1) * self.y -3, j * self.x + 1:(j + 1) * self.x -3]
                _ = cv2.resize(_, (20, 21), interpolation=cv2.INTER_AREA)
                lst.append(_)
        
        lst = np.array(lst).reshape(-1, 20, 21, 3)
        c = self.model.predict(lst)
        return np.argmax(c, axis=1).reshape(self.count[1], self.count[0])

    def show(self):
        lst = self.lst.reshape(self.count[1], self.count[0], 20, 21, 3)
        k = np.array([lst[6, 8]])
        cv2.imshow("ori", k[0])
        cv2.waitKey(0)
        np.save("six.npy", k)

if __name__ == '__main__':
    a = Reader((1403, 180), (1801, 928), (16, 30))
    a.read()
    a.show()