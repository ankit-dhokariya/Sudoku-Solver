from random import randint
from puzzle_generator import generator
from game import find_blank, check_validity


def checkGrid(grid):
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                return False

    # We have a complete grid!
    return True


def solveGrid(grid):
    global counter
    # Find next empty cell
    find = find_blank(grid)
    if find:
        row, col = find
        for value in range(1, 10):
            # Check that this value has not already be used on this row
            if check_validity(grid, value, (row, col)):
                grid[row][col] = value
                if checkGrid(grid):
                    counter += 1
                    break
                elif solveGrid(grid):
                    return True
            # break
    grid[row][col] = 0


board = generator(3)
print("Full Grid")
for i in board:
    print(i)
print()
attempts = 5
counter = 1
while attempts > 0:
    # Select a random cell that is not already empty
    row = randint(0, 8)
    col = randint(0, 8)
    while board[row][col] == 0:
        row = randint(0, 8)
        col = randint(0, 8)
    # Remember its cell value in case we need to put it back
    backup = board[row][col]
    board[row][col] = 0

    # Take a full copy of the grid
    copy = board
    # Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
    counter = 0
    solveGrid(copy)
    # If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
    if counter != 1:
        board[row][col] = backup
        # We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
        attempts -= 1

print("Grid")
for i in board:
    print(i)
