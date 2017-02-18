"""
A Simple Scrabble Game

v1.0

A simple function that accepts any single word(which contains either lowercase and uppercase letters) and counts the total number of equivalent points of the entire word 
"""

def scrabble_score(word):
    score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
         "x": 8, "z": 10}
    word_sum = 0
    
    for letter in word:
        for key in sorted(score):
            if letter.upper() in key or letter.lower() in key:
                word_sum += score[key]
                break
    return word_sum