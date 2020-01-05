def even(n):
    return not int(n) % 2

# Just copies the same board.
def copy_evaluator(board, i):
    return board.get_cell_state(i)

def invert_evaluator(board, i):
    return not copy_evaluator(board, i)

# TODO: can get a `Grid` abstract class and make the GameBoard class use any grid?
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
        self.__num_rows = num_rows
        self.__num_cols = num_cols

    def __total_items(self):
        return self.__num_rows * self.__num_cols

    def __third(self, index):
        L = self.__num_cols
        n = index
        base = int((n / L) + 1) * L if even(index / L) else int((n / L) - 1) * L
        off = ((n % L) - 1) % L if even(index / L) else ((n % L) + 1) % L
        return base + off

    def _is_valid_index(self, index):
        return index >= 0 and index < self.__total_items()

    def get_neighbors(self, index):
        t = self.__total_items()
        return ((index + self.__num_cols) % t, (index - self.__num_cols) % t, self.__third(index) % t)

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
