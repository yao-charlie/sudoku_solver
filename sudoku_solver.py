import logging
import copy
import sudoku_scraper as scrape

# Custom logging attempt.
# TODO: replace with class method in another module. Possibly leave for future work for future modules.
# # custom logger:
# log_column = logging.getLogger(__name__)
#
# # custom handlers:
# log_column_c_handler = logging.StreamHandler()
# log_column_c_handler.setLevel(logging.INFO)
#
#
# # Custom formatters and add to handler:
# log_column_c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# log_column_c_handler.setFormatter(log_column_c_format)
#
# # add to logger
# log_column.addHandler(log_column_c_handler)


logging.basicConfig(level=logging.CRITICAL)

# A Sudoku puzzle is effectively a solution to three sets: 9 rows, 9 columns and 9 3x3 blocks.
# Each must satisfy the condition that only one element exists from numbers 1-9.
# A puzzle is proposed when some elements are populated in the grid, to form existing constraints on the rest of board.
# (N.B. fewer constraints typically mean a harder puzzle, assuming it is solvable)
# Typically, unfilled elements are present but our purposes, we'll assign these to '0' to easily test for this condition.

# Solution below is not necessarily formatted in typical distribution detail but attempts to demonstrate the steps
# in which to solve it.

# The data structure we can use to define a Sudoku grid is a 2-degree list: sudoku = [i][j], with i, j being max 9 (8).

# A random sample sudoku puzzle from websudoku:

# sudoku_puzzle = [[2, 6, 0, 9, 0, 0, 0, 8, 0],
#                  [0, 0, 3, 7, 1, 0, 0, 0, 0],
#                  [0, 0, 7, 4, 0, 8, 0, 0, 0],
#                  [0, 9, 4, 0, 8, 0, 3, 0, 0],
#                  [1, 7, 6, 0, 5, 0, 2, 9, 8],
#                  [0, 0, 8, 0, 9, 0, 4, 1, 0],
#                  [0, 0, 0, 5, 0, 1, 6, 0, 0],
#                  [0, 0, 0, 0, 7, 3, 5, 0, 0],
#                  [0, 4, 0, 0, 0, 9, 0, 3, 1]
#                  ]

# sudoku_puzzle = [[3, 0, 1, 8, 0, 7, 0, 0, 0],
#                  [6, 0, 0, 4, 9, 1, 3, 7, 0],
#                  [0, 0, 0, 0, 0, 0, 1, 8, 0],
#                  [0, 3, 2, 0, 0, 0, 0, 0, 0],
#                  [4, 0, 0, 0, 0, 0, 0, 0, 6],
#                  [0, 0, 0, 0, 1, 9, 0, 0, 0],
#                  [0, 0, 0, 2, 3, 0, 4, 0, 7],
#                  [5, 0, 8, 9, 0, 0, 0, 0, 0],
#                  [0, 0, 3, 0, 0, 0, 0, 0, 0]
#                  ]

# From https://www.sudoku-solutions.com/
# Test1Charlie
# sudoku_puzzle = [[1, 0, 3, 0, 9, 0, 0, 8, 0],
#                  [0, 0, 2, 0, 1, 8, 0, 0, 0],
#                  [8, 0, 0, 0, 0, 0, 1, 0, 0],
#                  [9, 4, 0, 0, 0, 3, 7, 0, 0],
#                  [2, 0, 0, 1, 0, 9, 0, 0, 4],
#                  [0, 0, 1, 5, 0, 0, 0, 9, 2],
#                  [0, 0, 5, 0, 0, 0, 0, 0, 9],
#                  [0, 0, 0, 7, 3, 0, 2, 0, 0],
#                  [0, 2, 0, 0, 6, 0, 5, 0, 8]
#                  ]


# To generalize:
# Sudoku is based off base 9 numbering (note that '0' does not exist) and that it is a squared integer. Thus, a Sudoku
# puzzle with base 4 or base 16 are quite possible.

# sudoku4 = [[1, 2, 3, 4],
#            [3, 4, 1, 2],
#            [2, 1, 4, 3],
#            [4, 3, 2, 1]
#            ]



# The above is a valid Sudoku on base 4. Hexadecimal Sudoku's also exist (hexadoku)
# TODO: write webscraper or so to more easily parse out samples
# So we should be able to generalize our function to solve any sized sudoku's as long as we pass the correct bases and
# roots.

sudoku_grid_size = 9

