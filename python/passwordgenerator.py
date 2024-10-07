"""
Password Generator

This is a simple Python script that generates a random password whenever it is called. It has the following conditions:

1. It has a minimum length of at least 10 characters
2. It contains lower case letters coming from a pre-defined set 
3. It contains upper case letters coming from a pre-defined set
4. It contains alphanumeric numbers 
5. Has symbols set by a pre-defined list
"""

import string 
from random import *

def password_generator():
    # Characters
    letterchars = string.ascii_letters
    digitchars = string.digits
    puncchars = string.punctuation

    # Length
    minlength = 10
    maxlength = 20

    chars = letterchars + digitchars + puncchars
 
    for x in range(randint(minlength, maxlength)):
        x = choice(chars)
        print(x, end="")
    print(end="\n")

password_generator()


