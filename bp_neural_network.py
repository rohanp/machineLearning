#!/usr/bin/env python
""" A Multilayer Artificial Neural Network with Backpropagation """

__author__ = 'Rohan Pandit'

from itertools import product
from time import clock
from math import exp
import numpy as np

TRIALS = 100000
ALPHA = 0.25 #learning rate
INPUT = np.array( list(filter( lambda x: x.count(1) == 1, product( [0,1], repeat=8))) )
INPUT = np.c_[INPUT, -1*np.ones(INPUT.shape[1])] #add bias
OUTPUT = { hash( tuple(x) ):  x[:-1] for x in INPUT }

def main():
    w, v_b, epochs = train()
    verifyNetwork(w, v_b)
    print("\nEpochs: ", epochs)

def train():
    epochs = 0
    w = 2*np.random.rand( 9,3 ) - 1
    v_b = 2*np.random.rand( 4, 8 ) - 1

    while not trained(w, v_b, epochs) and epochs < TRIALS:
        np.random.shuffle(INPUT)
        for x in INPUT:
            out, h_b = forward(x, w, v_b)
            target = x[:-1]

            h_b = h_b[:, np.newaxis] # 4x1
            h, v = h_b[:-1], v_b[:-1,:] # 3x1, 3x8 (remove bias)
            x = x[:, np.newaxis] # 9x1

            delta = ((out - target) * out * (1 - out))[np.newaxis, :] # 1x8
            v_b = v_b - ALPHA * np.dot(h_b, delta)
            w = w - ALPHA * np.dot(x, np.dot(delta, v.T) * (h * (1-h)).T)

            epochs += 1

            if epochs % 100 == 0:
                print("Epochs: ", epochs, "Error: ",sum( 0.5*(target-out)**2 ))

    return w, v_b, epochs

def forward(x, w, v_b):
    h = f( np.dot(x, w) )
    h_b = np.r_[h, -1*np.ones(1)] #add bias
    return f( np.dot(h_b, v_b) ), h_b

def f(x):
    return 1/(1+exp(-x))

def fprime(x):
    return f(x)*(1-f(x))

def trained(w, v_b, epochs):
    for x in INPUT:
        out, h_b = forward(x, w, v_b)

        E = error(x, out)
        if E > 0.1: return False

    return True

def error(x, out):
    return sum( 0.5*(x[:-1]-out)**2 )

def verifyNetwork(w, v_b):
    out = np.array([ forward(x, w, v_b)[0] for x in INPUT ])
    print(out)
    print("Data")
    print("x=\n", INPUT)
    print("out=\n", np.round(out, 0) )
    print("w=\n", w)
    print("v=\n", v_b)
    print("error=\n", np.add.reduce(0.5*(INPUT[:,:-1]-out)**2,0) )

f = np.vectorize(f)

if __name__ == "__main__":
    start = clock()
    main()
    print("Run time = ", round(clock() - start, 2) , " seconds")