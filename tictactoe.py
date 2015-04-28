__author__ = "Rohan Pandit"

from itertools import permutations
import numpy as np
from random import choice, uniform
import pickle as pkl
from time import time


def main():
    start = time()
    #prob = createDict()
    #pkl.dump(prob, open( 'probability.pkl', 'wb'))
    prob = pkl.load(open('probability.pkl', 'rb'))
    print(len(prob.keys()))
    prob = fakeGame(prob)
    print(time() - start)

    playGame(prob)


def playGame():
    board = np.array(list("-" * 9), dtype=np.dtype('a1')).reshape((3, 3))
    print('Welcome to Tic-Tac Toe! Enter a coord to begin')

    while not checkWin(board):
        print(board)
        board = board[:move] + 'O' + board[move + 1:]
        board = computerTurn(board)


def computerTurn(board, prob):
    board = str(board)
    move = weighted_choice(getMoves(board), prob[board])
    board = board[:move] + 'X' + board[move + 1:]
    return np.array(list(board), dtype=np.dtype('a1')).reshape((3, 3))


def fakeGame(prob):
    for board in prob.keys():
        moves = getMoves(board)

        for move in moves:
            myTurn(board[:], prob)  # modified prob


def myTurn(board, prob):
    if checkWin(board):
        return checkWin(board)

    move = weighted_choice(getMoves(board), prob[board])
    board = board[:move] + 'X' + board[move + 1:]

    winner = oppTurn(board, prob)

    board = board[:move] + '-' + board[move + 1:]

    if winner == 'X':
        if prob[board][move] < 0.97: prob[board][move] += 0.03
    if winner == 'O':
        if 0.1 < prob[board][move]: prob[board][move] -= 0.01
    else:
        if prob[board][move] < 0.99: prob[board][move] += 0.01

    return winner


def oppTurn(board, prob):
    if checkWin(board):
        return checkWin(board)

    move = choice(getMoves(board))
    print(move)
    board = board[:move] + 'O' + board[move + 1:]

    print(board)
    return myTurn(board, prob)


def getMoves(board):
    return [i for i, x in enumerate(board) if x == '-']


def weighted_choice(choices, weights):
    weights = [weights[i] for i in choices]
    r = uniform(0, 1)
    upto = 0

    for c, w in zip(choices, weights):
        if upto + w > r:
            return c
        upto += w


def createDict():
    prob = {}

    for x in range(5):
        for o in range(5):
            if abs(x - o) < 2:
                for i in permutations(x * 'X' + o * 'O' + (9 - x - o) * '-'):
                    if not checkWin(i):
                        prob[''.join(i)] = [0]*9

    return prob


def checkWin(board):
    if board.count('-') == 0: return 'DRAW'

    board = np.array(list(board), dtype=np.dtype('a1')).reshape((3, 3))
    win_prob = [
        # horizontal
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),
        # vertical
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),
        # crossed
        ((0, 0), (1, 1), (2, 2)),
        ((2, 0), (1, 1), (0, 2))
    ]

    for win_board in win_prob:
        in_a_row = ''
        for coord in win_board:
            in_a_row += str(board[coord])

        xs = in_a_row.count('X')
        os = in_a_row.count('O')

        if abs(xs - os) == 2:
            return 'X' if xs > os else 'O'

    return ''


if __name__ == "__main__":
    main()