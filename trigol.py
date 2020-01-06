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
    neighbors = board.grid._get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    return n_states > 0 or board.get_cell_state(i)

def conwayish_evaluator(board, i):
    neighbors = board.grid._get_neighbors(i)
    n_states = sum([board.get_cell_state(n) for n in neighbors])
    # Unchanged if 1
    if n_states == 1:
        return board.get_cell_state(i)
    # Spawn if 2; else die
    return n_states == 2

# TODO: GameBoard should use an arbitrary grid. Should allow square grids, hex
# grids, etc., just with different adjacency rules.

# Grids are indexing utilities for GameBoards.
class Grid:
    def __init__(self, num_rows, num_cols):
        self._num_rows = num_rows
        self._num_cols = num_cols
        # Default to none.
        self._print_line_lead = ""

    # Must be implemented.
    def _get_neighbors(self, index):
        assert False

    # Must be implemented.
    def _get_uni_cell(self, index):
        assert False

    def _total_items(self):
        return self._num_rows * self._num_cols

    def _is_valid_index(self, index):
        return index >= 0 and index < self._total_items()

    # Accepts out-of-bound row, col pairs.
    def _get_index(self, row, col):
        row = row % self._num_rows
        col = col % self._num_cols
        return ((row * self._num_cols) + col) % self._total_items()

    def _get_row_col(self, index):
        assert self._is_valid_index(index)
        return int(index / self._num_cols), index % self._num_cols

class QuadGrid(Grid):
    def __init__(self, num_rows, num_cols):
        assert num_rows > 0 and num_cols > 0
        super().__init__(num_rows, num_cols)

    def _get_neighbors(self, index):
        row, col = self._get_row_col(index)
        return [self._get_index(pair[0], pair[1]) for pair in [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1),                 (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1)
        ]]

    def _get_uni_cell(self, index):
        return { True: "■", False: "□" }

# TriGrid is a default triangle-tesselated toroidal grid. Each cell has three
# neighbors, corresponding to its three shared edges.
class TriGrid(Grid):
    def __init__(self, num_rows, num_cols):
        assert num_rows > 0 and num_cols > 0
        assert even(num_rows)
        super().__init__(num_rows, num_cols)
        # Offsets are prettier.
        self._print_line_lead = " "

    # Offsets must be defined for an odd row.
    def _inner_get_neighbors(self, index, offsets):
        row, col = self._get_row_col(index)
        flipper = -1 if even(index / self._num_cols) else 1
        def inner_get(d_row, d_col):
            modified_row = row + (flipper * d_row)
            modified_col = col + (flipper * d_col)
            return self._get_index(modified_row, modified_col)
        return [inner_get(pair[0], pair[1]) for pair in offsets]

    def _get_neighbors(self, index):
        return self._inner_get_neighbors(index, [
            (-1, 0),
            (-1, 1),
            (1, 0)
        ])

    def _get_uni_cell(self, index):
        row, _ = self._get_row_col(index)
        return { True: "▼", False: "▽" } if even(row) else { True: "▲", False: "△" }

# TriGrid12 is a variant triangle-tesselated toroidal grid. Each cell has twelve
# neighbors, corresponding to the 12 triangles that share one of its vertices.
class TriGrid12(TriGrid):
    def __init__(self, num_rows, num_cols):
        super().__init__(num_rows, num_cols)

    def _get_neighbors(self, index):
        return self._inner_get_neighbors(index, [
            (1, 1),(2, 0),(1, 0),
            (2, -1),(1, -1),(0, -1),
            (-1, 0),(-2, 0),(-3, 1),
            (-2, 1),(-1, 1),(0, 1)
        ])

class GameBoard:
    def __init__(self, num_rows, num_cols, evaluator=infection_evaluator, grid_class=TriGrid):
        self.grid = grid_class(num_rows, num_cols)
        self.evaluator = evaluator
        # Initialize all cells to dead.
        self.cells = [False] * num_rows * num_cols

    def get_cell_state(self, index):
        assert self.grid._is_valid_index(index)
        return self.cells[index]

    def set_cell_state(self, index, state):
        assert self.grid._is_valid_index(index)
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

    # TODO: grids should provide iterable index/unicode option pairs.
    def print(self):
        def print_cell(alive):
            return self.grid._get_uni_cell(index)[alive]
        for row in range(0, self.grid._num_rows - 1, 2):
            line = " " * row
            for col in range(self.grid._num_cols):
                top_index = row * self.grid._num_cols + col
                bottom_index = (row + 1) * self.grid._num_cols + col
                line += self.__print_cell(top_index, False)
                line += self.__print_cell(bottom_index, True)
            print(line)
