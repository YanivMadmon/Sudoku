import time
import BacktrackSolver as BkSolver
import LinearProgrammingSolver as LpSolver
import random


def read_from_txt(text_file):
    """ A function that return boards that saved on text file
        :param text_file: file in format n^2 chars or number in a row
        :return: boards: all boards that in the file
        """
    fp = open(text_file, "r")
    boards = fp.readlines()
    return boards


def random_line(text_file):
    """ Return a random line from file
        :param text_file: file in format n^2 chars or number in a row
        :return: one random board that in the file
        """
    lines = open(text_file).read().splitlines()
    my_line = random.choice(lines)
    return [my_line+"\n"]


def display_sudoku_problem(input_board):
    """ A function that get board sudoku and print to screen
                 :param input_board: Sudoku board - a list of char (0 empty, other is value of the cell)
                 """
    board = []
    board[:0] = input_board[0].strip()
    size = int(len(board) ** 0.5)
    square_root = int(size ** 0.5)
    temp = [i for i in range(0, size, square_root)]
    for i, cell in enumerate(board):
        row, col = divmod(i, size)
        if col == 0:
            if row in temp:
                print('+' + square_root * ((square_root*2 + 1) * '-' + '+'))
        if col in temp:
            print("| ", end="")
        print(cell + " ", end="")
        if col == size-1:
            print("|")
    print('+' + square_root * ((square_root * 2 + 1) * '-' + '+') + "\n")


def solve_all(solver):
    """ Solve all of the boards and print time and results (how many solved)
        :param solver: Solver that we use
        """
    start = time.time()
    status = solver.solve()
    end = time.time()
    msg = f"\tsolver: {solver}\t Time: {end - start}\t Result: [{status[0]}:{status[1]}]\n"
    print(msg)


def create_report_easy_backtracking():
    """ create_report_easy_backtracking: For report only - create files of easy board result solved
        all the Heuristics
        """
    # List of sudokus files to solve
    sudoku_files = [("sudoku_boards_txt/easy_20.txt", "_easy")]
    # List of solvers name
    solvers = ["bk_arc_fc_mrv", "bk_arc_fc", "bk_fc_mrv", "bk_arc_mrv", "bk_arc", "bk_fc", "bk_mrv"]

    for file in sudoku_files:
        boards = read_from_txt(file[0])
        for solver in solvers:
            # Create txt file and save result. format: board number, attempts backtracking, time
            f = open(solver+file[1]+".txt", 'w')

            arc, mrv, fc = False, False, False
            if "arc" in solver:
                arc = True
            if "mrv" in solver:
                mrv = True
            if "fc" in solver:
                fc = True

            # Create solver
            backtracking_solver = BkSolver.BacktrackingSolver(boards, print_to_screen=False, arc=arc,
                                                              forward_check=fc, mrv=mrv, print_to_file=f)
            solve_all(backtracking_solver)
            f.close()
            del backtracking_solver


def create_report_hard_backtracking():
    """ create_report_easy_backtracking: For report only - create files of easy board result solved
        all the Heuristics
        """
    # List of sudokus files to solve
    sudoku_files = [("sudoku_boards_txt/hard_20.txt", "_hard")]
    # List of solvers name
    solvers = ["bk_arc_fc_mrv", "bk_arc_fc", "bk_fc_mrv", "bk_arc_mrv"]

    for file in sudoku_files:
        boards = read_from_txt(file[0])
        for solver in solvers:
            # Create txt file and save result. format: board number, attempts backtracking, time
            f = open(solver + file[1] + ".txt", 'w')

            arc, mrv, fc = False, False, False
            if "arc" in solver:
                arc = True
            if "mrv" in solver:
                mrv = True
            if "fc" in solver:
                fc = True

            # Create solver
            backtracking_solver = BkSolver.BacktrackingSolver(boards, print_to_screen=False, arc=arc,
                                                              forward_check=fc, mrv=mrv, print_to_file=f)
            solve_all(backtracking_solver)
            f.close()
            del backtracking_solver


