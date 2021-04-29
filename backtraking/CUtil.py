import string

class CUtil:

    # Returns a dictionary containing the cell UID as they key and the data for the cell as the value
    # Ex: 'AA': 2, 'AB': 4 ....
    @staticmethod
    def generate_board(initial_board, grid_size):
        board_dictionary = dict()
        iterator = 0
        board_identifiers = CUtil.__generate_board_identifiers(grid_size)

        # The default values
        value_in_board = [str(i) for i in range(1, 10)]
        # Add additional values ​​according to the size of the table
        value_in_board.extend(list(string.ascii_uppercase[0:int(grid_size ** 2) - 9]))
        candid = ''
        for char in value_in_board:
            candid += char

        for row in initial_board:
            for data in row:
                identifier = board_identifiers[iterator]
                board_dictionary[identifier] = data
                if data == '0':
                    board_dictionary[identifier] = candid
                iterator += 1

        return board_dictionary

    # returns a dictionary containing possible constraints for each cell
    # Ex: 'AA': 'AB', 'AC' ....
    @staticmethod
    def generate_constraint_dictionary(grid_size):
        identifiers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        board_size = grid_size * grid_size
        rows_selected = columns_selected = identifiers[:board_size]

        board_identifiers = CUtil.__generate_board_identifiers(grid_size)
        generated_grids = CUtil.__generate_grids(rows_selected, grid_size)

        constraints = dict()

        for board_identifier in board_identifiers:
            rows = CUtil.__others_in_row(board_identifier, rows_selected)
            columns = CUtil.__others_in_columns(board_identifier, columns_selected)
            grids = CUtil.__others_in_grid(board_identifier, generated_grids)

            constraints[board_identifier] = set(rows + columns + grids)

        return constraints

    # returns a tuple containing possible constraints for each cell
    # Ex: ('AA', 'AB'), ('AA', AC') ....
    @staticmethod
    def constraints_as_tuple(constraints):
        constraints_tuples = []
        for key, values in constraints.items():
            for value in values:
                constraints_tuples.append((key, value))

        return constraints_tuples

    @staticmethod
    def __others_in_row(board_identifier, identifiers):
        # if 'AB' then get just 'A', because that's the row
        row_identifier = board_identifier[0]
        others = []

        for identifier in identifiers:
            new_element = row_identifier + identifier
            if new_element != board_identifier:
                others.append(new_element)

        return others

    @staticmethod
    def __others_in_columns(board_identifier, identifiers):
        # if 'AB' then get just 'B', because that's the columns
        column_identifier = board_identifier[1]
        others = []

        for identifier in identifiers:
            new_element = identifier + column_identifier
            if new_element != board_identifier:
                others.append(new_element)

        return others

    @staticmethod
    def __others_in_grid(board_identifier, grids):
        # if 'AB' then get just 'B', because that's the columns
        selected_grid = []
        for index, grid in enumerate(grids):
            for element in grid:
                if element == board_identifier:
                    selected_grid = list(grid)
                    break

        selected_grid.remove(board_identifier)
        return selected_grid

    @staticmethod
    def __generate_grids(identifiers, grid_size):
        split_identifiers = []
        for i in range(grid_size):
            start = i * grid_size
            end = grid_size * (i + 1)
            selected = identifiers[start:end]
            split_identifiers.append(list(selected))

        grids = []
        for row in split_identifiers:
            # ["A", "B", "C"]
            for column in split_identifiers:
                # ["A", "B", "C"]
                inner_grid = []
                for identifier_row in row:
                    for identifier_column in column:
                        inner_grid.append(identifier_row + identifier_column)

                grids.append(inner_grid)

        return grids

    @staticmethod
    def __generate_board_identifiers(grid_size):
        identifiers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        board_size = grid_size * grid_size

        rows_selected = columns_selected = identifiers[:board_size]
        board = []
        for row_identifier in rows_selected:
            for column_identifier in columns_selected:
                board.append(row_identifier + column_identifier)

        return board

    @staticmethod
    def __testing9x9():
        string = "ABCDEFGHI"

        output_string = ""
        for letter1 in string:
            for letter2 in string:
                output_string += letter1 + letter2 + " "

            output_string += "\n"

        print(output_string)