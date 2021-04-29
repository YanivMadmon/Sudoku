from copy import deepcopy
import random


class BackTracking:
    def __init__(self, forward_check=True):
        self.forward_check = forward_check
        self.time = 0
    """
        In Backtracking, we start with a empty state. (No values to the variables).
        We then pick one variable from the set.

        The order of picking the variables[the square to be filled in sudoku] depends on the heuristics used.
        Here we have used Minimum Remaining Value Heuristic to select the variable.

        The steps for back tracking:
        1. Choose a variable (square in a sudoku)
        2. Pick a value from the domain(1..9)
        3. Check if the picked value satisfies the constraints.
        4. If it does, pick another variable and repeat the process.
        5. If somewhere in the tree if the constraint satisfaction is broken, back track to the parent and try
            replacing the value for the parent variable until all the variables are filled and is consistent with the
            constraints established.
    """

    def backtracking_search(self, constraint, mrv=True):
        return self.backtrack({}, constraint, mrv)

    def backtrack(self, state, constraint, mrv):
        """
        if state is complete, then return state (If all the variable has a particular value)
        :param mrv: flag
        :param state:
        :param constraint:
        :return:
        """
        if self.is_complete(state, constraint):
            return state

        """
            select unassigned variable and assign values to it
            Heuristics -> MRV (Minimum remaining value)
        """
        if mrv:
            cell = self.get_minimum_remaining_value(state, constraint)
        else:
            cell = self.next_cell(state, constraint)

        # deep copy
        domain = deepcopy(constraint.board)

        for value in constraint.board[cell]:

            """
                check if the value is consistent, given the restrictions
            """
            if self.is_consistent(cell, value, state, constraint):

                """
                    add cell = val to state
                """
                state[cell] = value

                if self.forward_check:
                    deductions = {}
                    deductions = self.infer(state, deductions, constraint, cell, value)
                    if deductions != -1:
                        result = self.backtrack(state, constraint, mrv)
                        if result != -1:
                            return result
                    self.time += 1
                    if self.time > 100000000:
                        del state[cell]
                        return -1
                    del state[cell]
                    constraint.board.update(domain)

                else:
                    result = self.backtrack(state, constraint, mrv)
                    if result != -1:
                        return result
                    self.time += 1
                    if self.time > 100000000:
                        del state[cell]
                        return -1
                    del state[cell]
                    constraint.board.update(domain)

        return -1

    @staticmethod
    def is_complete(assignment, constraint):
        return set(assignment.keys()) == set(constraint.board.keys())

    @staticmethod
    def next_cell(state, constraint):
        unassigned_cell = {}
        for cell in constraint.board:
            if cell not in state.keys():
                return cell

    @staticmethod
    def select_random_variables(state, constraint):
        unassigned_cell = {}
        for cell in constraint.board:
            if cell not in state.keys():
                unassigned_cell.update({cell: len(constraint.board[cell])})
        return list(unassigned_cell.keys())[random.randint(0, len(unassigned_cell) - 1)]

    @staticmethod
    def is_consistent(var, value, assignment, constraint):
        for neighbor in constraint.neighbour[var]:
            if neighbor in assignment.keys() and assignment[neighbor] == value:
                return False
        return True

    """
        Forward checking is mainly used for early detection of failures.
        Terminate search when any variable has no legal values.

        1. assign value to a variable[a square or a box]
        2. iterate over the peers of the square
        3. if the peers is not already assigned a value and if the given value is in probable list of values (domain)
            for the neighbour, remove that value from the neighbour's probable list(domain)

            In other words, remove values for neighbour from domain that are inconsistent with A
    """
    @staticmethod
    def get_left_over_values_in_domain(constraint, neighbor, value):
        constraint.board[neighbor] = constraint.board[neighbor].replace(value, "")
        return constraint.board[neighbor]

    @staticmethod
    def infer(state, deductions, constraint, cell, value):
        deductions[cell] = value

        for neighbor in constraint.neighbour[cell]:
            if neighbor not in state and value in constraint.board[neighbor]:
                if len(constraint.board[neighbor]) == 1:
                    return -1
                left_over_values = BackTracking.get_left_over_values_in_domain(constraint, neighbor, value)

                if len(left_over_values) == 1:
                    check = BackTracking.infer(state, deductions, constraint, neighbor, left_over_values)
                    if check == -1:
                        return -1
        return deductions

    @staticmethod
    def get_minimum_remaining_value(state, constraint):
        unassigned_cell = {}
        for cell in constraint.board:
            if cell not in state.keys():
                unassigned_cell.update({cell: len(constraint.board[cell])})
        minimum_remaining_value = min(unassigned_cell, key=unassigned_cell.get)
        return minimum_remaining_value

