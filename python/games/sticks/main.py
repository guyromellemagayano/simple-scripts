import random
sticks = 21

print("There are 21 sticks, you can take 1-4 sticks at a time.\n Whoever will take the last stick will lose")

while True:
	print("Sticks left: ", sticks)
	sticks_taken = int(input("You took? (1-4): "))
	if sticks == 1:
		print("You took the last stick. You lose")
		break
	if sticks_taken >= 5 or sticks_taken <= 0:
		print("Wrong input!")
		continue
	print("Computer took: ", random.randint(1, 4), "\n")
	sticks -= 4
