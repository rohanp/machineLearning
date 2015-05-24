__author__ = 'Rohan Pandit'

import numpy as np
from itertools import product
from random import random, choice, randrange
from time import clock

TRIALS = 30
ALPHA = 0.25 #learning rate
INPUT = np.array( [(0,0,-1), (0,1,-1), (1,0,-1), (1,1,-1)], ndmin=2)
OUTPUT = { hash((i, j)): i or j for (i, j, b) in INPUT }

def main():
    weights, epochs = train()
    verifyNetwork(weights)
    print("Weights: ", weights)
    print("Epochs: ", epochs)

def train():
    w = np.random.rand(3)
    epochs = 0

    for t in range(TRIALS):
        idx = randrange(0, INPUT.shape[0])
        x = INPUT[idx]

        out = np.dot(x, w) > 0
        target = OUTPUT[ hash( (x[0], x[1]) ) ]

        w = w - ALPHA * (out - target) * x

        if trained(w):
            epochs = t
            break

    return w, epochs

def trained(w):
    for x in INPUT:
        if OUTPUT[ hash( (x[0], x[1]) ) ] != (np.dot(x, w) > 0):
            return False

    return True

def verifyNetwork(w):
    for x in INPUT:
        print(x[0], 'or', x[1] , end=" = ")
        print(np.dot(x, w) > 0)

if __name__ == "__main__":
    start = clock()
    main()
    print("Run time = ", round(clock() - start, 2) , " seconds")
