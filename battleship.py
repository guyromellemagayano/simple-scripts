"""
Battleship Game

The goal of the game is to guess the exact coordinates(x, y) of a battleship in the battlefield so you could sunk it. You only have 4 tries to guess the correct coordinates. 

Conditions:
1. The size dimensions of the entire battlefield is abour 5 x 5 units. The program will only register rows and columns starting from 0 to 4. Above the given range will generate an error exception
2. Inputting the same coordinates(rows x columns) twice will generate an error exception
3. When you get the exact coordinates, the entire program terminates
"""

from random import randint

board = []

for x in range(5):
    board.append(["O"] * 5)

def print_board(board):
    for row in board:
        print(" ".join(row))

print("Let's play Battleship!")
print_board(board)

def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

ship_row = random_row(board)
ship_col = random_col(board)

# Simulate a pre-defined number of tries before ending the game
turn=[]
for turn in range(4):
    guess_row = int(input("Guess Row:"))
    guess_col = int(input("Guess Col:"))

    if guess_row == ship_row and guess_col == ship_col:
        print("Congratulations! You sunk my battleship!")
        break
    else:
        if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
            print("Oops, that's not even in the ocean.")
        elif(board[guess_row][guess_col] == "X"):
            print("You guessed that one already.")
        else:
            print("You missed my battleship!")
            board[guess_row][guess_col] = "X"
            # Print (turn + 1) here!
            print(turn+1)
            if turn == 3:
                print("Game Over")

        print_board(board)

    