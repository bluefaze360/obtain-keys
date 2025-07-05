"""
Lance Wilson
Prof. Lloyd
CSC 110
December 13, 2023

Game Title: Obtain the Minigame Keys
Objective:
"""
import os


# import games
import slidingTilePuzzle
import blindHangman
import hangman
import encryptedHangman
import guessNumSurvivalEdition
import guessnum
import mazeRunner2D
import mazeRunner3D

import sys
from time import sleep

roomDesc = mapInfo = objInfo = miniGames = currentRoom = ""
keyA = keyB = keyC = keyD = ""  # key initialization
torch = leet_to_eng_dict = defuser = maze_minimap = ""  # Initialization of unlock-able items
items = []
playerDead = gamePlayable = gameCompleted = miniGameCompleted = False
score = 0


def main():

    print("Initializing...")
    sleep(1.5)
    global roomDesc, mapInfo, objInfo, miniGames, currentRoom, keyA, keyB, keyC, keyD, torch, leet_to_eng_dict, defuser, maze_minimap

    roomDesc, mapInfo, objInfo, miniGames = readFiles()

    # Key declaration
    keyA = objInfo[2][0]
    keyB = objInfo[6][0]
    keyC = objInfo[11][0]
    keyD = objInfo[13][0]

    # manageInv(keyD) # testing that you can actually enter Room D4
    # Locked items declaration
    torch = objInfo[1][0]
    leet_to_eng_dict = objInfo[5][0]
    defuser = objInfo[10][0]
    maze_minimap = objInfo[12][0]

    currentRoom = "B1"

    mainMenu()


def mainMenu():
    global currentRoom, items, score
    key = ""
    beatGame = False
    # main game loop
    while key.upper() != "X":
        printActionChoices()
        key = input()
        # if key.upper() == "ADMIN":
        #     items.append(keyA)
        #     items.append(keyB)
        #     items.append(keyC)
        #     items.append(defuser) # These lines were to test if the items affected the code as intended.

        # Movement Bindings
        if key.upper() in ["W", "A", "S", "D"]:
            for relRooms in mapInfo:
                # Champion Room (D4)
                if relRooms[2] == currentRoom and relRooms[0] == "D4" and keyD not in items:
                    print(f"Cannot enter room until all keys have been unlocked. You are still in {currentRoom}.")
                    break
                elif relRooms[2] == currentRoom and relRooms[0] == "D4" and keyD in items and (not beatGame):
                    print(f"Welcome, my champion! You are done with this whole game! You can exit if you want...")
                    # if the player goes back to room D4, a different message should be played.
                    print(f"By the way, your score is: {score}")
                    beatGame = True
                    break
                elif relRooms[2] == currentRoom and relRooms[0] == "D4" and keyD in items and beatGame:
                    print(f"Welcome, back, my champion! You can exit if you want...")
                    print(f"By the way, your score is: {score}!")
                    break

                if relRooms[2] == currentRoom:  # Normal room movement
                    if key.upper() == "W" and relRooms[1] == "N":
                        currentRoom = relRooms[0]
                        print(f"Now in room {currentRoom}")
                        break
                    if key.upper() == "A" and relRooms[1] == "W":
                        currentRoom = relRooms[0]
                        print(f"Now in room {currentRoom}")
                        break
                    if key.upper() == "S" and relRooms[1] == "S":
                        currentRoom = relRooms[0]
                        print(f"Now in room {currentRoom}")
                        break
                    if key.upper() == "D" and relRooms[1] == "E":
                        currentRoom = relRooms[0]
                        print(f"Now in room {currentRoom}")
                        break

        # Other Action Bindings

        if key.upper() == "L":
            printRoomDesc()
            for objects in objInfo:
                if objects[1] == currentRoom and (objects[0] not in items):
                    equipItem = input(f"""You found a {objects[0]} in the room!
                Do you want to equip it? This may be important for your progression!
                [E] to equip item
                [Any] to not equip item
                """)
                    if equipItem.upper() == 'E':
                        print("Adding item to pouch...")
                        sleep(1)
                        if "(Unlocked)" in objects[0]:
                            print("Cannot pick up item. You need to beat the game in this room to unlock it!")
                        elif "(Achievement)" in objects[0]:
                            print("Cannot pick up item. You need to beat this game twice in this room to obtain the "
                                  "key!")
                        else:
                            print("Item added!")
                            manageInv(objects[0])

        if key.upper() == "R":
            print(f"\nYou are currently in Room {currentRoom}.")

        if key.upper() == "I":
            print("Items in pouch:")
            for i in items:
                print(f"- {i}")
            removeItem = input("Which item do you want to remove? ")
            if removeItem in items:  # CASE SENSITIVE!!
                removeButtonPressed = input("Are you sure you want to remove that item? \n Press [R] to remove: ")
                if removeButtonPressed.upper() == "R":
                    items.remove(removeItem)
                    print("Item removed")

        if key.upper() == "P":
            if gamePlayable:
                gameDispatcher()
            else:
                print("There isn't a game here. Explore the map to find games!")  # there will be someone who will
                # accidentally press the play button when there is no game.

    print()


