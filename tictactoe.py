__author__ = "Rohan Pandit"

from itertools import product
from random import uniform, choice
import pickle as pkl
from time import time

def main():
    start = time()

    prob = createDict()
    oppProb = createDict()
    print("Number of boards: %s"%len(prob.keys()))

    print("Training...")
    for i in range(1000000):
        trainingGame(prob, oppProb, i)

    print( checkNonzero(prob) )
    print( checkNonzero(oppProb) )
    pkl.dump(prob, open( 'filled_prob_human_start.pkl', 'wb'))

    with open('filled_prob_human_start.pkl', 'rb') as f:
        prob = pkl.load(f)

    print( "Time elapsed: %s \n"%(time() - start) )
    playGame(prob, oppProb)

def createDict():
    prob = {}

    for i in product('XO-', repeat=9):
        x = i.count('X')
        o = i.count('O')
        if x < 5 and o < 5 and abs(x-o) <= 1:
            prob[''.join(i)] = [50]*9

    return prob

def trainingGame(prob, oppProb, gameNum):
    board = 'O' + '-'*8
    score = [0]*8
    myTurn(board, prob, oppProb, score, gameNum, 1)  # modifies prob

def myTurn(board, prob, oppProb, score, gameNum, depth):
    gwinner = checkWin(score, board)
    if gwinner: return gwinner

    if 100000 < gameNum:
        move = weighted_choice( getMoves(board), prob[board] )
    else:
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

def oppTurn(board, prob, oppProb, score, gameNum, depth):
    gwinner = checkWin(score, board)
    if gwinner: return gwinner

    if 100000 < gameNum and 0 < depth:
        move = weighted_choice( getMoves(board), oppProb[board] )
    else:
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

def getMoves(board):
    return [i for i, x in enumerate(board) if x == '-']


def weighted_choice_careful(choices, weights):
    weights = [weights[i] - min(weights) + 1 for i in choices]
    r = uniform(0, max(weights))
    upto = 0

    for c, w in zip(choices, weights):
        if upto + w >= r:
            return c
        upto += w


def weighted_choice(choices, weights):
    weights = [weights[i] + 0.4*max(weights) for i in choices]
    r = uniform(0, max(weights))
    upto = 0

    for c, w in zip(choices, weights):
        if upto + w >= r:
            return c
        upto += w

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

def playGame(prob, oppProb):
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
        board = computerTurn(board, prob, oppProb, score)
        print('opp probs:', oppProb[board])


    pprint(board)
    print('')
    print(checkWin(score, board) + " won the game!")

    if input("Would you like to play again? y or n\n") == "y":
        playGame(prob, oppProb)

def computerTurn(board, prob, oppProb, score):
    move = weighted_choice_careful( getMoves(board), prob[board] )

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

if __name__ == "__main__":
   main()