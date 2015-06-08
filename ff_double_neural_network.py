__author__ = 'Rohan Pandit'

import numpy as np
from itertools import product
from random import random, shuffle
from time import clock

TRIALS = 500000
ALPHA = 0.20 #learning rate
INPUT_1 = np.array([[0.1,2,0,-1], [-0.1,2,0,-1], [0.1,-2,1,-1], [-0.1, -2,1,-1] ])
INPUT_2 = np.array([[2,0.1,0,-1], [-2,0.1,0,-1], [-2,-0.1,1,-1], [2,-0.1,1,-1]])
OUTPUT_1 = { hash( tuple(x) ):  0 > x[0] for x in INPUT_1 }
OUTPUT_2 = { hash( tuple(x) ):  0 > x[1] for x in INPUT_2 }

def main():
    w1, w2, epochs = train()

    print("m = ", -w1[0]/w1[1], " b = ", w1[2]/w1[1])
    print("m = ", -w2[0]/w2[1], " b = ", w2[2]/w2[1])

    verifyNetwork(w1, w2)
    print("Epochs: ", epochs)

def train():
    w1 = 2*np.random.rand( INPUT_1.shape[1] ) - 1
    w2 = 2*np.random.rand( INPUT_2.shape[1] ) - 1

    epochs = 0

    while not trained1(while1) and not trained2(w2) and epochs < TRIALS:
        np.random.shuffle(INPUT_1)
        for x in INPUT_1:
            out = np.dot(x, w1) > 0
            target = OUTPUT_1[ hash( tuple(x) ) ]
            w1 = w1 - ALPHA * (out - int(target)) * x

        np.random.shuffle(INPUT_2)
        for x in INPUT_2:
            out = np.dot(x, w2) > 0
            target = OUTPUT_2[ hash( tuple(x) ) ]
            w2 = w2 - ALPHA * (out - int(target)) * x
            epochs += 1

    return w1, w2, epochs

def trained1(w):
    for x in INPUT_1:
        if OUTPUT_1[ hash( tuple(x) ) ] != (np.dot(x, w) > 0):
            return False

    return True

def trained2(w):
    for x in INPUT_2:
        if OUTPUT_2[ hash( tuple(x) ) ] != (np.dot(x, w) > 0):
            return False
    return True

def verifyNetwork(w1, w2):
    for x in INPUT_1:
        print(x[0], ',', x[1] , " = ", np.dot(x, w1) > 0)
    for x in INPUT_2:
        print(x[0], ',', x[1] , " = ", np.dot(x, w2) > 0)
    print()

if __name__ == "__main__":
    start = clock()
    main()
    print("Run time = ", round(clock() - start, 2) , " seconds")