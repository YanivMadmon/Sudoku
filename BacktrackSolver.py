import math
from backtraking.ArcConsistency import ArcConsistency
from backtraking.BackTrack import BackTracking
from backtraking.CUtil import CUtil
from backtraking.Constraint import Constraint
import time


def solve_using_arc_consistency(constraint):
    arc = ArcConsistency(constraint)
    arc_consistent_sudoku = arc.ac3(constraint)
    check_complete = arc.is_complete(constraint)
    if check_complete and arc_consistent_sudoku:
        return arc_consistent_sudoku
    return None


class BacktrackingSolver:
    def __init__(self, boards, print_to_screen=True, arc=True, forward_check=True, mrv=True, print_to_file=None):

        self.box_size = []  # box size for each sudoku
        self.boards = []  # an array containing all sudokus represented as dictionary
        self.arc = arc  # use arc or not
        self.print_to_screen = print_to_screen
        self.fc = forward_check
        self.mrv = mrv
        self.print_to_file = print_to_file

        for line_board in boards:
            board = line_board.strip()  # strip the trailing "\n"

            # calculate size of the board and the box
            board_size = int(math.sqrt(len(board)))
            box_size = int(math.sqrt(board_size))
            self.box_size.append(box_size)

            constructed_sudoku = self.construct_sudoku(board, board_size)

            board = CUtil.generate_board(constructed_sudoku, box_size)
            self.boards.append(board)

    def get_grid_sizes(self):
        return self.box_size

    def get_boards(self):
        return self.boards

    def solve(self):
        if self.print_to_screen:
            print(f"\nStart solve {len(self.box_size)} boards with Solver {self.__str__()}\n")
        success_counter = 0
        for index, board in enumerate(self.boards):
            start = time.time()

            size_box = self.box_size[index]
            board_constraints = CUtil.generate_constraint_dictionary(size_box)
            constraint = Constraint(board, board_constraints, size_box)

            if self.arc:
                solve = solve_using_arc_consistency(constraint)
                if solve is not None:
                    end = time.time()
                    if self.print_to_file is not None:
                        self.print_to_file.write(
                            f"{index + 1}, {0}, {end - start}\n")
                    print(f" Board number {index + 1} solve successfully using arc consistency only ")
                    if self.print_to_screen:
                        self.print_board(solve, constraint.grid_size)
                    success_counter += 1
                    continue

            solve, backtrack_count = self.solve_using_backtrack(constraint)
            end = time.time()
            if solve is not None:
                if self.print_to_file is not None:
                    self.print_to_file.write(f"{index+1},{backtrack_count},{end - start}\n")
                msg = f" Board number {index + 1} solve successfully using back tracing," \
                    f" after {backtrack_count} attempts and time :{end - start}"
                if self.mrv:
                    msg += ", using MRV"
                if self.fc:
                    msg += ", using FC"
                if self.arc:
                    msg += ", using ARC"
                print(msg)
                if self.print_to_screen:
                    self.print_board(solve, constraint.grid_size)
                success_counter += 1
                continue

            elif self.print_to_file is not None:
                self.print_to_file.write(f"{index + 1}, -1, {end - start} \n")

        return success_counter, len(self.box_size)

    def solve_using_backtrack(self, constraint):
        back_track = BackTracking(self.fc)
        backtrack_sudoku = back_track.backtracking_search(constraint, self.mrv)
        if backtrack_sudoku != -1:
            return backtrack_sudoku, back_track.time
        return None, -1

    def __str__(self):
        msg = "Backtracking Solver"
        if self.mrv:
            msg += ", using MRV"
        if self.fc:
            msg += ", using FC"
        if self.arc:
            msg += ", using ARC"
        return msg

    @staticmethod
    def construct_sudoku(line, sudoku_size):
        sudoku = []
        for i in range(sudoku_size):
            start = i * sudoku_size
            end = sudoku_size * (i + 1)
            split_on_size = line[start: end]
            row = BacktrackingSolver.get_array(split_on_size)
            sudoku.append(row)

        return sudoku

    @staticmethod
    def get_array(strings):
        array = []
        for string in strings:
            array.append(string)
        return array

    @staticmethod
    def print_board(board, size_box):
        sudoku_size = size_box ** 2
        sort_board = dict(sorted(board.items()))
        temp = [i for i in range(0, sudoku_size, size_box)]
        for i, cell in enumerate(sort_board.values()):
            row, col = divmod(i, sudoku_size)
            if col == 0:
                if row in temp:
                    print('+' + size_box * ((5 * size_box * 2 + 4) * '-' + '+'))
            if col in temp:
                print("| ", end="")

            x = int((12 - len(cell)) / 2)
            if len(cell) % 2 == 0:
                print(x * " " + cell + (x - 1) * " ", end="")
            else:
                print(x * " " + cell + x * " ", end="")

            if col == sudoku_size - 1:
                print("|")
        print('+' + size_box * ((5 * size_box * 2 + 4) * '-' + '+') + "\n")


    @staticmethod
    def print_board_empty(board, size_box):
        sudoku_size = size_box ** 2
        sort_board = dict(sorted(board.items()))
        temp = [i for i in range(0, sudoku_size, size_box)]
        for i, cell in enumerate(sort_board.values()):
            if len(cell) != 1:
                cell = "0"
            row, col = divmod(i, sudoku_size)
            if col == 0:
                if row in temp:
                    print('+' + size_box * ((size_box * 2 + 4) * '-' + '+'))
            if col in temp:
                print("| ", end="")

            x = int((4 - len(cell)) / 2)
            if len(cell) % 2 == 0:
                print(x * " " + cell + (x - 1) * " ", end="")
            else:
                print(x * " " + cell + x * " ", end="")

            if col == sudoku_size - 1:
                print("|")
        print('+' + size_box * ((size_box * 2 + 4) * '-' + '+') + "\n")
