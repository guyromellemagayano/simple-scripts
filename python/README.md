# Python scripts

The Python code is grouped by purpose. Run scripts from the repository root
with `python3`, followed by the script path.

## Games

Interactive games live in `games/`, with one directory per game:

- `battleship/`
- `deal_no_deal/`
- `dice-roll/`
- `flames/`
- `guess-that-number/`
- `guessing-game-one/`
- `hangman/`
- `magic-eight-ball/`
- `rock-paper-scissors/`
- `scrabble/`
- `sticks/`
- `tic-tac-toe/`

For example:

```sh
python3 python/games/guess-that-number/main.py
```

## Utilities

Task-focused and reusable scripts live in `utils/`:

- `date_parser.py` prints the current date and time.
- `password_generator.py` generates passwords with configurable constraints.
- `show_calendar.py` prints the current month's calendar.
- `temperature_conversion.py` prints a Fahrenheit-to-Celsius table.
- `whois_lookup.py` performs a WHOIS lookup and requires the `python-whois`
  package.

## Exercises

Learning exercises live in `exercises/` and are grouped by subject:

- `basics/` covers syntax, variables, classes, functions, lists, and data
  structures.
- `collections/` contains list filtering and deduplication exercises.
- `math/` contains arithmetic, number, sequence, and equation exercises.
- `patterns/` contains console shape and character-pattern exercises.
- `statistics/` contains grade and exam-statistics exercises.
- `text/` contains word-censoring and palindrome exercises.

## Tests

Run the automated test suite from the repository root:

```sh
python3 -m unittest discover -s python/tests -v
```

Alternatively, use the Makefile:

```sh
make -C python test
```
