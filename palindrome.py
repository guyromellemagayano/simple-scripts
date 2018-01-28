def palindrome(text):
	reverse_text = text[::-1]
	if text == reverse_text:
		print("It is a palindrome")
	else:
		print("Its not a fucking palindrome")

word = input("Enter a word: ")
palindrome(word)