def readFiles():
    return readRoomFile(), readMapFile(), readObjFile(), readGameFile()


def readRoomFile():
    roomDescriptions = []
    with open('TermProject/rooms.txt', 'r') as rooms:
        for room in rooms:
            roomDescriptions.append(room.rstrip("\n").split("|"))
    return roomDescriptions


def readMapFile():
    locDescriptions = []
    with open('TermProject/map_layout.txt', 'r') as map_layout:
        for loc in map_layout:
            locDescriptions.append(loc.rstrip("\n").split(","))

        for segments in locDescriptions:
            if segments == [""]:
                locDescriptions.remove(segments)

        for i in range(len(locDescriptions)):
            locDescriptions[i] = locDescriptions[i][0].split("|")

        for segments in locDescriptions:
            if segments == [""]:
                locDescriptions.remove(segments)

    return locDescriptions


def readObjFile():
    objectDescriptions = []
    with open('TermProject/objects.txt', 'r') as objects:
        for obj in objects:
            objectDescriptions.append(obj.rstrip("\n").split("|"))
    return objectDescriptions


def readGameFile():
    gameDescriptions = []
    with open('TermProject/games.txt', 'r') as games:
        for game in games:
            gameDescriptions.append(game.rstrip("\n").split("|"))
    return gameDescriptions


def gameDispatcher():
    global score
    for game in miniGames:
        if game[1] == currentRoom:

            # Games that are unlocked by default
            if game[0] == "Sliding Tile Puzzle":
                slidingTilePuzzle.main()
            elif game[0] == "Hangman":
                hangman.main()
            elif game[0] == "Guess The Number":
                guessnum.main()

            # Games that help complete the objectives
            elif game[1] == "A4":
                if "torch (Unlocked)" not in items:
                    blindHangman.main()
                    if blindHangman.bonus:
                        manageInv(keyA)
                        score += 35
                    elif (not blindHangman.bonus) and (not blindHangman.lostGame):
                        manageInv(torch)
                        score += 15
                    elif blindHangman.lostGame:
                        print("You lost! Press P to play again!")
                        score -= 2
                elif ("torch (Unlocked)" in items) or (keyA in items):
                    hangman.main()
                    if not hangman.lostGame:
                        manageInv(keyA)
                        score += 15
                    elif hangman.lostGame:
                        print("You lost! Press P to play again!")
                        score -= 1
            elif game[1] == "B3":
                if keyA in items:
                    if "dictionary (Unlocked)" not in items:
                        encryptedHangman.main()
                        if encryptedHangman.lostGame:
                            print("You lost! Press P to play again!")
                            score -= 4
                        else:
                            print("Nice deciphering skills! To ease your brain, I'm going to give you a dictionary!")
                            manageInv(leet_to_eng_dict)
                            score += 15
                    elif "dictionary (Unlocked)" in items:
                        print("Player has beaten Encrypted Hangman...")
                        sleep(1)
                        hangman.main()
                        if hangman.lostGame:
                            print("You lost! Press P to play again!")
                            score -= 4
                        else:
                            manageInv(keyB)
                            score += 15
                else:
                    print("You have to obtain key A in order to play games in this room!")
                    break
            elif game[1] == "C4":
                if keyB in items:
                    if "defuser (Unlocked)" not in items:
                        if "knife" in items:
                            guessNumSurvivalEdition.runGame(5)
                            if guessNumSurvivalEdition.score < 30:
                                print("You took too many explosions at once! You died!")
                                print("You lost! Press P to play again!")
                                score -= 10
                            elif guessNumSurvivalEdition.score >= 30:
                                print("You survived!")
                                manageInv(defuser)
                                score += 15
                        else:
                            guessNumSurvivalEdition.runGame(3)
                            if guessNumSurvivalEdition.score < 25:
                                print("You took too many explosions at once! You died!")
                                print("You lost! Press P to play again!")
                                score -= 10
                            elif guessNumSurvivalEdition.score >= 25:
                                print("You survived!")
                                manageInv(defuser)
                                score += 15
                    elif "defuser (Unlocked)" in items:
                        guessnum.main()
                        if guessnum.lostGame:
                            print("You lost! Press P to play again!")
                            score -= 10
                        else:
                            manageInv(keyC)
                            score += 15
                else:
                    print("You have to obtain key B in order to play games in this room!")
                    break
            elif game[1] == "D3":
                if keyC in items:
                    if "Minimap (Unlocked)" not in items:
                        mazeRunner3D.main()
                        if mazeRunner3D.gameFinished:
                            print("You made it out!")
                            manageInv("Minimap (Unlocked)")
                            score += 5
                        else:
                            print("So you got lost? Eh. Better luck next time.")
                            score -= 15
                    elif "Minimap (Unlocked)" in items:
                        mazeRunner2D.main()
                        if mazeRunner2D.gameFinished:
                            print("You made it out!")
                            manageInv(keyD)
                            score += 5
                        else:
                            print("So you couldn't get out? Eh. Better luck next time.")
                            score -= 15
                else:
                    print("You have to obtain key C in order to play games in this room!")
                    break


