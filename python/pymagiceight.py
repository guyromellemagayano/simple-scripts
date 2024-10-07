import random

question = input('Ask the magic 8 ball a question (Press enter to start): ')
answers = [
	"You are awesome",
	"You suck at anything you do", 
	"Keep up the good work",
	"You're immoral",
	"You're not normal anymore",
	"No one loves you anymore",
	"So many pretentious people",
	"You rock",
	"You're awesome",
	"You're important to other people"
]
print(answers[random.randint(1, len(answers))])	