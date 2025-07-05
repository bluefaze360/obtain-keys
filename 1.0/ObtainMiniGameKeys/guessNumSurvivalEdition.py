"""Guess the Number Without Exploding, by Lance Wilson
Try to NOT guess the exploding number, but you get three chances.

Original by Al Sweigart.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: tiny, beginner, game"""

import random

score = 0


def runGame(live_count):
    global score
    lives = live_count
    try:
        number = int(input(f"""Please enter a number between 1 and 10, but be careful: if you choose the exploding number, the room explodes!
Enter your number: """))
    except ValueError:
        print("I said, enter a NUMBER!!")
        number = 0

    while lives > 0:
        explodingNumber = random.randint(1, 10)
        if 0 < number < 11:
            score += 1
        else:
            print("Number out of scope. You do not gain any points.")
        try:
            number = int(input(f"""\nPlease enter a number between 1 and 10, but be careful: if you choose the exploding number, the room explodes!
Enter your number: """))
        except ValueError:
            print("I said, enter a NUMBER!!")
        if number == explodingNumber:
            lives -= 1
            print(f"You chose the exploding number, and you lost a life! You have {lives} remaining lives.")

    print(f"You lost all your lives! Your score for this game is: {score}!")
