# if __name__ == '__main__':


# A Sudoku puzzle is effectively a solution to three sets: 9 rows, 9 columns and 9 3x3 blocks.
# Each must satisfy the condition that only one element exists from numbers 1-9.
# A puzzle is proposed when some elements are populated in the grid, to form existing constraints on the rest of board.
# (N.B. fewer constraints typically mean a harder puzzle, assuming it is solvable)
# Typically, unfilled elements are present but our purposes, we'll assign these to '0' to easily test for this condition.


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

# We define three functions to test this property.

# Function 1: test row.
