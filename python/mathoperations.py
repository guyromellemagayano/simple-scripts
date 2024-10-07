"""
This module contains the functions for the math operations: addition, subtraction, multiplication, and division.
"""
def math_operations():
  print("\nMath Operations\n")
  print("1. Addition")
  print("2. Subtraction")
  print("3. Multiplication")
  print("4. Division")
  print("5. Exit")
  choice = int(input("\nEnter your choice (1-5): "))

  num1 = int(input("\nEnter first number: "))
  num2 = int(input("Enter second number: "))

  # Input validation
  while choice < 1 or choice > 5:
    print("Invalid choice. Please enter a number between 1 and 5.")
    choice = int(input("\nEnter your choice (1-5): "))

  # Choice selection and output
  if choice == 1:
    sum = num1 + num2
    print("\nSum =", sum)
  elif choice == 2:
    difference = num1 - num2
    print("\nDifference =", difference)
  elif choice == 3:
    product = num1 * num2
    print("\nProduct =", product)
  elif choice == 4:
    if num2 == 0:
      print("\nCannot divide by zero.")
    else:
      quotient = num1 / num2
      print("\nQuotient =", quotient)
  elif choice == 5:
    exit()
  else:
    print("\nInvalid choice")

math_operations()
