import queue


# https://www.youtube.com/watch?v=mo0gmLMC72E
class ArcConsistency():

    """
        queue with all the arcs of CSP
    """
    q = queue.Queue()
    nodes_expanded = 0

    def __init__(self, constraint):
        for arc in constraint.constraints_tuples:
            self.q.put(arc)

    def ac3(self, constraint):
        i = 0
        """
            (X,Y) is an arc 
            
            Represented as X-> Y
            
            X, Y is consistent if, for each value 'x' that X can take, there is a value 'y' that
            Y can take respecting the restriction 
            
            Similarly, vice-versa for Y->X
        """
        while not self.q.empty():
            (X, Y) = self.q.get()
            i += 1

            # Remove consistent values
            if self.arc_reduce(constraint, X, Y):
                if len(constraint.board[X]) == 0:
                    return False

                for Z in (constraint.neighbour[X] - set(Y)):
                    self.q.put((Z, X))

        return True

    # returns true if a value is removed
    def arc_reduce(self, constraint, X, Y):
        reduced = False
        values = set(constraint.board[X])

        """
            values ->
                Domain for X
                Possible set of values that can be assigned
        """
        for x in values:
            if not self.is_consistent(constraint, x, X, Y):
                """
                    if there is no value that satisfies the restriction between X->Y
                    remove x from set of possible values (in this case constraint.board[X])
                """
                constraint.board[X] = constraint.board[X].replace(x, '')
                reduced = True

        return reduced

    """
        check if the value x is consistent (respecting the constraints) with all possible values of Y
    """
    @staticmethod
    def is_consistent(constraint, x, X, Y):
        for y in constraint.board[Y]:
            if Y in constraint.neighbour[X] and y != x:
                return True
        return False

    @staticmethod
    def is_complete(constraint):
        for variable, value in constraint.board.items():
            if len(constraint.board[variable]) > 1:
                return False
        return True
