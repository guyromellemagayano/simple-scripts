"""
Generate a random number between 1 and 9 (including 1 and 9). Ask the user to guess the number, then tell them whether they guessed too low, too high, or exactly right. (Hint: remember to use the user input lessons from the very first exercise)

Extras:

Keep the game going until the user types “exit”
Keep track of how many guesses the user has taken, and when the game ends, print this out.
"""

from random import randint

def guessingGameOne():
	user_prompt = 0
	user_tries = 0;
	guess_number = randint(1,9)

	while user_prompt != guess_number and user_prompt != "exit":
		user_prompt = input('Guess the number (1,9). Type "exit" to end program: ')
		user_tries += 1

		if user_prompt == "exit":
			break
		else: 
			if int(user_prompt) == guess_number:
				print( "You got it right after", user_tries, "tries" )
			elif int(user_prompt) > guess_number:
				print( "Higher!" )
			elif int(user_prompt) < guess_number:
				print( "Lower!" )
			else:
				print( "Out of range" )

guessingGameOne()