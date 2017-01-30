import logging

rows = 'ABCDEFGHI'
cols = '123456789'

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    if len(value) == 0:
        raise NameError('box [{}] = ""'.format(value))
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diag_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
              ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            new_val = values[peer].replace(digit, '')
            if len(new_val) == 0:
                raise NameError('box [{}] = ""'.format(peer))
            assign_value(values, peer, new_val)

    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
                # values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.

    Used by search to solve the puzzle.

    Repeatedly try different constraints to reduce the digits in each box.

    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_boxes = [box for box in values.keys() if len(values[box]) > 1]
    if len(unsolved_boxes) == 0:
        return values
    min_box = ''
    min_len = 1111
    for box in unsolved_boxes:
        if len(values[box]) < min_len:
            min_len = len(values[box])
            min_box = box

    for val in values[min_box]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, min_box, val)
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    result =  values.copy()
    for unit in unitlist:
        unsolved_boxes = [box for box in unit if len(values[box]) == 2]

        for box in unsolved_boxes:
            for box2 in unsolved_boxes:
                # Find all instances of naked twins
                if box != box2 and values[box] == values[box2]:
                    for digit in values[box]:
                        for elim_box in unit:
                            if elim_box != box and elim_box != box2 and digit in result[elim_box] and len(result[elim_box]) >1:
                                # Eliminate the naked twins as possibilities for their peers
                                # display(values)
                                logging.debug('naked twins {} {} {}'.format(box, box2, values[box]))
                                logging.debug('naked twins: removing digit {} from {} {}'.format(digit, elim_box, values[elim_box]))
                                assign_value(result, elim_box, result[elim_box].replace(digit, ''))
    return result


