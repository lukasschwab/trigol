# TODO: some docstrings.
# TODO: SVG animation output.

def even(n):
    return not int(n) % 2

# Just copies the same board.
def copy_evaluator(board, i):
    return board.get_cell_state(i)

def invert_evaluator(board, i):
    return not copy_evaluator(board, i)

def infection_evaluator(board, i):
    neighbors = board.get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    return n_states > 0 or board.get_cell_state(i)

def conwayish_evaluator(board, i):
    neighbors = board.get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    # Unchanged if 1
    if n_states == 1:
        return board.get_cell_state(i)
    # Spawn if 2; else die
    return n_states == 2

# TODO: GameBoard should use an arbitrary grid. Should allow square grids, hex
# grids, etc., just with different adjacency rules.
class Grid:
    def __init__(self, num_rows, num_cols):
        assert False

    def _is_valid_index(self, index):
        assert False

    def get_neighbors(self, index):
        assert False

# TriGrid is just an indexing utility.
class TriGrid(Grid):
    def __init__(self, num_rows, num_cols):
        assert even(num_rows)
        self._num_rows = num_rows
        self._num_cols = num_cols

    def _total_items(self):
        return self._num_rows * self._num_cols

    def _third(self, index):
        L = self._num_cols
        n = index
        base = int((n / L) + 1) * L if even(index / L) else int((n / L) - 1) * L
        off = ((n % L) - 1) % L if even(index / L) else ((n % L) + 1) % L
        return base + off

    def _is_valid_index(self, index):
        return index >= 0 and index < self._total_items()


    # Offsets must be defined for an odd row.
    def _inner_get_neighbors(self, index, offsets):
        row, col = self._get_row_col(index)
        flipper = -1 if even(index / self._num_cols) else 1
        def inner_get(d_row, d_col):
            modified_row = row + (flipper * d_row)
            modified_col = col + (flipper * d_col)
            return self._get_index(modified_row, modified_col)
        return [inner_get(pair[0], pair[1]) for pair in offsets]


    def get_neighbors(self, index):
        return self._inner_get_neighbors(index, [
            (-1, 0),
            (-1, 1),
            (1, 0)
        ])

    # Accepts out-of-bound row, col pairs.
    def _get_index(self, row, col):
        row = row % self._num_rows
        col = col % self._num_cols
        return ((row * self._num_cols) + col) % self._total_items()

    def _get_row_col(self, index):
        assert self._is_valid_index(index)
        return int(index / self._num_cols), index % self._num_cols

class TriGrid12(TriGrid):
    def __init__(self, num_rows, num_cols):
        super().__init__(num_rows, num_cols)

    def get_neighbors(self, index):
        return self._inner_get_neighbors(index, [
            (1, 1),(2, 0),(1, 0),
            (2, -1),(1, -1),(0, -1),
            (-1, 0),(-2, 0),(-3, 1),
            (-2, 1),(-1, 1),(0, 1)
        ])

class GameBoard(TriGrid):
    def __init__(self, num_rows, num_cols, evaluator=copy_evaluator):
        super().__init__(num_rows, num_cols)
        # Initialize all cells to dead.
        self.cells = [False] * num_rows * num_cols
        self.evaluator = evaluator

    def get_cell_state(self, index):
        assert self._is_valid_index(index)
        return self.cells[index]

    def set_cell_state(self, index, state):
        assert self._is_valid_index(index)
        self.cells[index] = state

    def step(self):
        next = [False] * len(self.cells)
        for i in range(len(self.cells)):
            next[i] = self.evaluator(self, i)
        self.cells = next

    def __print_cell(self, index, up):
        if up:
            return "▲" if self.get_cell_state(index) else "△"
        return "▼" if self.get_cell_state(index) else "▽"

    # TODO: columnar printing.
    def print(self):
        for row in range(0, self._num_rows - 1, 2):
            line = " " * row
            for col in range(self._num_cols):
                top_index = row * self._num_cols + col
                bottom_index = (row + 1) * self._num_cols + col
                line += self.__print_cell(top_index, False)
                line += self.__print_cell(bottom_index, True)
            print(line)
