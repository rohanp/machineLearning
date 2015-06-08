__author__ = 'Rohan Pandit'

import numpy as np
from itertools import product
from random import random, shuffle
from time import clock

TRIALS = 500000
ALPHA = 0.25 #learning rate
INPUT = np.array( [[0,4], [4,0], [2.01,2.01]] )  #np.array( list( product( (0,1), repeat=2) ) , ndmin=2)
INPUT = np.c_[INPUT, -1*np.ones( INPUT.shape[0] )].astype(dtype=float) #add bias
OUTPUT = { hash( tuple(x) ):  4 - x[0] < x[1] for x in INPUT }
INPUT_TEST =  np.array( [[0,4], [4,0], [2.01, 2.01], [4.1,0], [0,4.1]] )
INPUT_TEST = np.c_[INPUT_TEST, -1*np.ones( INPUT_TEST.shape[0] )].astype(dtype=float) #add bias
OUTPUT_TEST = { hash( tuple(x) ):  4 - x[0] < x[1] for x in INPUT_TEST }

def main():
    w, epochs = train()
    print("m = ", -w[0]/w[1], " b = ", w[2]/w[1])
    verifyNetwork(w)
    print("Epochs: ", epochs)

def train():
    w = 2*np.random.rand( INPUT.shape[1] ) - 1
    epochs = 0

    while not trained(w) and epochs < TRIALS:
        np.random.shuffle(INPUT)
        for x in INPUT:
            out = np.dot(x, w) > 0
            target = OUTPUT[ hash( tuple(x) ) ]

            w = w - ALPHA * (out - int(target)) * x
            epochs += 1

    return w, epochs

def trained(w):
    for x in INPUT:
        if OUTPUT[ hash( tuple(x) ) ] != (np.dot(x, w) > 0):
            return False
    return True

def verifyNetwork(w):
    for x in INPUT_TEST:
        print(x[0], ',', x[1] , " = ", np.dot(x, w) > 0)
    print()

if __name__ == "__main__":
    start = clock()
    main()
    print("Run time = ", round(clock() - start, 2) , " seconds")