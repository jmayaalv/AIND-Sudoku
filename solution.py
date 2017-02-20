assignments = []

ROWS = 'ABCDEFGHI'
COLS = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def __remove_digit(values, box, digit):
    """
    Removes a digt from a box
    :param values: a grid in dict form
    :param box: box where the values wants to be removed
    :return: updated dict with the puzzle value
    """
    return assign_value(values, box, values[box].replace(digit, ''))


def cross(a, b):
    """Cross product of elements in A and elements in B.
    :param a: A list of items in A
    :param b: A list of items in B
    """
    return [s + t for s in a for t in b]


boxes = cross(ROWS, COLS)
row_units = [cross(r, COLS) for r in ROWS]
column_units = [cross(ROWS, c) for c in COLS]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[r + c for r, c in (zip(ROWS, COLS))], [a + b for a, b in zip(ROWS, COLS[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def __find_naked_twins(values, unit):
    """Find the naked twins in a unit
        :param: values: a grid in dict form
        :param: unit: a list of boxes

        :return: list of boxes with their value appearing exactly in two boxes.
    """
    boxes_with_pair = [box for box in unit if len(values[box]) == 2]

    twins = set()
    for box in boxes_with_pair:
        twins |= {peer for peer in boxes_with_pair if values[box] == values[peer] and box != peer}
    return list(twins)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    :param: values: a dictionary of the form {'box_name': '123456789', ...}

    :return:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        twins = __find_naked_twins(values, unit)
        if len(twins) == 2:
            twin_digits = values[twins[0]]
            for box in unit:
                if box not in twins:
                    for digit in twin_digits:
                        values = __remove_digit(values, box, digit)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    :param grid: - A grid in string form.
    :return:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return dict(map(lambda t: (t[0], COLS if t[1] == '.' else t[1]), zip(boxes, grid)))


def display(values):
    """
    Display the values as a 2-D grid.
    :param  values: The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)


def eliminate(values):
    """Eliminate values from peers of each box with a single value.
        :param values: Sudoku in dictionary form.
        :return:
            Resulting Sudoku in dictionary form after eliminating values.
        """
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        digit = values[box]
        for peer in peers[box]:
            values = __remove_digit(values, peer, digit)
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.
        :param values: Sudoku in dictionary form.
        :return:
            Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        boxes_in_unit = [box for box in unit]
        for box in boxes_in_unit:
            digits = [d for d in values[box]]
            for d in digits:
                candidate = [box for box in unit if d in values[box]]
                if len(candidate) == 1:
                    values = assign_value(values, candidate[0], d)
    return values


def reduce_puzzle(values):
    """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        :param values: A sudoku in dictionary form.
        :return:
            The resulting sudoku in dictionary form.
        """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    """
    Using depth-first search and propagation, try all possible values.
    :param values:
    :return:
    """

    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[box]) == 1 for box in boxes):
        return values

    n, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    for digit in values[box]:
        new_sudoku = values.copy()
        values = assign_value(new_sudoku, box, digit)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

    return False


def solve(grid):
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
