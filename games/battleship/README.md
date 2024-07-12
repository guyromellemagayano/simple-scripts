# Battleship Game

Welcome to the Battleship Game! The goal of the game is to guess the exact coordinates (x, y) of a battleship in the battlefield so you can sink it. You have 4 tries to guess the correct coordinates.

## Conditions

1. The battlefield is a 5x5 grid. Rows and columns are indexed from 0 to 4. Inputting coordinates outside this range will generate an error.
2. Inputting the same coordinates (rows x columns) twice will generate an error.
3. If you guess the correct coordinates, the game terminates immediately.

## How to Play

1. Run the game using Python:

    ```sh
    python main.py
    ```

    > Or use the `make run-battleship-game` command in the root folder to run this program without navigating through the code.

2. Follow the prompts to input your guesses for the row and column.

## Possible Moves and Errors

### Guessing Out of Bounds

If you input coordinates outside the range 0-4 for either the row or column, you will see an error message: "Oops, that's not even in the ocean."

### Guessing the Same Coordinates Twice

If you guess the same coordinates (row x column) more than once, you will see an error message: "You guessed that one already."

### Hitting the Battleship
  
If you guess the correct coordinates where the battleship is located, you will see the message: "Congratulations! You sunk my battleship!" and the game will terminate.

### Missing the Battleship

If you guess the coordinates that do not match the battleship's location, you will see the message: "You missed my battleship!" and your guess will be marked on the board with an "X".
