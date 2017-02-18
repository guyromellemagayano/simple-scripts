"""
Word Censor Script v1.0

Self-explanatory script that accepts any text and a word to be censored and returns the text with some words censored
"""

def censor(text, word):
    if word in text:
        text = text.replace(word,"*" * len(word))
        return text