def create_report_lp_and_bt():
    """ create_report_lp_and_bt: For report only - create files of lr and br all Heuristics
    """
    # List of sudokus files to solve
    sudoku_files = [("sudoku_boards_txt/easy_1000.txt", "_easy_1000"), ("sudoku_boards_txt/sudoku_16.txt", "_big_16"), ("sudoku_boards_txt/hard_95.txt", "_hard_95"), ("sudoku_boards_txt/sudoku_25.txt", "_huge_25")]
    # List of solvers name
    solvers = ["lr", "bk_arc_fc_mrv"]

    for file in sudoku_files:
        boards = read_from_txt(file[0])
        for solver in solvers:
            # Create txt file and save result. format: board number, attempts backtracking, time
            f = open(solver + file[1] + ".txt", 'w')

            arc, mrv, fc = False, False, False
            if "arc" in solver:
                arc = True
            if "mrv" in solver:
                mrv = True
            if "fc" in solver:
                fc = True

            if solver == "lr":
                my_solver = LpSolver.LinearProgrammingSolver(boards, print_to_screen=False, print_to_file=f)
            else:
                # Create solver
                my_solver = BkSolver.BacktrackingSolver(boards, print_to_screen=False, arc=arc,
                                                              forward_check=fc, mrv=mrv, print_to_file=f)
            solve_all(my_solver)
            f.close()
            del my_solver


def start_solve_user_boards():
    """ Main program in normal mode:
                        Asks which sudoku to solve in which, and with which method of solving
                        """
    while True:

        board_difficult = input(f"What type of board would you like to solve?\n\t"
                                f"1. Easy 9X9\n\t2. Hard 9X9\n\t3. Large 16X16\n\t4. Huge 25X25\n")
        if board_difficult == "1":
            board = random_line("sudoku_boards_txt/easy_1000.txt")
        elif board_difficult == "2":
            board = random_line("sudoku_boards_txt/hard_95.txt")
        elif board_difficult == "3":
            board = random_line("sudoku_boards_txt/sudoku_16.txt")
        elif board_difficult == "4":
            board = random_line("sudoku_boards_txt/sudoku_25.txt")
        else:
            print("Error Invalid selection")
            continue

        print(f"The selected board is:\n ")
        display_sudoku_problem(board)

        use_solver = input(f"What solver do you want to use?\n\t"
                                f"1. Backtracking \n\t2. Linear Programming\n")
        if use_solver == "1":
            heuristics = input(f"What Heuristics do you want?\n"
                               f"You can select several heuristics! for example 12: Arc + Mrv\n\t"
                               f"1. Arc \n\t2. Mrv \n\t3. fc\n")
            arc, mrv, fc = False, False, False
            if "1" in heuristics:
                arc = True
            if "2" in heuristics:
                mrv = True
            if "3" in heuristics:
                fc = True
            solver = BkSolver.BacktrackingSolver(board, print_to_screen=True, arc=arc, forward_check=fc, mrv=mrv,
                                                 print_to_file=None)

        elif use_solver == "2":
            solver = LpSolver.LinearProgrammingSolver(board, print_to_screen=True)
        else:
            print("Error Invalid selection")
            continue

        solve_all(solver)

        if input("To exit Press - E\n") == "E":
            break


def main():
    while True:
        select = input("Select one of the options:\n\t1. Solve another Sudoku\n\t2. Create report\n\n\t9. Exit\n")
        if select == "1":
            start_solve_user_boards()
        elif select == "2":
            if  input("The process of building the report takes several hours,"
                      " if you are sure you want to continue, press y\n") == "y":
                create_report_easy_backtracking()
                create_report_hard_backtracking()
                create_report_lp_and_bt()
        elif select == "9":
            break


if __name__ == '__main__':
    main()
