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
    #prob = pkl.load(open('probability.pkl', 'rb'))
    prob = pkl.load(open('filled_prob.pkl', 'rb'))
    print(len(prob.keys()))

    #for _ in range(10000):
    #    prob = fakeGame(prob)

    #pkl.dump(prob, open( 'filled_prob.pkl', 'wb'))

    print(time() - start)

    playGame(prob)

def pprint(obj):
    print(obj[:3])
    print(obj[3:6])
    print(obj[6:9])

def playGame(prob):
    board = '-'*9
    print('Welcome to Tic-Tac Toe!')

    while not checkWin(board):
        print("Computer turn")
        pprint(board)
        board = computerTurn(board, prob)

        pprint(board)
        move = int( input('Enter a index, human\n' ) )
        while board[move] != '-':
            move = int( input('Try again, that index is taken\n') )
        board = board[:move] + 'O' + board[move + 1:]

    print(checkWin(board) + " won the game!")

def computerTurn(board, prob):
    move = weighted_choice(getMoves(board), prob[board])
    print(prob[board])
    board = board[:move] + 'X' + board[move + 1:]
    return board


def fakeGame(prob):
    board = '-'*9
    moves = getMoves(board)
    move = choice(moves)
    board = board[:move] + 'X' + board[move+1:]

    winner = myTurn(board, prob)  # modifies prob

    board = board[:move] + '-' + board[move+1:]

    if winner == 'X':
        prob[board][move] += 3
    if winner == 'O':
        prob[board][move] -= 1
    else:
        prob[board][move] += 1

    return prob

def myTurn(board, prob):
    if checkWin(board):
        return checkWin(board)

    move = weighted_choice(getMoves(board), prob[board])
    board = board[:move] + 'X' + board[move + 1:]

    winner = oppTurn(board, prob)

    board = board[:move] + '-' + board[move + 1:]

    if winner == 'X':
        prob[board][move] += 3
    if winner == 'O':
        prob[board][move] -= 1
    else:
       prob[board][move] += 1

    return winner


def oppTurn(board, prob):
    if checkWin(board):
        return checkWin(board)

    move = choice(getMoves(board))
    board = board[:move] + 'O' + board[move + 1:]

    return myTurn(board, prob)


def getMoves(board):
    return [i for i, x in enumerate(board) if x == '-']


def weighted_choice(choices, weights):
    weights = [weights[i] for i in choices]
    r = uniform(0, max(weights))
    upto = 0

    for c, w in zip(choices, weights):
        if upto + w > r:
            return c
        upto += w


def createDict():
    prob = {}

    for x in range(6):
        for o in range(6):
            if abs(x - o) < 2:
                for i in permutations(x * 'X' + o * 'O' + (9 - x - o) * '-'):
                    prob[''.join(i)] = [1]*9

    return prob


def checkWin(board):
    boardCopy = board[:]
    board = np.array(list(board), dtype=np.dtype('str')).reshape((3, 3))

    for row in board:
        if all(row == 'X'):
            return 'X'
        elif all(row == 'O'):
            return 'O'

    for col in board.T:
        if all(col == 'X'):
            return 'X'
        elif all(col == 'O'):
            return 'O'

    if all( np.diagonal(board) == 'X') or all( np.diagonal(board.T) == 'X'):
        return 'X'

    if all( np.diagonal(board) == 'O') or all( np.diagonal(board.T) == 'O'):
        return 'O'

    if boardCopy.count('-') == 0: return 'DRAW'

    return ''

if __name__ == "__main__":
    main()