sudoku_root = int(sudoku_grid_size ** .5)

# sudoku_puzzle = [[1, 0, 3, 0],
#                  [0, 4, 0, 2],
#                  [0, 0, 4, 0],
#                  [0, 0, 0, 1]
#                  ]

# The function structure to go over each element is as follows:
def sudoku_printer(puzzle):
    if not puzzle:
        return print("You have passed 'False'! If you're expecting a puzzle, there was perhaps no solution?")

    # Check if what's passed is a valid sudoku matrix.

    if verify_entries(puzzle) and verify_shape(puzzle):

        for row in range(len(puzzle)):
            print()  # used to add en endline
            for column in range(len(puzzle[row])):
                print(puzzle[row][column], end=' ')  # end used to not print the end line command
        print()  # final end line


# This function only prints but the structure can be used for the iterative check
# PASS: change this to a decorator? Review after defining the solver.
#       -Doesn't seem appropriate as you would need the values passed from the function as is.

def verify_entries(puzzle):
    for row in range(len(puzzle)):
        for column in range(len(puzzle[row])):
            if not (sudoku_grid_size >= puzzle[row][column] >= 0 and isinstance(puzzle[row][column], int)):
                return False
    return True


def verify_shape(puzzle):
    if len(puzzle) != sudoku_grid_size:
        return False
    for row in range(len(puzzle)):
        if len(puzzle[row]) != sudoku_grid_size:
            return False
    return True


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

        logging.debug(
            "The value at row:{row}, column:{column} is {a}".format(row=row, column=column, a=puzzle[row][column]))

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
    block_row = row // sudoku_root
    logging.debug("Block Row is {a}".format(a=block_row))
    column_row = column // sudoku_root
    logging.debug("Column Row is {a}".format(a=column_row))

    for i in range(sudoku_root):
        for j in range(sudoku_root):
            logging.debug("{a}".format(a=puzzle[block_row * sudoku_root + i][column_row * sudoku_root + j]))
            if candidate == puzzle[block_row * sudoku_root + i][column_row * sudoku_root + j]:
                logging.debug("Constraint is False. Return.")
                return False

    logging.debug("Constraint is True. Return.")
    return True


# DONE: explore solution using modulo?
#       -alternative solutions appear to pass in values of row - row % 3 to set the index as the top-left entry and
#        iterate over a range of 3x3. Effectively floor division - possibly done as other languages may not have
#        (easy) floor division functions and it was not exploiting built-in python methods. Similar behvaiour can be
#        seen in other functions that do not have 'in' method for lists.


# As any given candidate must satisfy all three constraints, we'll compound these to reduce future function calls.

def all_constraint(puzzle, candidate, row, column):
    return row_constraint(puzzle, candidate, row) and \
           column_constraint(puzzle, candidate, column) and \
           block_constraint(puzzle, candidate, row, column)


# Finally, create a function to iterate over solutions and check if they satisfy constraints. This will take an
# incomplete Sudoku puzzle and return a completed puzzle (array) or return 'unsolvable'.

# Naive (and incomplete) solution is to simply iterate through:

def naive_solve_sudoku(puzzle):
    for row in range(len(puzzle)):
        for column in range(len(puzzle[row])):
            if puzzle[row][column] == 0:
                for candidate in range(sudoku_grid_size):
                    if all_constraint(puzzle, candidate, row, column):
                        puzzle[row][column] = candidate
    return puzzle


# This only returns items which can be satisfied with a first pass.

# There are a few ways to solve this but a back-tracking algorithm appears to be a reasonable solution. This will define
# all possible solutions in a tree-like data structure and the algorithm will need to perform depth-first recursive
# searches to identify candidates. If it fails, it will go up the tree until it reaches a node which still has options
# to iterate through.

# A typical depth-first recursive algorithm is as follows:
# def depth_first(tree):
#     if final constraint:
#         return True
#     for each child in tree
#         if untraversable:
#             return False
#         else:
#             return depth_first(child-tree)

# Our final condition is either we cannot satisfy the constraint at the given node, or, we are at the final element and
# the Sudoku is solved.

# Previously created due to scope reasons of needing a placeholder puzzle as we do not want to change the original.
# Now somewhat unnecessary as single function calls within code. Vestiges left here for documentation purposes.
def add_element(puzzle, candidate, row, column):
    puzzle[row][column] = candidate
    return puzzle


def remove_element(puzzle, row, column):
    puzzle[row][column] = 0
    return puzzle


