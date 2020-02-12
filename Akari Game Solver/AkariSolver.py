# a CSP solution approach to AKARI problems by Ozgun Ozerk

from constraint import *


row = int(input("Please enter row size: "))  # how many rows
col = int(input("Please enter column size: "))  # how many columns

text = input("Please enter the game board as a single line: ")  # W for white boxes, B for empty black boxes, Number(0,1,2,3 or 4) for black boxes with number
matrix = []
for i in range(0, row+2):
    matrix.append([])  # creating an empty row
    for j in range(0,col+2):
        matrix[i].append('X')  # encapsulating the board with black boxes to avoid getting out of range for indexing errors

for i in range(1,row+1):  # constructing the matrix
    for j in range(1,col+1):
        matrix[i][j] = text[(i-1)*col + (j-1)]  # assigning the input values into the matrix

print("\n\nAKARI GAME TO SOLVE:")
print("W/ white box,   B/ Black box with no number,    (0,1,2,3,4)/ black box with number")
print("--------------------------")
for i in range(1, row+1):  # printing the initial matrix
    print(matrix[i][1:col+1])
print("--------------------------\n\n")


problem = Problem()  # CSP problem initialization

counter = 0  # for controlling which boxes are white
# print("White box indices are:")  # for debugging
for i in range(1,row+1):  # iterating throughout the matrix for determining which boxes are white
    for j in range(1,col+1):

        if matrix[i][j] == 'W':  # if current box is white
            # print(counter)  # printing the number of it  # for debugging
            problem.addVariable(counter, [0,1])  # adding the variable with the domain to the problem; domain: 0 means no light, 1 means light
        counter += 1
# print("White box indices end \n ---------------- \n")  # for debugging


for i in range(1, row+1):  # iterating throughout the matrix again, this time for solving the problem
    for j in range(1, col+1):

        if matrix[i][j] == 'W':  # if current box is white
            leftBoundary = 0  # setting boundary limit for left, right, upper and lower respectively
            rightBoundary = 0
            upperBoundary = 0
            lowerBoundary = 0

            i1 = i  # temp variables for checking the boundaries
            j1 = j
            i2 = i
            j2 = j
            i3 = i
            j3 = j
            i4 = i
            j4 = j

            while matrix[i1][j1] == 'W':  # while loops check to the left until it encounters a non-white box
                j1 = j1-1
            leftBoundary = j1  # storing the boundary limit

            while matrix[i2][j2] == 'W':  # while loops check to the right until it encounters a non-white box
                j2 = j2+1
            rightBoundary = j2  # storing the boundary limit

            while matrix[i3][j3] == 'W':  # while loops check upwards until it encounters a non-white box
                i3 = i3-1
            upperBoundary = i3  # storing the boundary limit

            while matrix[i4][j4] == 'W':  # while loops check downwards until it encounters a non-white box
                i4 = i4+1
            lowerBoundary = i4  # storing the boundary limit

            vertical_set = set(list(range(col * (i-1) + leftBoundary, col * (i-1) + rightBoundary - 1)))  # creating a set for vertical white neighbourhoods
            horizontal_set = set(list(range(col * upperBoundary + (j-1), (lowerBoundary-2) * col + j, col)))  # creating a set for horizontal white neighbourhoods
            union_set = vertical_set.union(horizontal_set)  # creating a union set of vertical and horizontal

            # for debugging
            # print("white box:", i, j)  # printing the current white box index
            # print("vertical list:", vertical_set)  # printing these sets
            # print("horizontal list:", horizontal_set)
            # print("union set:", union_set)

            problem.addConstraint(MaxSumConstraint(1), list(vertical_set))  # there cannot be more than 1 lightbulb in each vertical set, (turning it into list since sets are not iterable
            problem.addConstraint(MaxSumConstraint(1), list(horizontal_set))  # same for the horizontal set
            problem.addConstraint(MinSumConstraint(1), list(union_set))  # there should be at least 1 lightbulb for each white box in its horizontal or vertical neighbourhoods

        if matrix[i][j] != 'W' and matrix[i][j] != 'B':  # if the current box not a empty black or white one
            if int(matrix[i][j]) >= 0 and int(matrix[i][j]) <= 4:  # meaning we have a black box with a number (this control is unnecessary but better to be safe in case of wrong inputs)
                adjacent = []  # creating an empty list for storing the adjacent white boxes
                if matrix[i][j-1] == 'W':  # checking the left adjacent box is white
                    adjacent.append((i-1)*col + j-2)
                if matrix [i][j+1] == 'W':  # checking the right adjacent box is white
                    adjacent.append((i-1)*col + j)
                if matrix [i-1][j] == 'W':  # checking the upper adjacent box is white
                    adjacent.append((i-2)*col + j-1)
                if matrix [i+1][j] == 'W':  # checking the lower adjacent box is white
                    adjacent.append(i*col + j-1)

                # print("black box:", matrix[i][j], "adjacents:", adjacent)  # printing the adjacent list  # for debugging
                problem.addConstraint(ExactSumConstraint(int(matrix[i][j])), adjacent)  # adjacent lightbulb amount should match with the black box's number


result = problem.getSolutions()
# print(result)  #  printing all the solutions

print("\n\nTHE SOLUTION")
print("L/ light bulb,   W/ no light bulb,   B/ Black box with no number,    (0,1,2,3,4)/ black box with number")
print("--------------------------")


counter = 0  # counter for white box control
for i in range(1, row+1):  # iterating throughout the matrix again, this time for visualizing the solution
    for j in range(1, col+1):
        if matrix[i][j] == 'W':
            if result[0].get(counter) == 1:  # result[0] returning the first solution dictionary
                matrix[i][j] = 'L'
        counter += 1

for i in range(1, row+1):  # printing the final matrix solution
    print(matrix[i][1:col+1])

print("--------------------------")
print("END OF THE SOLUTION")

# input for easy: WWBWW2W3WWWWWWWWWWWW1WWWWWWW1WWWWWWWWWWWWBW1WW1WW
# input for medium: W2WWWWWWW2W1WBWBWWWBWWWWWWWWW2WWW2W1WBW2WWWWWWW3W
# input for hard: WWBWWWWWWW3WWWWWWBWWBW1BBB1W2WW0WWWWWWBWWWWWWW2WW
# TESTED ON: [https://www.puzzle-light-up.com/]
