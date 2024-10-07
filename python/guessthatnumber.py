"""
Guess that Number [v1.0]

The Goal: Similar to the first project, this project also uses the random module in Python. The program will first randomly generate a number unknown to the user. The user needs to guess what that number is. (In other words, the user needs to be able to input information.) If the user’s guess is wrong, the program should return some sort of indication as to how wrong (e.g. The number is too high or too low). If the user guesses correctly, a positive indication should appear. You’ll need functions to check if the user input is an actual number, to see the difference between the inputted number and the randomly generated numbers, and to then compare the numbers.
"""

import random

def guessThatNumber():
	while True:
		try:
			number = int(input("Enter your desired number (1-10): "))
			generate_number = random.randrange(0, 10) 
		except ValueError:
			print(number, 'is not a number, try again.')
			continue
		if number > generate_number:
			print("Your chosen number is greater than the generated number!")
		elif number < generate_number:
			print("Your chosen number is less than than the generated number!")
		else:
			print("You got it fucking right!")

guessThatNumber()


