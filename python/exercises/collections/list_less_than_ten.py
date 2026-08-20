"""
List Less Than Ten

Write a program to list all numbers from 1 to 10 with the following conditions:
1. Instead of printing the elements one by one, make a new list that has all the elements and print out a new list
2. Write this in one line
3. Ask the user for a number and return a list that contains only elements from the original list that are smaller than that number given by the user
"""

# Condtion 1
numList = [1,2,3,4,5,6,7,8,9,10]
for x in numList:
	print(x, end=" ")
print("\n")

# Condition 2
print([x for x in numList])
print("\n")

# Condition 3 
def countNumList(num):
	for x in range(1, num+1):
		print(x)

countNumList(int(input("Enter a limit: ")))