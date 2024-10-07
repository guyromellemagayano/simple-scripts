from random import randint

BOARD_SIZE = 5
MAX_TURNS = 4


def initialize_board(size=BOARD_SIZE):
    """Initialize the game board with the given size."""
    return [["O"] * size for _ in range(size)]


def print_board(board):
    """Print the game board."""
    for row in board:
        print(" ".join(row))


def random_row(board):
    """Generate a random row index within the board."""
    return randint(0, len(board) - 1)


def random_col(board):
    """Generate a random column index within the board."""
    return randint(0, len(board[0]) - 1)


def check_guess(guess_row, guess_col, ship_row, ship_col, board):
    """
    Check the player's guess against the ship's position and the game board state.

    Returns:
        "hit" if the guess is correct,
        "out_of_bounds" if the guess is outside the board,
        "already_guessed" if the position has been guessed before,
        "miss" otherwise.
    """
    if guess_row == ship_row and guess_col == ship_col:
        return "hit"
    elif guess_row < 0 or guess_row >= len(board) or guess_col < 0 or guess_col >= len(board[0]):
        return "out_of_bounds"
    elif board[guess_row][guess_col] == "X":
        return "already_guessed"
    else:
        return "miss"


def mark_board(board, guess_row, guess_col):
    """Mark the guessed position on the board."""
    board[guess_row][guess_col] = "X"
