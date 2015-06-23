#!/usr/bin/env python
""" Tic Tac Toe with Machine Learning AI """

__author__ = "Rohan Pandit"

from itertools import product, permutations
from random import uniform, choice
import pickle as pkl
from time import time
import numpy as np

def main():
    start = time()

    prob = createDict()
    oppProb = createDict()
    print("Number of boards: %s"%len(prob.keys()))

    print("Training...")
    for i in range(1000000):
        #bottomUpTraining(prob)
        trainingGame(prob, oppProb, i)

    print( checkNonzero(prob) )
    print( checkNonzero(oppProb) )
    pkl.dump(prob, open( 'filled_prob_human_start.pkl', 'wb'))


    with open('filled_prob_human_start.pkl', 'rb') as f:
        prob = pkl.load(f)

    oppProb = prob

    print( "Time elapsed: %s \n"%(time() - start) )

    playGame(prob, oppProb)

def createDict():
    prob = {}

    for board in product('XO-', repeat=9):
        x = board.count('X')
        o = board.count('O')
        if x < 5 and o < 5 and abs(x-o) <= 1:
            prob[''.join(board)] = [50]*9

    return prob

def bottomUpTraining(prob):
    for i in range(0, 9, -1):
        for board in product('XO-', repeat=i):
            x = board.count('X')
            o = board.count('O')
            if x < 5 and o < 5 and abs(x-o) <= 1 and not checkWin(board):
                pass

def trainingGame(prob, oppProb, gameNum):
    board = '-'*9
    score = [0]*8
    oppTurn(board, prob, oppProb, score, gameNum, 1)  # modifies prob

def myTurn(board, prob, oppProb, score, gameNum, depth):
    gwinner = getWinner(board)
    if gwinner: return gwinner

    try:
        move = choice( getMoves(board) )
        board = board[:move] + 'X' + board[move + 1:]
        updateScore(score, move, 1)

        winner = oppTurn(board, prob, oppProb, score, gameNum, depth + 1)

        board = board[:move] + '-' + board[move + 1:]

        if winner == 'X':
            prob[board][move] += 3
        elif winner == 'O':
            prob[board][move] -= 1
        else:
            prob[board][move] += 1

        if prob[board][move] < 0: prob[board][move] = 0

        return winner

    except IndexError:
        print(board)

def oppTurn(board, prob, oppProb, score, gameNum, depth):
    gwinner = getWinner(board)
    if gwinner: return gwinner

    try:
        move = choice( getMoves(board) )
        board = board[:move] + 'O' + board[move + 1:]
        updateScore(score, move, -1)

        winner = myTurn(board, prob, oppProb, score, gameNum, depth+1)

        board = board[:move] + '-' + board[move + 1:]

        if winner == 'X':
            oppProb[board][move] -= 1
        elif winner == 'O':
            oppProb[board][move] += 3
        else:
            oppProb[board][move] += 1

        if oppProb[board][move] < 0: oppProb[board][move] = 0

        return winner

    except IndexError:
        print("INDEX error")
        print(board)



def getMoves(board):
    return [i for i, x in enumerate(board) if x == '-']

def updateScore(score, move, player):
    row = move // 3
    col = move % 3

    score[row] += player
    score[3 + col] += player

    if (row == col):
        score[6] += player
    if (3 - 1 - col == row):
        score[7] += player

def checkNonzero(prob):
    count = 0
    for i in prob.keys():
        for j in prob[i]:
            if j != 9:
                count+=1
                break

    return count

def oldCheckWin(board):
    ### check if any of the rows has winning combination
    for i in range(3):
        if len(set(board[i*3:i*3+3])) is  1 and board[i*3] is not '-':
            return True
    ### check if any of the Columns has winning combination
    for i in range(3):
       if (board[i] is board[i+3]) and (board[i] is  board[i+6]) and board[i] is not '-':
           return True
    ### 2,4,6 and 0,4,8 cases
    if board[0] is board[4] and board[4] is board[8] and board[4] is not '-':
        return  True
    if board[2] is board[4] and board[4] is board[6] and board[4] is not '-':
        return  True
    return False

def checkWin(score, board):
    for i in score:
        if i == 3: return "X"
        if i == -3: return "O"

    if board.count('-') == 0:
        return "NO ONE"

def pprint(obj):
    print( ' '.join([i if i!= '-' else str(j) for i,j in zip(obj[:3], range(3)) ]) )
    print( ' '.join([i if i!= '-' else str(j) for i,j in zip(obj[3:6], range(3,6)) ]) )
    print( ' '.join([i if i!= '-' else str(j) for i,j in zip(obj[6:9], range(6,9)) ]) )

def getWinner(board):
    for i in range(3):
        if len(set(board[i*3:i*3+3])) is  1 and board[i*3] is not '-':
            return board[i*3]
    ### check if any of the Columns has winning combination
    for i in range(3):
       if (board[i] is board[i+3]) and (board[i] is  board[i+6]) and board[i] is not '-':
           return board[i]
    ### 2,4,6 and 0,4,8 cases
    if board[0] is board[4] and board[4] is board[8] and board[4] is not '-':
        return  board[0]
    if board[2] is board[4] and board[4] is board[6] and board[4] is not '-':
        return  board[2]

    if board.count('-') == 0:
        return "NO ONE"

    return False

def test():
    board = '-OX--X--O'
    prob = createDict()
    oppProb = createDict()
    ratio = [0,0,0]

    for i in range(100000):
        win = myTurn(board, prob, oppProb, [0]*9, 0, 1)

        if win == 'X':
            ratio[0] += 1
        elif win == 'O':
            ratio[1] += 1
        else:
            ratio[2] += 1

    print([x/sum(ratio) for x in ratio])

test()