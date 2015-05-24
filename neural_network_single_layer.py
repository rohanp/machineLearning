__author__ = 'Rohan Pandit'

import numpy as np
from itertools import product
from random import random, shuffle
from time import clock

TRIALS = 3000
ALPHA = 0.25 #learning rate
INPUT = np.array( [ [i, j] + [-1] for i, j in product( (0,1), repeat=2) ], ndmin=2)
OUTPUT = { hash( tuple(x) ): x[0] or x[1] for x in INPUT }

def main():
    weights, epochs = train()
    verifyNetwork(weights)
    print("Weights: ", weights)
    print("Epochs: ", epochs)

def train():
    w = np.random.rand( INPUT.shape[1] )
    epochs = 0

    while not trained(w) and epochs < TRIALS:
        np.random.shuffle(INPUT)
        for x in INPUT:
            out = np.dot(x, w) > 0
            target = OUTPUT[ hash( tuple(x) ) ]

            w = w - ALPHA * (out - target) * x
            epochs += 1

    return w, epochs

def trained(w):
    for x in INPUT:
        if OUTPUT[ hash( tuple(x) ) ] != (np.dot(x, w) > 0):
            return False
    return True

def verifyNetwork(w):
    for x in INPUT:
        print(x[0], 'or', x[1] , end=" = ")
        print(np.dot(x, w) > 0)
    print()

if __name__ == "__main__":
    start = clock()
    main()
    print("Run time = ", round(clock() - start, 2) , " seconds")