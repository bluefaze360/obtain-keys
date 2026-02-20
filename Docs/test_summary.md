# Test Summaries

This doc outlines what tests I did, and how/why it failed/succeeded.

## Table of Contents
- [Obtain Keys CLI Integration Test 1](#obtain-keys-cli-test-1)
    - [Intended Changes](#intended-changes:)
    - [Result](#result)
- [Maze Runner 2D Test 1](#maze-runner-2d-test-1)
- [Leetspeak Test 1](#leetspeak-test-1)
- [GuessNum Test 1](#guessnum-test-1)
- [Hangman Test 1](#hangman-test-1)
    - [Intended Changes](#intended-changes-1)
    - [Result](#result-1)



## Obtain Keys CLI Test 1

Test Information:<br>
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_obtainkeys_1.png?raw=true)


Explanation: There is an empty list [''] inside the results list. Upon running the debugger for the Obtain Keys CLI, I noticed how the length of roomDescriptions was 19, but I only had 16 rooms. This is because when this function was reading the rooms.txt file, it had empty spaces (because I kinda emphasized readability), so it appended the empty lines as empty lists. This is where the test fails: pytest reads the empty list, which has a length of 1, and fails it because of the 
`
assert(len(record)) >= 2
`
line. 
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_obtainkeys_1_lists.png?raw=true)

### Intended Changes:

Remove extra spaces in rooms.txt file.

### Result:
100% Success!
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_obtainkeys_1_all_pass.png?raw=true)

## Maze Runner 2D Test 1

Test Information:<br>
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_mazeRunner2D_1_all_pass.png?raw=true)

## Leetspeak Test 1

Test Information:<br>
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_leetspeakTranslator_1_all_pass.png?raw=true)

## GuessNum Test 1

Test Information:<br>
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_guessnum_1_all_pass.png?raw=true)

## Hangman Test 1

Test Information:<br>
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_hangman_1.png?raw=true)

Explanation: Pretty self explanatory, but I think it's failing at 5 instead of 6

Here is the test that failed:<br>
```py
def test_game_needs_exactly_6_wrong_guesses_to_lose(self):
    """Game should be lost after 6 wrong guesses (max without drawing)."""
    # HANGMAN_PICS has 7 states, so 6 wrong guesses triggers loss
    # (index 6 is the final state)
    max_wrong_before_loss = len(hangman.HANGMAN_PICS) - 2
    assert max_wrong_before_loss == 6
```
Remember: the length of hangman pics is 7, but we are subtracting 2, so the max_wrong_before_loss is 5...
Only one of the pics displays when you didn't get a wrong answer, so subtracting two does not make sense.

### Intended Changes:
Change 2 to 1:
```py
def test_game_needs_exactly_6_wrong_guesses_to_lose(self):
    """Game should be lost after 6 wrong guesses (max without drawing)."""
    # HANGMAN_PICS has 7 states, so 6 wrong guesses triggers loss
    # (index 6 is the final state)
    max_wrong_before_loss = len(hangman.HANGMAN_PICS) - 1
    assert max_wrong_before_loss == 6
```

### Result:
100% Success!<br>
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_hangman_1_all_pass.png?raw=true)


