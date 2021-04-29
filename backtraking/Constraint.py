"""
    This class sets the constraints for our sudoku.

                AA AB  AC AD
                BA BB  BC BD

                CA CB  CC CD
                DA DB  DC DD

    In the above 4x4 sudoku grid,
    The grid for AA is: AB BA BB
    The explicit constraint is given as follows:
        1. The numbers in the following pairs of squares cannot be the same:
            (AA,AB), (AA,AC), (AA, AD), (AA,BA), (AA,CA), (AA,DA), (AA,BB)

        The above constraints needs to be written for every cell in the sudoku. This can be extended similarly
        for NxN sudoku.
"""
from backtraking.CUtil import CUtil


class Constraint:
    """
        Args:
            board: A dictionary with key as the identifier to a cell and the value of the key is the value of the cell
            constraints: A dictionary with key as identifier to a cell and values is identifier to other cells
                         that cant have the same value as the current identifier (the explicit constraints), this includes
                         cells in the same row, same column and same grid
            grid_size: size of a grid (a 9x9 sudoku has 3 as its grid size, 4x4 sudoku as 2 as its grid size)
    """
    def __init__(self, board, constraints, grid_size):
        self.grid_size = grid_size
        self.neighbour = constraints
        self.constraints_tuples = CUtil.constraints_as_tuple(self.neighbour)  # constraints as tuples
        self.board = board