# Function which takes a Sudoku puzzle and solves. Index is need to easily initialize but otherwise shouldn't be passed
# on the original function call.
# Done: remove the ability for the user to add an index function call.
#       -At least as much as one can - changed it to a private method call should we ever want to change this to a class
#        and otherwise abstracted the algorthimic portion away from the call.

def __solve_sudoku_algo(puzzle, index=0):
    # Define final recursion state and return value if recursion is successful
    # Flatten the row/column calls, we'll cast both to 'index' and reference row/column off index.
    if index == sudoku_grid_size ** 2:
        return puzzle

    # rebuilding row/column location
    column = index % sudoku_grid_size
    row = index // sudoku_grid_size
    logging.info(
        "SS called at index {index}, and at row {row} and column {column}".format(index=index, row=row, column=column))

    # check to see if the element is already filled. If so, we assume it is correct as we cannot change it
    # regardless and move onto the next element.
    if puzzle[row][column] != 0:
        return __solve_sudoku_algo(puzzle, index + 1)

    # iterate through all 1-9 possibilities in the given cell.
    for candidate in range(sudoku_grid_size):

        # if all constraints are valid, assign it the number, then pass the new candidate puzzle to another solve_sudoku
        if all_constraint(puzzle, candidate + 1, row, column):

            add_element(puzzle, candidate + 1, row, column)

            # state condition to check when to backtrack, then reset the graph to try a new candididate. Needed since
            # the state we check is if it's empty (initialized to 0). An alternative that most graph searches otherwise
            # take tends to be to store a flag if we've 'traversed' a node - we could do this but not needed here given
            # we know the Sudoku structure.

            state = __solve_sudoku_algo(puzzle, index + 1)

            # Decision to return to upper level decision node
            if not state:
                remove_element(puzzle, row, column)

            # Decision to pass this all the way up the chain if we're successful as 'state' = a finished puzzle is
            # 'True'.
            if state:
                return state
    else:
        return False


def solve_sudoku(puzzle, verbose=True, solve_in_place=False):
    if not verify_shape(puzzle) and verify_entries(puzzle):
        print('This is not a valid puzzle!')
        return False

    if verbose:
        print('\nThe Sudoku puzzle being solved is:')
        sudoku_printer(puzzle)

    if solve_in_place:
        solution = puzzle
        __solve_sudoku_algo(solution)
    else:
        solution = copy.deepcopy(puzzle)
        __solve_sudoku_algo(solution)

    if verbose:

        if solution:
            print('\nA solution is:')
            sudoku_printer(solution)
        else:
            print('\nThere is no solution!')

        if not solve_in_place:
            print("\nIt has now been stored in any variable you've assigned it to.")
        else:
            print("\nThe original Sudoku has now been modified in place.")

    return solution


if __name__ == '__main__':
    # print()
    # print("The sudoku puzzle being solved is:")
    # sudoku_printer(sudoku_puzzle)
    # print()
    # print("The solution is:")


    # Testing integration of the sudoku scraper

    sudoku_puzzle = scrape.new_sudoku('easy')
    solve_sudoku(sudoku_puzzle, solve_in_place=True)
    sudoku_puzzle = scrape.new_sudoku('medium')
    solve_sudoku(sudoku_puzzle, solve_in_place=True)
    sudoku_puzzle = scrape.new_sudoku('hard')
    solve_sudoku(sudoku_puzzle, solve_in_place=True)
    sudoku_puzzle = scrape.new_sudoku('evil')
    solve_sudoku(sudoku_puzzle, solve_in_place=True)

    # print(verify_shape(sudoku_puzzle))


# Tests:
#item = 9

# print(row_constraint(sudoku_puzzle, item, 0))
# print(row_constraint(sudoku_puzzle, item, 1))
# print(row_constraint(sudoku_puzzle, item, 2))


# print(column_constraint(sudoku_puzzle, item, 0))
# print(column_constraint(sudoku_puzzle, item, 1))
# print(column_constraint(sudoku_puzzle, item, 2))
#
# print(block_constraint(sudoku_puzzle, item, 1, 1))
# print(block_constraint(sudoku_puzzle, item, 5, 1))
# print(block_constraint(sudoku_puzzle, item, 3, 1))
# print(block_constraint(sudoku_puzzle, item, 1, 3))

# print(all_constraint(sudoku_puzzle, 9, 7, 0))
