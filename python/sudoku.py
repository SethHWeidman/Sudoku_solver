assignments = []
ROWS = 'ABCDEFGHI'
COLS = '123456789'

def get_boxes(A, B):
    '''Combinations of concatenations of all the strings in a list of strings.'''
    return [s+t for s in A for t in B]

boxes = get_boxes(ROWS, COLS)

def grid_values(grid_string, blanks='.'):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid_string - A grid in string form.
        blanks - what string to fill in the blanks with
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid_string:
        if c == '.':
            values.append(blanks)
        elif c in all_digits:
            values.append(c)
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Allocated the amount of space needed to hold the value of the greatest length.
    # For a complete board, this will just be 1.
    width = 1+max(len(values[s]) for s in boxes)

    # Multiply the width by 3
    # Take three of these
    # Add '+'s in between them
    line = '+'.join(['-'*(width*3)]*3)

    # For each row and column in the data:
    # Print the value in that cell
    # Center it (https://www.tutorialspoint.com/python/string_center.htm)
    # Add "|" if the string is in column 3 or 6.
    # Print a "line" if the current row is the third or sixth
    for r in ROWS:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # Get all the solved boxes
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]

    # For a given solved box...
    for box in solved_boxes:

        # ...get the value in the box
        digit = values[box]

        # ...and for each of that box's "peers"...
        for peer in peers[box]:

            # ...delete that value from the possible values in that box
            values[peer] = values[peer].replace(digit, '')
            # print("Eliminated ", digit, "from box ", peer, " using the 'eliminate' strategy.")
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
            if len(dplaces) == 1 and values[dplaces[0]] != digit:
                values[dplaces[0]] = digit
                # print("Placed value ", digit, " in box ", dplaces[0])
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        peers(dict): a dictionary with each cell as the key and each of its
        "peers" as a value
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    """
    Implement the naked twins elimination strategy:
    Go through each cell:
    For each cell with two values:
    Find if there is a cell in "peers" that has the same two values in it
    Save those two box values
    For any cell that is a peer of both of those
    Eliminate those two values from those two boxes
    """
    # print("Before naked twins:")
    # display(values)
    # Get all the boxes with two values
    boxes_with_two = [box for box in values.keys() if len(values[box]) == 2]

    # Loop through these boxes
    for box_with_two in boxes_with_two:

        # Get that box's values
        box_values = values[box_with_two]

        # Peers that have the same two values:
        same_peers = [peer for peer in peers[box_with_two] if values[peer] == box_values]

        # If we find a "naked twin":
        if len(same_peers) == 1:

            # Peers that have the same two values:
            box_with_two_peers = same_peers[0]

            # Get the peers of each box
            peers_1, peers_2 = peers[box_with_two], peers[box_with_two_peers]

            # Get boxes that are peers of both
            peers_of_both = [peer2 for peer2 in peers_2 if peer2 in peers_1]

            # For each "peer of both"
            for peer_of_both in peers_of_both:

                # Only for the peers that have more than one value in them
                if len(values[peer_of_both]) > 1:

                    # For each of the "naked twins values":
                    for value in box_values:

                        # If the peer_of_both:
                        if value in values[peer_of_both]:

                            # Eliminate it
                            values[peer_of_both] = (
                                values[peer_of_both]
                                .replace(value, '')
                                )
                            # print("Eliminated", value, "from", peer_of_both, "using Naked Twins")
                            # display(values)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # print(peers)
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    print("Displaying the grid: ")
    grid_vals = grid_values(grid, blanks='.')
    display(grid_vals)
    print("Solving the puzzle: ")
    grid_vals_puzzle = grid_values(grid, blanks='123456789')
    final_values = search(grid_vals_puzzle)
    return final_values


def solve_values(values):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    print("Solving the puzzle: ")
    final_values = search(values)
    return final_values
