#!/usr/bin/env python3
import sys


class Flames:

	def main(self):
		self.__init__()

	def __init__(self):
		self.text = list("FLAMES")
		self.tries = 0
		self.menu()

	def menu(self):
		print(end="\n")
		print("PLAY FLAMES", end="\n\n")
		self.a = input ("Start the game (Y/N): ")
		self.check(self.a)

	def check(self, a1):
		if(str.isalpha(a1) == True):
			self.startup(a1)
		else:
			print("\n\n")
			print("Enter valid character")
			self.menu()

	def startup(self, a2):
		if(self.tries != 3):
			if(a2 == 'Y' or a2 == 'y'):
				self.flame()
			elif(a2 == 'N' or a2 == 'n'):
				sys.exit()
			else:
				print("\n\n")
				print("Enter valid input")
				self.tries = self.tries+1
				self.menu()
		else:
			print("\n\n")
			print("What the fuck?!")
			sys.exit()

	def flame(self):
		print(end="\n")
		self.n1 = input("Enter the first name: ")
		self.n1 = self.n1.strip()
		self.n1 = str.lower(self.n1)

		self.n2 = input("Enter the second name: ")
		self.n2	= self.n2.strip()
		self.n2 = str.lower(self.n2)

		if(set(r"`~1!2@3#4$5%6^7&8*9(0)-_=+[{]}\|;:',<.>/?+-*/.").intersection(self.n1) or set(r"`~1!2@3#4$5%6^7&8*9(0)-_=+[{]}\|;:',<.>/?+-*/.").intersection(self.n2)):
			print("Invalid name. Try to enter a valid name.")
			self.flame()

		self.n1_list = list(self.n1)
		self.n2_list = list(self.n2)

		n1_list = len(self.n1_list)
		n2_list = len(self.n2_list)

		self.lencalc(n1_list, n2_list)
		print(end="\n")
		self.result()
		print(end="\n")

	def lencalc(self, n1_list, n2_list):
		for i in range(n1_list):
			for j in range(n2_list):
				try:
					if(self.n1_list[i] == self.n2_list[j]):
						self.n1_list.remove(self.n1_list[i])
						self.n2_list.remove(self.n2_list[j])
					else:
						continue
				except IndexError:
					n1_list = n1_list - 1
					n2_list = n2_list - 1
					self.lencalc(n1_list, n2_list)
				finally:
					self.totallen = len(self.n1_list) + len(self.n2_list)
		self.flgame(self.totallen)

	def flgame(self, clen):
		clen = self.totallen
		check = clen % len(self.text)
		if((check == 0) or (check > clen)):
			clen = len(self.text)
		else:
			clen = check
		for i in range(clen):
			ivalue = i
		self.flcalc(ivalue, clen)

	def flcalc(self, ivalue1, clen1):
		while(len(self.text) != 1):
			try:
				from collections import deque
				text1 = deque(self.text)
				text1.remove(text1[ivalue1])
				text1.rotate(len(text1) - ivalue1)
				self.text = list(text1)
				self.flgame(clen1)
			except IndexError:
				from collections import deque
				pseudo = (clen1 - 1) - len(self.text)
				self.text.pop(pseudo)
				text1 = deque(self.text)
				text1.rotate(len(text1) - pseudo)
				self.text = list(text1)
				self.flgame(clen1)

	def result(self):
		for i in range(1):
			if(self.text[0]=='F'):
				print(f'{self.n1} and {self.n2} are FRIENDS')
			elif(self.text[0]=='L'):
				print(f'{self.n1} and {self.n2} are LOVERS')
			elif(self.text[0]=='A'):
				print(f'{self.n1} and {self.n2} are AFFECTIONIATE WITH EACH OTHER')
			elif(self.text[0]=='M'):
				print(f'{self.n1} and {self.n2} are MARRIED or WEDDINGS BELLS ARE RINGING')
			elif(self.text[0]=='E'):
				print(f'{self.n1} and {self.n2} are ENEMIES')
			else:
				print(f'{self.n1} and {self.n2} are SIBLINGS')

Flames()
