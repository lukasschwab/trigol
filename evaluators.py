# Just copies the same board.
def copy_evaluator(board, i):
    return board.get_cell_state(i)

def invert_evaluator(board, i):
    return not copy_evaluator(board, i)

def infection_evaluator(board, i):
    neighbors = board.grid._get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    return n_states > 0 or board.get_cell_state(i)

# Adapted conway for the default TriGrid.
def conwayish_evaluator(board, i):
    neighbors = board.grid._get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    # Unchanged if 1
    if n_states == 1:
        return board.get_cell_state(i)
    # Spawn if 2; else die
    return n_states == 2

# Standard Game of Life.
def conway_evaluator(board, i):
    neighbors = board.grid._get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    if n_states == 2:
        return board.get_cell_state(i)
    elif n_states == 3:
        return True
    return False
