# GENERIC

# copy_evaluator does not change any cell states.
def copy_evaluator(board, i):
    return board.get_cell_state(i)

# invert_evaluator inverts every cell state.
def invert_evaluator(board, i):
    return not copy_evaluator(board, i)

# infection_evaluator makes grants life to every cell neighboring at least one
# live cell.
def infection_evaluator(board, i):
    neighbors = board.grid._get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    return n_states > 0 or board.get_cell_state(i)

# TRIANGLE GRIDS

# trigrid_conway_evaluator is a shoddy adapted version of the standard
# conway_evaluator for the three-adjacent triangle grid.
def trigrid_conway_evaluator(board, i):
    neighbors = board.grid._get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    # Unchanged if 1
    if n_states == 1:
        return board.get_cell_state(i)
    # Spawn if 2; else die
    return n_states == 2

# QUAD GRIDS

# Standard Game of Life.
def conway_evaluator(board, i):
    neighbors = board.grid._get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    if n_states == 2:
        return board.get_cell_state(i)
    elif n_states == 3:
        return True
    return False
