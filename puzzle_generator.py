from random import randint
from game import find_blank, check_validity

counter = 1


def checkGrid(grid):
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == 0:
                return False

    # We have a complete grid!
    return True


def solveGrid(grid):
    global counter

    find = find_blank(grid)
    if find:
        row, col = find
        for value in range(1, 10):
            if check_validity(grid, value, (row, col)):
                grid[row][col] = value
                if checkGrid(grid):
                    counter += 1
                    break
                elif solveGrid(grid):
                    return True

    grid[row][col] = 0


def generator(base):

    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    from random import sample

    def shuffle(s):
        return sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    return board


def puzzle(base):

    global counter
    board = generator(base)

    attempts = 5

    while attempts > 0:
        row = randint(0, 8)
        col = randint(0, 8)
        while board[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)

        backup = board[row][col]
        board[row][col] = 0

        copy = board

        counter = 0
        solveGrid(copy)

        if counter != 1:
            board[row][col] = backup
            attempts -= 1

    return board
