# Test Summaries

This doc outlines what tests I did, and how/why it failed/succeeded.

## Table of Contents
- [Obtain Keys CLI Integration Test 1](#obtain-keys-cli-test-1)
    - [Intended Changes](#intended-changes)
    - [Result](#result)



## Obtain Keys CLI Test 1

Test Information:<br>
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_obtainkeys_1.png?raw=true)


Explanation: There is an empty list [''] inside the results list. Upon running the debugger for the Obtain Keys CLI, I noticed how the length of roomDescriptions was 19, but I only had 16 rooms. This is because when this function was reading the rooms.txt file, it had empty spaces (because I kinda emphasized readability), so it appended the empty lines as empty lists. This is where the test fails: pytest reads the empty list, which has a length of 1, and fails it because of the 
`
assert(len(record)) >= 2
`
line. 
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_obtainkeys_1_lists.png?raw=true)

### Intended Changes

Remove extra spaces in rooms.txt file.

### Result:
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_obtainkeys_1_all_pass.png?raw=true)

## Maze Runner 2D (and 3D) Test 1

Test Information:<br>
![Here](https://github.com/bluefaze360/obtain-keys/blob/main/Images/TestImages/test_mazeRunner2D_1_all_pass.png?raw=true)
