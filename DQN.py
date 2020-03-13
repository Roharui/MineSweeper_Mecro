
import reader as rd
from reader import tf
from random import random
import numpy as np

keras = tf.keras

class QL:
    episod = 1000
    def __init__(self, reader):
        self.reader = reader
        self.datas = []

        self.model = self.makeModel()

    def makeModel(self):
        model = rd.Sequential()
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(800, activation='relu'))
        model.add(keras.layers.Dense(480, activation='liner'))
        model.add(keras.layers.Reshape((16, 30)))
        return model
    
    def isRandom(self):
        return (self.episod/1000) > random()

    def do(self):
        for i in range(self.episod):
            x = self.reader.read()
            y_pre = None
            if self.isRandom():
                c = np.array(np.where(x == 0)).T
                y_pre = np.random.choice(c, 5, replace=False)
            else:
                c = self.model.predict(x)

    