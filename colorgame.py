import sys

# creating the game board from input file
with open(sys.argv[1], "r") as my_file:
    matrix = [row.split() for row in my_file.readlines()]

score_dict = {"B": 9, "G": 8, "W": 7, "Y": 6, "R": 5, "P": 4, "O": 3, "D": 2, "F": 1, "X": 0} # weights of colors
score = 0

# print initial game board
for row in matrix:
    print(" ".join(row))
print(f"\nYour score is: {score}")


def find_neighbor(row, column):
    neighbor_list = []
    if initial_coordinate == "X":
        for number in range(-(len(matrix)-1), len(matrix)):
            new_row = row + number
            if (0 <= new_row <= (len(matrix) - 1)) and (new_row != row) and (matrix[new_row][column] != " "):
                # first expression is for edges of matrix since they cannot have 4 neighbors
                neighbor_list.append((new_row, column))

        for number in range(-(len(matrix[0])-1), len(matrix[0])):
            new_col = column + number
            if (0 <= new_col <= (len(matrix[0]) - 1)) and (new_col != column) and (matrix[row][new_col] != " "):
                neighbor_list.append((row, new_col))

    else:
        for number in range(-1, 2):  # range is different from "X" because this one includes only 4(or less) neighbors
            new_row = row + number
            if (0 <= new_row <= (len(matrix)-1)) and (new_row != row) and (matrix[new_row][column] != " "):
                neighbor_list.append((new_row, column))

        for number in range(-1, 2):
            new_col = column + number
            if (0 <= new_col <= (len(matrix[0])-1)) and (new_col != column) and (matrix[row][new_col] != " "):
                neighbor_list.append((row, new_col))

    return neighbor_list


def collect_balls(row, column):
    global score
    matrix[row][column] = " "
    for neighbor in find_neighbor(row, column):
        if initial_coordinate == "X":
            try:
                score += score_dict[matrix[neighbor[0]][neighbor[1]]]
            except KeyError:  # when we consider chain bombs, some of the neighbors might have been converted to " "
                pass
            if matrix[neighbor[0]][neighbor[1]] == initial_coordinate:
                matrix[neighbor[0]][neighbor[1]] = " "
                collect_balls(neighbor[0], neighbor[1])  # function will turn for every same neighbor
            else:
                matrix[neighbor[0]][neighbor[1]] = " "

        else:
            if matrix[neighbor[0]][neighbor[1]] == initial_coordinate:
                matrix[neighbor[0]][neighbor[1]] = " "
                score += score_dict[initial_coordinate]
                collect_balls(neighbor[0], neighbor[1])


def reshape_board():
    global matrix
    global score
    score += score_dict[initial_coordinate]  # only neighbors' scores have been added up to now, not chosen ball itself
    # move blanks up
    x = 0
    while x <= len(matrix):
        for rownum, j in enumerate(matrix):
            for colnum, element in enumerate(j):
                if element == " " and rownum - 1 >= 0:  # to prevent move from row (0) to row (-1) of the matrix
                    matrix[rownum][colnum], matrix[rownum - 1][colnum] = matrix[rownum - 1][colnum], matrix[rownum][colnum]
        x += 1

    # remove empty column
    column_list = list(map(list, zip(*matrix)))
    for column in range(len(column_list)-1, -1, -1):
        if "".join(column_list[column]) == " " * len(matrix):
            # if the column is empty, it will give empty string that has len(column) characters when we join that
            column_list.remove(column_list[column])

    # remove empty row
    matrix = list(map(list, zip(*column_list)))
    for row in range(len(matrix) - 1, -1, -1):
        if "".join(matrix[row]) == " " * len(matrix[0]):
            matrix.remove(matrix[row])


def game_over():
    if len(matrix) == 0:
        return True
    else:
        for row in range(len(matrix)):
            for column in range(len(matrix[0])):
                if matrix[row][column] == "X":
                    return False
                elif row + 1 < len(matrix) and matrix[row][column] != " ":
                    if matrix[row][column] == matrix[row + 1][column]:
                        return False
                elif column + 1 < len(matrix[0]) and matrix[row][column] != " ":
                    if matrix[row][column] == matrix[row][column + 1]:
                        return False
    return True

# if the game is not over, keep taking row and column as input 
while not game_over():
    try:
        row_column = list(map(int, (input("\nPlease enter a row and column number: ")).split()))
        initial_row, initial_column = row_column[0], row_column[1]
        initial_coordinate = (matrix[initial_row][initial_column])
        if initial_coordinate == " ":
            raise IndexError
        neighbor_check = [matrix[neighbor[0]][neighbor[1]] for neighbor in find_neighbor(initial_row, initial_column)]
        # find_neighbor() returns neighbors as indexes, we can check neighbors by converting index tuples to letters
        if initial_coordinate not in neighbor_check and initial_coordinate != "X":
            pass
        else:
            collect_balls(initial_row, initial_column)
            reshape_board()
    except IndexError:
        print("\nPlease enter a valid size!")
    else:
        if len(matrix) > 0:
            print()
            for line in matrix:
                print(" ".join(line))
            print(f"\nYour score is: {score}")

if game_over():
    print("\nGame over!")
