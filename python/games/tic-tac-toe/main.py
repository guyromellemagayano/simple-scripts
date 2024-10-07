"""
Tic Tac Toe

A classic Python game of X's and O's. 
"""

import random

# Function that will draw the game's board


def makeBoard(board):
    print(end='\n')
    print('        |        |        ')
    print('    ' + board[7] + '  ' + ' | ' + '   ' +
          board[8] + '  ' + ' | ' + '   ' + board[9] + '  ')
    print('        |        |        ')
    print('--------------------------')
    print('        |        |        ')
    print('    ' + board[4] + '  ' + ' | ' + '   ' +
          board[5] + '  ' + ' | ' + '   ' + board[6] + '  ')
    print('        |        |        ')
    print('--------------------------')
    print('        |        |        ')
    print('    ' + board[1] + '  ' + ' | ' + '   ' +
          board[2] + '  ' + ' | ' + '   ' + board[3] + '  ')
    print('        |        |        ')
    print(end='\n')

# Function that prompts user to choose between "X" or "O"


def promptPlayerLetter():
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        letter = input('Choose between X or 0: ').upper()
    # The first element in the list returned is the player's letter while the other one is for the computer
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

# Function that determines who will make the first move


def makeFirstMove():
    if random.randint(0, 1) == 0:
        return 'Computer'
    else:
        return 'Player'

# Function that prompts player(user) to play again. Return True if yes, otherwise False


def replayGame():
    return input('Do you want to play again (y/n): ').lower().startswith('y')

# Function that simulates the game by generating the game board, process the letter chosen by the user, and the move to be made by either the player(user) or the computer


def makeMove(board, letter, move):
    board[move] = letter

# Function that determines whether the player(user) has won the game


def winGame(board, letter):
    # 1. Across the top
    # 2. Across the middled
    # 3. Across the bottom
    # 4. Down the left side
    # 5. Down the middle
    # 6. Down the right side
    # 7. Diagonal (1)
    # 8. Diagonal (2)
    return ((board[7] == letter and board[8] == letter and board[9] == letter) or (board[4] == letter and board[5] == letter and board[6] == letter) or (board[1] == letter and board[2] == letter and board[3] == letter) or (board[7] == letter and board[4] == letter and board[1] == letter) or (board[8] == letter and board[5] == letter and board[2] == letter) or (board[9] == letter and board[6] == letter and board[3] == letter) or (board[7] == letter and board[5] == letter and board[3] == letter) or (board[9] == letter and board[5] == letter and board[1] == letter))

# Function that duplicates the board after either the player(user) or the computer's turn


def copyBoard(board):
    duplicateBoard = []

    for x in board:
        duplicateBoard.append(x)
    return duplicateBoard

# Function that determines if the game board still has free blocks for any moves


def freeSpace(board, move):
    return board[move] == ' '

# Function that prompts the player(user) to make a move and that move is simulated


def playerMove(board):
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not freeSpace(board, int(move)):
        move = input('Your move (1-9): ')
    return int(move)

# Function that returns a valid move from the passed list on the game board or returns None if there is no more valid moves


def pickRandomMoveFromList(board, movesList):
    possibleMoves = []

    for i in movesList:
        if freeSpace(board, i):
            possibleMoves.append(i)
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

# Function that automates the computer's move in the game board


def computerMove(board, compLetter):
    if compLetter == 'X':
        playerLetter == 'O'
    else:
        playerLetter == 'X'

    # Algorithm of AI(Artificial Intelligence) for the game
    # It's first job is to determine if the player(user) can win after the next move
    for i in range(1, 10):
        copy = copyBoard(board)
        if freeSpace(copy, i):
            makeMove(copy, playerLetter, i)
            if winGame(copy, playerLetter):
                return i

    # Try to make a move from one of the corners(1, 3, 7, 9), if they are free
    move = pickRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center(5), if its free
    if freeSpace(board, 5):
        return 5

    # Make a move on one of the board's sides(2, 4, 6, 8)
    return pickRandomMoveFromList(board, [2, 4, 6, 8])

# Function that returns True if the space on the board has been taken. Otherwise return False


def boardFull(board):
    for x in range(1, 10):
        if freeSpace(board, x):
            return False
    return True


# Program Execution [Start Here]
while True:
    # Reset the board
    gameBoard = [' '] * 10
    playerLetter, compLetter = promptPlayerLetter()
    turn = makeFirstMove()
    print('The ' + turn + ' will go first')
    gameCommence = True

    while gameCommence:
        # Player's Turn
        if turn == 'Player':
            makeBoard(gameBoard)
            move = playerMove(gameBoard)
            makeMove(gameBoard, playerLetter, move)

            if winGame(gameBoard, playerLetter):
                makeBoard(gameBoard)
                print('Congratulations! You won the game!')
                gameCommence == False
            else:
                if boardFull(gameBoard):
                    makeBoard(gameBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'Computer'
        # Computer's Turn
        else:
            move = computerMove(gameBoard, compLetter)
            makeMove(gameBoard, compLetter, move)

            if winGame(gameBoard, compLetter):
                makeBoard(gameBoard)
                print('You Lose! The Computer has beaten you.')
                gameCommence = False
            else:
                if boardFull(gameBoard):
                    makeBoard(gameBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'Player'

    if not replayGame():
        break
