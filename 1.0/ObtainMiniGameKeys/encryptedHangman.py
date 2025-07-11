"""Encrypted Hangman, by Lance Wilson
Original Hangman by Al Sweigart al@inventwithpython.com
Guess the letters to a secret word before the hangman is drawn, but the letters are displayed in leetspeak.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, word, puzzle"""

# The original "Hangman" is featured in the book "Invent Your Own
# Computer Games with Python" https://nostarch.com/inventwithpython

import random

from leetspeakTranslator import translate

HANGMAN_PICS = [r"""
 +--+
 |  |
    |
    |
    |
    |
=====""",
                r"""
 +--+
 |  |
 O  |
    |
    |
    |
=====""",
                r"""
 +--+
 |  |
 O  |
 |  |
    |
    |
=====""",
                r"""
 +--+
 |  |
 O  |
/|  |
    |
    |
=====""",
                r"""
 +--+
 |  |
 O  |
/|\ |
    |
    |
=====""",
                r"""
 +--+
 |  |
 O  |
/|\ |
/   |
    |
=====""",
                r"""
 +--+
 |  |
 O  |
/|\ |
/ \ |
    |
====="""]

# (!) Try replacing CATEGORY and WORDS with new strings.
CATEGORY = 'Animals'
WORDS = 'ANT BABOON BADGER BAT BEAR BEAVER CAMEL CAT CLAM COBRA COUGAR COYOTE CROW DEER DOG DONKEY DUCK EAGLE FERRET FOX FROG GOAT GOOSE HAWK LION LIZARD LLAMA MOLE MONKEY MOOSE MOUSE MULE NEWT OTTER OWL PANDA PARROT PIGEON PYTHON RABBIT RAM RAT RAVEN RHINO SALMON SEAL SHARK SHEEP SKUNK SLOTH SNAKE SPIDER STORK SWAN TIGER TOAD TROUT TURKEY TURTLE WEASEL WHALE WOLF WOMBAT ZEBRA'.split()
lostGame = False


def main():
    global lostGame
    lostGame = False
    print('Hangman, by Al Sweigart al@inventwithpython.com')

    # Setup variables for a new game:
    missedLetters = []  # List of incorrect letter guesses.
    correctLetters = []  # List of correct letter guesses.
    secretWord = random.choice(WORDS)  # The word the player must guess.

    while True:  # Main game loop.
        drawHangman(missedLetters, correctLetters, secretWord)

        # Let the player enter their letter guess:
        guess = getPlayerGuess(missedLetters + correctLetters)

        if guess in secretWord:
            # Add the correct guess to correctLetters:
            correctLetters.append(guess)

            # Check if the player has won:
            foundAllLetters = True  # Start off assuming they've won.
            for secretWordLetter in secretWord:
                if secretWordLetter not in correctLetters:
                    # There's a letter in the secret word that isn't
                    # yet in correctLetters, so the player hasn't won:
                    foundAllLetters = False
                    break
            if foundAllLetters:
                print('Yes! The secret word is:', secretWord)
                print('You have won!')
                break  # Break out of the main game loop.
        else:
            # The player has guessed incorrectly:
            missedLetters.append(guess)

            # Check if player has guessed too many times and lost. (The
            # "- 1" is because we don't count the empty gallows in
            # HANGMAN_PICS.)
            if len(missedLetters) == len(HANGMAN_PICS) - 1:
                drawHangman(missedLetters, correctLetters, secretWord)
                print('You have run out of guesses!')
                print('The word was "{}"'.format(secretWord))
                lostGame = True
                break


def drawHangman(missedLetters, correctLetters, secretWord):
    """Draw the current state of the hangman, along with the missed and
    correctly-guessed letters of the secret word."""
    print(HANGMAN_PICS[len(missedLetters)])
    print('The category is:', CATEGORY)
    print()

    # Show the incorrectly guessed letters in leetspeak:
    print('Missed letters: ', end='')
    for letter in missedLetters:
        translate(letter)
    if len(missedLetters) == 0:
        print('No missed letters yet.')
    print()

    # Display the blanks for the secret word (one blank per letter):
    blanks = ['_'] * len(secretWord)

    # Replace blanks with correctly guessed leet letters:
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks[i] = secretWord[i]
    # Show the secret word with spaces in between each letter, however, the letters are changed to leetspeak:
    translate(' '.join(blanks))


def getPlayerGuess(alreadyGuessed):
    """Returns the letter the player entered. This function makes sure
    the player entered a single letter they haven't guessed before."""
    while True:  # Keep asking until the player enters a valid letter.
        print(f'\nGuess a letter.')
        guess = input('> ').upper()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif not guess.isalpha():
            print('Please enter a LETTER.')
        else:
            return guess


# If this program was run (instead of imported), run the game: