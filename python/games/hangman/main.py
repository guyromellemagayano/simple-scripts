#!/usr/bin/env python3
import random

# Initialization
word = [
	"secret",
	"hidden",
	"television"
]
guesses = ''
turns = 10
select_word = word[random.randint(0, len(word)-1)]

while turns > 0:
	fail = 0

	for char in select_word:
		if char in guesses:
			print(char, end=" ")
		else:
			print("_", end=" ")
			fail += 1

	if fail == 0:
		print("\n")
		print("You Won!")
		break

	print("\n")

	guess = input("Guess a character: ")

	guesses += guess

	if guess not in select_word:
		turns -= 1

		print("\n")

		print(f"Wrong character. You only have {turns} turns left")

		if turns == 0:
			print("\n")
			print("You lose")
