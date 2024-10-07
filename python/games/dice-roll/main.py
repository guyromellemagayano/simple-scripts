"""
Dice Rolling Simulator

A simple Python script that simulates a dice generating a number after it was rolled
"""

import random

def diceRoll():
    x = random.randrange(1, 7)

    # Prints result in a dice form
    if x == 1:
        print("*")
    elif x == 2:
        print("* *")
    elif x == 3:
        print("* * *")
    elif x == 4:
        print("*  *")
        print("*  *")
    elif x == 5:
        print("*   *")
        print("  *  ")
        print("*   *")
    else:
        print("* * *")
        print("* * *")

diceRoll()
