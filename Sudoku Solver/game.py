def print_bo(bo):

    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("---------------------")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")

            if j == len(bo[0]) - 1:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

def find_blank(bo):

    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)

    return None

def check_validity(bo, num, pos):

    # Validity of num in Row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Validity of num in Column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Validity of num in box
    r = pos[0] // 3
    c = pos[1] // 3

    for i in range(r * 3, r * 3 + 3):
        for j in range(c * 3, c * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def solution(bo):

    find = find_blank(bo)

    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if check_validity(bo, i, (row, col)):
            bo[row][col] = i

            if solution(bo):
                return True

            bo[row][col] = 0

    return False
