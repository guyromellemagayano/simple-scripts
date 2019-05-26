"""
Make a two-player Rock-Paper-Scissors game. (Hint: Ask for player plays (using input), compare them, print out a message of congratulations to the winner, and ask if the players want to start a new game)
"""

import random

def rockPaperScissors():
	user_input = input("Select from Rock, Paper, Scissors: ")
	computer_input = random.choice(['Rock', 'Paper', 'Scissors'])

	print( "Computer selects " + computer_input )

	if( user_input == "rock" or user_input == "Rock" ):
		if( computer_input == "Paper" ):
			print( "Paper wins over rock." )
		elif( computer_input == "Rock" ):
			print( "Rock over rock? No one wins. Obviously." )
		elif( computer_input == "Scissors" ):
			print( "Rock wins over scissors" )
	elif( user_input == "paper" or user_input == "Paper" ):
		if( computer_input == "Paper" ):
			print( "Paper over paper? No one wins. Obviously." )
		elif( computer_input == "Rock" ):
			print( "Paper wins over rock." )
		elif( computer_input == "Scissors" ):
			print( "Scissors wins over paper" )
	elif( user_input == "scissors" or user_input == 'Scissors' ):
		if( computer_input == "Paper" ):
			print( "Scissors wins over paper." )
		elif( computer_input == "Rock" ):
			print( "Rock wins over scissors." )
		elif( computer_input == "Scissors" ):
			print( "Scissors over scissors? No one wins. Obviously." )
	else:
		print( "Invalid input. Please try to input the correct word." )

rockPaperScissors();
