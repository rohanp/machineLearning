__author__ = 'Rohan Pandit'

import numpy as np
from itertools import product
from random import random, shuffle
from time import clock

TRIALS = 50000
ALPHA = 0.25 #learning rate
INPUT = np.array( list( product( (0,1), repeat=2) ) , ndmin=2)
INPUT = np.c_[INPUT, -1*np.ones( INPUT.shape[0] )].astype(dtype=int) #add bias
OUTPUT = { hash( tuple(x) ):  x[0] ^ x[1] for x in INPUT }

def main():
    w, v, epochs = train()
    verifyNetwork(w, v)
    print("\nEpochs: ", epochs)

def train(epochs = 0):
    w = 2*np.random.rand( 3,2 ) - 1
    v  = 2*np.random.rand( 3 ) - 1

    while not trained(w, v) and epochs < TRIALS:
        np.random.shuffle(INPUT)
        w = np.random.rand( 3,2 ) - 1
        v  = 2*np.random.rand( 3 ) - 1

        for x in INPUT:
            out = f(x, w, v)
            target = OUTPUT[ hash( tuple(x) ) ]


            epochs += 1

    return w, v, epochs

def trained(w, v):
    for x in INPUT:
        if OUTPUT[ hash( tuple(x) ) ] != f(x, w, v):
            return False
    return True

def verifyNetwork(w, v):
    for x in INPUT:
        print(x[0], ',', x[1] , " = ", f(x, w, v))
    print()

    print("Statistics")
    print("x=\n", INPUT)
    print("w=\n", w)
    print("v=\n", v)

def f(x, w, v):
    h = np.array([ np.dot(x, w[:,0]) > 0, np.dot(x, w[:,1]) > 0, -1])
    return np.dot(v, h) > 0


if __name__ == "__main__":
    start = clock()
    main()
    print("Run time = ", round(clock() - start, 2) , " seconds")
