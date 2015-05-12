__author__ = "Rohan Pandit"

from itertools import product
import numpy as np
from random import choice, uniform
import pickle as pkl
from time import time

def main():
    start = time()
    #prob = createDict()
    #pkl.dump(prob, open( 'probability.pkl', 'wb'))

    prob = pkl.load(open('probability.pkl', 'rb'))
    print("Number of boards: %s"%len(prob.keys()))

    print("Training...")
    for _ in range(10000000):
        trainingGame(prob)

    print( checkNonzero(prob) )
    pkl.dump(prob, open( 'filled_prob_human_start.pkl', 'wb'))


    with open('filled_prob_human_start.pkl', 'rb') as f:
        prob = pkl.load(f)

    print( "Time elapsed: %s \n"%(time() - start) )
    playGame(prob)

def createDict():
    prob = {}
    start = time()
    entered = 0

    for i in product('XO-', repeat=9):
        x = i.count('X')
        o = i.count('O')
        if x < 5 and o < 5 and abs(x-o) <= 1 and not checkWin(i):
            prob[''.join(i)] = [9]*9

    return prob

def trainingGame(prob):
    board = '-'*9
    score = [0]*8
    oppTurn(board, prob, score)  # modifies prob

def myTurn(board, prob, score):
    winner = checkWin(score, board)
    if winner:
        return winner

    move = choice(getMoves(board))
    board = board[:move] + 'X' + board[move + 1:]
    updateScore(score, move, 1)

    winner = oppTurn(board, prob, score)

    board = board[:move] + '-' + board[move + 1:]

    if winner == 'X':
        prob[board][move] += 3
    elif winner == 'O':
        prob[board][move] -= 1
    else:
        prob[board][move] += 1

    return winner

def oppTurn(board, prob, score):
    winner = checkWin(score, board)
    if winner:
        return winner

    moves = getMoves(board)
    move = choice(moves)
    board = board[:move] + 'O' + board[move + 1:]
    updateScore(score, move, -1)

    return myTurn(board, prob, score)

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

def playGame(prob):
    board = '-'*9
    print('Welcome to Tic-Tac Toe! Human Starts')
    print()

    score = [0]*8

    while not checkWin(score, board):
        pprint(board)
        board = humanTurn(board, score)

        if checkWin(score, board): break

        print("Computer turn")
        pprint(board)
        board = computerTurn(board, prob, score)


    pprint(board)
    print('')
    print(checkWin(score, board) + " won the game!")

    if input("Would you like to play again? y or n\n") == "y":
        playGame(prob)

def computerTurn(board, prob, score):
    move = weighted_choice(getMoves(board), prob[board])
    print('probs: ', prob[board])
    board = board[:move] + 'X' + board[move + 1:]
    print()
    updateScore(score, move, 1)
    return board

def humanTurn(board, score):
    move = input('Enter a index, human\n' )

    try:
        move = int(move)
    except ValueError:
        print('You are doing this wrong')

    while board[move] != '-':
        move = input('Try again, that index is taken\n')
        quit()

    board = board[:move] + 'O' + board[move + 1:]
    updateScore(score, move, -1)
    return board

def weighted_choice(choices, weights):
    weights = [weights[i] + 9 - min(weights) for i in choices]
    r = uniform(0, max(weights))
    upto = 0

    for c, w in zip(choices, weights):
        if upto + w > r:
            return c
        upto += w

def checkWin(score, board):
    for i in score:
        if i == 3: return "X"
        if i == -3: return "O"

    if board.count('-') == 0:
        return "NO ONE"


def pprint(obj):
    print( ' '.join([i if i!= '-' else str(j) for i,j in zip(obj[:3], range(3)) ]))
    print( ' '.join([i if i!= '-' else str(j) for i,j in zip(obj[3:6], range(3,6)) ]))
    print( ' '.join([i if i!= '-' else str(j) for i,j in zip(obj[6:9], range(6,9)) ]))

if __name__ == "__main__":
   main()