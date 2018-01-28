"""
Grading System

A simple Python script that records grades of students and it will determine the rating and average of all students together
"""

lloyd = {
	"name": "Lloyd",
	"homework": [90.0, 97.0, 75.0, 92.0],
	"quizzes": [88.0, 40.0, 94.0],
	"tests": [75.0, 90.0]
}
alice = {
	"name": "Alice",
	"homework": [100.0, 92.0, 98.0, 100.0],
	"quizzes": [82.0, 83.0, 91.0],
	"tests": [89.0, 97.0]
}
tyler = {
	"name": "Tyler",
	"homework": [0.0, 87.0, 75.0, 22.0],
	"quizzes": [0.0, 75.0, 78.0],
	"tests": [100.0, 100.0]
}

students = [lloyd,alice,tyler]

def average(students):
	s = sum(students)
	return float(s) / len(students)

def get_average(student):
	whomework = 0
	wquizzes = 0
	wtests = 0
	whomework = whomework + average(student["homework"]) * 0.1
	wquizzes = wquizzes + average(student["quizzes"]) * 0.3
	wtests = wtests + average(student["tests"]) * 0.6
	return whomework + wquizzes + wtests

def getlettergrade(score):
	if score <60:
		return "F"
	elif score <70:
		return "D"
	elif score <80:
		return "C"
	elif score <90:
		return "B"
	else:
		return "A"

def getclassaverage(students):
	lst = [lloyd,alice,tyler]
	s = len(lst)
	aver = get_average(lloyd) + get_average(alice) + get_average(tyler)
	final = aver/s
	return final

print("Average students' grade:", getclassaverage(students))
print("Rating:", getlettergrade(getclassaverage(students)))