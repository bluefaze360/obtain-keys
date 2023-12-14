"""Leetspeak Translator by Lance Wilson
From the leetspeak code, this has been modified to be imported into other projects to translate a phrase to leetspeak.
To import this translator, use:

from leetspeakTranslator import translate

The translate method expects a parameter (phrase), which will just be any string.

Original leetspeak code by Al Sweigart: al@inventwithpython.com
Original code source: https://inventwithpython.com/bigbookpython/project40.html
"""


import random



def translate(phrase):
    print(englishToLeetspeak(phrase), end='')


def englishToLeetspeak(message):
    """Convert the English string in message and return leetspeak."""
    # Make sure all the keys in `charMapping` are lowercase.
    charMapping = {
        'a': ['4', '@', '/-\\'], 'c': ['('], 'd': ['|)'], 'e': ['3'],
        'f': ['ph'], 'h': [']-[', '|-|'], 'i': ['1', '!', '|'], 'k': [']<'],
        'o': ['0'], 's': ['$', '5'], 't': ['7', '+'], 'u': ['|_|'],
        'v': ['\\/']}
    leetspeak = ''
    for char in message:  # Check each character:
        # There is a 70% chance we change the character to leetspeak.
        if char.lower() in charMapping and random.random() <= 0.70:
            possibleLeetReplacements = charMapping[char.lower()]
            leetReplacement = random.choice(possibleLeetReplacements)
            leetspeak = leetspeak + leetReplacement
        else:
            # Don't translate this character:
            leetspeak = leetspeak + char
    return leetspeak


# translate("Ace Ace")