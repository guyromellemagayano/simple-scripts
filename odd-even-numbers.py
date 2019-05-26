"""
Odd Even Numbers

A simple Python script that determines odd and even numbers 
"""

# Part 1: Ask the user for the a number and print whether that number is an odd or even number
def oddEvenNumbers(num1, num2):
	if int(num1) % 2 == 0:
		print("\n" + "That number is even")

	# Check if divisible by 4
	if int(num1) % 4 == 0:
		print("The number is divisible by 4")

	else: 
		print("\n" + "That number is odd")

	# Check of num1 is divisible by num2 
	if int(num1) % int(num2) == 0:
		print("Both numbers are divisible by one another" + "\n")
	else:
		print("Both numbers are not divisible by one another" + "\n")

inputNum1 = input("Enter first number: ")
inputNum2 = input("Enter second number: ")

oddEvenNumbers(inputNum1, inputNum2)
