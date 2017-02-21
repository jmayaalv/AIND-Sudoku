ROWS = 'ABCDEFGHI'
COLS = '123456789'

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
