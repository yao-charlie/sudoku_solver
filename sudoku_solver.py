import logging

# log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

# A Sudoku puzzle is effectively a solution to three sets: 9 rows, 9 columns and 9 3x3 blocks.
# Each must satisfy the condition that only one element exists from numbers 1-9.
# A puzzle is proposed when some elements are populated in the grid, to form existing constraints on the rest of board.
# (N.B. fewer constraints typically mean a harder puzzle, assuming it is solvable)
# Typically, unfilled elements are present but our purposes, we'll assign these to '0' to easily test for this condition.

# Solution below is not necessarily formatted in typical distribution detail but attempts to demonstrate the steps
# in which to solve it.

# The data structure we can use to define a Sudoku grid is a 2-degree list: sudoku = [i][j], with i, j being max 9 (8).

# A random sample sudoku puzzle from websudoku:

sudoku_puzzle = [[2, 6, 0, 9, 0, 0, 0, 8, 0],
                 [0, 0, 3, 7, 1, 0, 0, 0, 0],
                 [0, 0, 7, 4, 0, 8, 0, 0, 0],
                 [0, 9, 4, 0, 8, 0, 3, 0, 0],
                 [1, 7, 6, 0, 5, 0, 2, 9, 8],
                 [0, 0, 8, 0, 9, 0, 4, 1, 0],
                 [0, 0, 0, 5, 0, 1, 6, 0, 0],
                 [0, 0, 0, 0, 7, 3, 5, 0, 0],
                 [0, 4, 0, 0, 0, 9, 0, 3, 1]
                 ]


# The function structure to go over each element is as follows:
def sudoku_printer(puzzle):
    for row in range(len(puzzle)):
        print()  # used to add en endline
        for column in range(len(puzzle[row])):
            print(puzzle[row][column], end=' ')  # end used to not print the end line command
    print()  # final end line


# This function only prints but the structure can be used for the iterative check
# TODO: change this to a decorator? Review after defining the solver


# We define three functions to test the constraints.

# Function 1: test row. Pass in the puzzle and a candidate, check to see if the candidate is in the row. Return false is
# the element is in the row, violating the constraint.
# Not too difficult given the 'in' method for lists.

def row_constraint(puzzle, candidate, row):
    # for the i'th row, check if the element is in the row.

    # if candidate in puzzle[row]:
    #     return False
    # else:
    #     return True

    # Expressed as a one-liner:

    return False if candidate in puzzle[row] else True


# Function 2: test column. Pass in the puzzle and a candidate, check to see if the candidate is in the column. Return
# false is the element is in the column, violating the constraint.
# Additional complexity as you cannot natively use the 'in' method, you must check the column element in the specified
# row.

def column_constraint(puzzle, candidate, column):
    for row in range(len(puzzle)):

        logging.debug("{a}".format(a=puzzle[row][column]))

        if candidate == puzzle[row][column]:
            logging.debug("Constraint is False. Return.")
            return False

    logging.debug("Constraint is True. Return.")
    return True


# N.B. Alternatively - we could import numpy, transpose the matrix and then use 'in' method or possibly other methods.
# Or manually transpose. Complexity trade off.


# Function 3: text blocks. Pass in the puzzle and a candidate, check to see if the candidate is in the 3x3 box it
# belongs to. Return false is the element is in the box, violating the constraint.
# This is complicated as we must first identify the block the element is associate with. There are probably multiple
# ways of doing this. Note that compared to rows/columns, this is less of a generalized function as we will exploit
# the structure of the Sudoku puzzle. We'll use floor division to figure out which block we're in and iterate over the
# block.

def block_constraint(puzzle, candidate, row, column):
    block_row = row // 3
    logging.debug("Block Row is {a}".format(a=block_row))
    column_row = column // 3
    logging.debug("Column Row is {a}".format(a=column_row))

    for i in range(3):
        for j in range(3):
            logging.debug("{a}".format(a=puzzle[block_row*3 + i][column_row*3 + j]))
            if candidate == puzzle[block_row*3 + i][column_row*3 + j]:
                logging.debug("Constraint is False. Return.")
                return False

    logging.debug("Constraint is True. Return.")
    return True

# TODO: explore solution using modulo?




if __name__ == '__main__':
    print()
    print("The sudoku puzzle being solved is:")
    sudoku_printer(sudoku_puzzle)



# Tests:
# item = 9
# #
# # print(row_constraint(sudoku_puzzle, item, 0))
# # print(row_constraint(sudoku_puzzle, item, 1))
# # print(row_constraint(sudoku_puzzle, item, 2))
# #
# #
# # print(column_constraint(sudoku_puzzle, item, 0))
# # print(column_constraint(sudoku_puzzle, item, 1))
# # print(column_constraint(sudoku_puzzle, item, 2))
#
# print(block_constraint(sudoku_puzzle, item, 1, 1))
# print(block_constraint(sudoku_puzzle, item, 5, 1))
# print(block_constraint(sudoku_puzzle, item, 3, 1))
# print(block_constraint(sudoku_puzzle, item, 1, 3))
