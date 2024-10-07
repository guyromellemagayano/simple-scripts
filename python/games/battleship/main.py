from battleship import (
    initialize_board, print_board, random_row, random_col, check_guess, mark_board,
    MAX_TURNS
)


def main():
    print("\nBattleship Game\n")
    print("Welcome to the Battleship Game! The goal of the game is to guess the exact coordinates (x, y) of a battleship in the battlefield so you can sink it. You have 4 tries to guess the correct coordinates.\n")
    print("Conditions\n")
    print("1. The battlefield is a 5x5 grid. Rows and columns are indexed from 0 to 4. Inputting coordinates outside this range will generate an error.")
    print("2. Inputting the same coordinates (rows x columns) twice will generate an error.")
    print("3. If you guess the correct coordinates, the game terminates immediately.\n")
    print("Let's play Battleship!\n")

    board = initialize_board()
    ship_row = random_row(board)
    ship_col = random_col(board)

    print_board(board)

    for turn in range(MAX_TURNS):
        try:
            print(f"\nTurn {turn + 1}")
            guess_row = int(input("Guess Row (0-4): "))
            guess_col = int(input("Guess Col (0-4): "))
        except ValueError:
            print("\nPlease enter valid integers.")
            continue

        result = check_guess(guess_row, guess_col, ship_row, ship_col, board)
        if result == "hit":
            print("\nCongratulations! You sunk my battleship!\n")
            break
        elif result == "out_of_bounds":
            print("\nOops, that's not even in the ocean.\n")
        elif result == "already_guessed":
            print("\nYou guessed that one already.")
        else:
            print("\nYou missed my battleship!\n")
            mark_board(board, guess_row, guess_col)                
            print_board(board)
    else:
        print("\nGame Over.\n")


if __name__ == "__main__":
    main()