def printRoomDesc():
    for r_desc in roomDesc:
        if r_desc[0] == currentRoom:
            print(r_desc[1])


def printActionChoices():
    global gamePlayable
    print("""
[W] to go North
[S] to go South
[A] to go West
[D] to go East
[L] to look around the room
[I] to inspect/manage pouch contents
[R] to display current room""")
    for game in miniGames:
        if game[1] == currentRoom:
            if (objInfo[1][0] in items and objInfo[1][1] == currentRoom) or (
                    objInfo[5][0] in items and objInfo[5][1] == currentRoom):
                print(f'[P] to play "Hangman"')
                gamePlayable = True
                break
            elif objInfo[10][0] in items and objInfo[10][1] == currentRoom:
                print(f'[P] to play "Guess the Number"')
                gamePlayable = True
                break
            elif objInfo[12][0] in items and objInfo[12][1] == currentRoom:
                print(f'[P] to play "Maze Runner 2D"')
                gamePlayable = True
                break
            else:
                print(f'[P] to play "{game[0]}"')
                gamePlayable = True
                break
        else:
            gamePlayable = False
    print("""[X] to exit the game...""")


def manageInv(inventory_item):  # to make sure that each item isn't duplicated
    global items
    items.append(inventory_item)
    items = list(set(items))
    items.sort()  # because of set cast


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("That was sudden...")
    finally:
        print("Thanks for playing! Bye!")
        sys.exit(f"KeyboardInterrupt: y you exit the game?!?!")

"""
How did you approach this term project? Where did you get stuck, and how did you get unstuck?

One of the many places I got stuck was the Maze Runner programs, as they had functions I wasn't too familiar with. 
However, I found a way to manipulate the code so that it looked at the Mazes directory, and made so the maze runner 
programs were user-friendly.

How did you test your program? What doesn’t work as you’d like, perhaps things that you’d like to fix as you learn 
more? Write out at least 5 things that you tested. 

There were a lot of things that didn't work as intended throughout this program. 

1) When I edited this file on my MacBook, the open() wouldn't detect the .txt file (i.e. map_layout.txt) UNLESS I put 
the absolute path. For Windows, it doesn't matter as much.

2) I had to test if the [P] button played the game that the room was supposed to initialize, and if the game actually 
ran as intended.

3) I also had to test the games individually; to see if it actually worked or not. I would say this especially for 
"Encrypted Hangman", because I imported a leetspeak translator, and there were some instances that it outputted None 
(and after further testing, it was because I was trying to print a print function (the translate() function)).

4) After testing the games, I tested all the usable items. I first tested the keys, since those are essential for 
progression, and it took a while to configure it exactly. I then tested the unlockable items, like the torch, 
if they changed the game played. For the case of the torch, it would light up the hangman game, and the player would 
then see the letters.

5) Finally, I had to prevent duplication while enabling the user to pick up the items again after they dropped them, 
through the use of casting to a set, then casting back to a list, and then sorting the list.

What did you learn from this assignment? Do you feel this assignment is worth saving for your professional portfolio?

I learned about objectives while making a video game, and how to unlock certain missions with certain 
items/prerequisites. This project is worth saving on GitHub, and I will probably keep updating this game.
"""
