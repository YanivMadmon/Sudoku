# https://www.coin-or.org/PuLP/pulp.html
# https://www.coin-or.org/PuLP/CaseStudies/a_sudoku_problem.html
# https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html

import time
from pulp import *
import pulp as pl

import string


def data_constraint(board, size):
    """ A function that returns the constraints of the numbers given in the game board
    :param board: Sudoku board - a list of char (0 empty, other is value of the cell)
    :param size: Size of row / column of the board
    :return: constraint: list of list that represent the board data in the 3D matrix
    """
    constraint = []
    for i, cell in enumerate(board):
        if cell != '0':
            row, col = map(str, divmod(i, size))
            constraint.append([row, col, cell])
    return constraint


def display_sudoku_matrix(matrix, numbers, rows):
    """ A function that get matrix board sudoku and print to screen
      :param matrix: Sudoku 3D matrix board
      :param numbers: An array of all the values ​​that can be as values ​​in the board
      :param rows: An array of all the numbers of rows and column
      """
    size = len(numbers)
    square_root_size = int(size ** 0.5)
    # Create an array of all the values ​​in which we want to print a border in the table
    values_sub_grip = [str(i) for i in range(0, size, square_root_size)]
    for r in rows:
        if r in values_sub_grip:
            # print upper border
            print('+' + square_root_size * ((square_root_size * 2 + 1) * '-' + '+'))
        for c in rows:
            for v in numbers:
                if value(matrix[r][c][v]) == 1:
                    if c in values_sub_grip:
                        print("| ", end="")
                    print(v + " ", end="")
                    if c == str(size - 1):
                        print("|")
    print('+' + square_root_size * ((square_root_size * 2 + 1) * '-' + '+'))


class LinearProgrammingSolver:
    def __init__(self, boards, print_to_screen=True, print_to_file=None):
        self.boards = boards
        self.print_to_screen = print_to_screen
        self.print_to_file = print_to_file

    def __str__(self):
        return "Linear Programming Solver"

    def solve(self):
        """ Solving the board using linear programming
        :return True if Optimal - succeeded
        """
        if self.print_to_screen:
            print(f"\nStart solve {len(self.boards)} boards with Solver {self.__str__()}\n")
        success_counter = 0
        for board_number, line_board in enumerate(self.boards):
            start = time.time()
            board = line_board.strip()  # strip the trailing "\n"
            size = int(len(board) ** 0.5)

            # The default values
            value_in_board = [str(i) for i in range(1, 10)]
            # Add additional values ​​according to the size of the table
            value_in_board.extend(list(string.ascii_uppercase[0: size - 9]))

            rows_board = [str(i) for i in range(0, size)]
            cols_board = rows_board

            square_root_size = int(size ** 0.5)

            # Create sub_grids
            sub_grids = []
            for i in range(square_root_size):
                for j in range(square_root_size):
                    sub_grids += [[(rows_board[square_root_size * i + k], cols_board[square_root_size * j + l])
                                   for k in range(square_root_size) for l in range(square_root_size)]]

            # Definition of the variables, a matrix of 729 three-dimensional cells
            matrix_choices = LpVariable.dicts("Choice", (rows_board, cols_board, value_in_board), 0, 1, LpInteger)

            # Creating the Problem
            prob = LpProblem("Sudoku_Problem", LpMinimize)

            # Objective Function, set to 0 since Sudoku doesn't have an optimal solution
            prob += 0, "Arbitrary Objective Function"

            # Constraint 1: A row should have all the numbers from 1-9 and no number can be repeated (Row constraint)
            for v in value_in_board:
                for r in rows_board:
                    prob += lpSum([matrix_choices[r][c][v] for c in cols_board]) == 1, ""

            # Constraint 2: A column should have all the numbers from 1-9 and no number can be repeated (Column constraint)
            for v in value_in_board:
                for r in rows_board:
                    prob += lpSum([matrix_choices[r][c][v] for c in cols_board]) == 1, ""

            # Constraint 3: Only one number can be present in a cell (Value constraint)
            for r in rows_board:
                for c in cols_board:
                    prob += lpSum([matrix_choices[r][c][v] for v in value_in_board]) == 1, ""

            # Constraint 4: A sub grids should have all the numbers from 1-9 and no number can be repeated (Squares constraints)
            for v in value_in_board:
                for s in sub_grids:
                    prob += lpSum([matrix_choices[r][c][v] for (r, c) in s]) == 1, ""

            constraint_given = data_constraint(board, size)
            # Constraint 5: Set in matrix the number already given
            for constrain in constraint_given:
                prob += matrix_choices[constrain[0]][constrain[1]][constrain[2]] == 1, ""

            # Change solver
            # The problem data is written to an .lp file
            # prob.writeLP("Sudoku.lp")
            # solver = pulp.getSolver('CPLEX_CMD')
            # status = prob.solve(solver=GLPK(msg=False))

            solver = pl.PULP_CBC_CMD(msg=False, threads=1)

            prob.solve(solver)
            end = time.time()

            # The status of the solution is printed to the screen
            # print("Status:", LpStatus[prob.status])
            if prob.status == 1:
                if self.print_to_file != None:
                    self.print_to_file.write(
                    f"{board_number + 1}, {0}, {end - start}\n")
                print(f"\n Board number {board_number + 1} solve successfully, using {self.__str__()}")
                if self.print_to_screen:
                    display_sudoku_matrix(matrix_choices, value_in_board, rows_board)
                success_counter += 1
            else:
                print(f"\n Board number {board_number + 1} failed, using {self.__str__()}")

            # Remove all data
            del board
            del matrix_choices
            del value_in_board
            del rows_board
            del prob

        return success_counter, len(self.boards)








