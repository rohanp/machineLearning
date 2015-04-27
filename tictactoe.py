__author__ = "Rohan Pandit"

from itertools import permutations
import numpy as np
from random import choice, uniform
import pickle as pkl
from time import time
from numba import jit

def main():
	start = time()
	#prob = createDict()
	#pkl.dump(prob, open( 'probability.pkl', 'wb'))
	prob = pkl.load( open('probability.pkl', 'rb') )

	print(time()- start)

	prob = improveDict(prob)


def improveDict(prob):
	for state in prob.keys():

		moves = getMoves( map(int, list(state) ) )

		for move in moves:

			winner = playGame(state, move, prob)

			if winner == 1:
				if prob[ state ][ move ] < 0.97: prob[ state ][ move ] += 0.03 
			if winner == 2:
				if 0.1 < prob[ state ][ move ]: prob[ state ][ move ] -= 0.01
			else:
				if prob[ state ][ move ] < 0.99: prob[ state ][ move ] += 0.01 


def getMoves(state):
	return [i for i, x in enumerate(state) if int(x) == 0]

def playGame(state, move, prob):
	state = map(int, list(state))

	while not checkWin(state):
		state = myTurn(state, prob)
		state = oppTurn(state)

	return checkWin(state)

def myTurn(state, prob):
	move = weighted_choice(getMoves(state), prob[ ''.join(str(v) for v in state) ])
	state[move] = 1
	return state

def oppTurn(state):
	move = choice( getMoves(state) )
	state[move] = 2
	return state

def weighted_choice(choices, weights):
   r = uniform(0, 1)
   upto = 0

   print(choices, weights)

   for c, w in zip(choices, weights):
      if upto + w > r:
         return c
      upto += w

def createDict():
	prob = {}

	for x in range(4):
		for o in range(4):
			for i in permutations(x*'1'+o*'2'+(9 - x - o)*'0'):
				prob[ ''.join(i) ] = getMoves(i)

	return prob

def checkWin(state):

	state = np.array( state, dtype=int ).reshape( (3,3) )
	win_prob = [
        # horizontal
        ((0,0), (1,0), (2,0)),
        ((0,1), (1,1), (2,1)),
        ((0,2), (1,2), (2,2)),
        # vertical
        ((0,0), (0,1), (0,2)),
        ((1,0), (1,1), (1,2)),
        ((2,0), (2,1), (2,2)),
        # crossed
        ((0,0), (1,1), (2,2)),
        ((2,0), (1,1), (0,2))
    ]

	for win_state in win_prob:
		in_a_row = ''
		for coord in win_state:
			in_a_row += str(state[coord])

		xs = in_a_row.count('1')
		os = in_a_row.count('2')

		if xs == 2 or os == 2:
			return 1 if xs > os else 2

	return 0

if __name__ == "__main__":
	main()