from grid import QuadGrid
from evaluators import infection_evaluator

# TODO: SVG animation output.

# GameBoard represents a Game of Life state.
class GameBoard:
    def __init__(self, num_rows, num_cols, evaluator=infection_evaluator, grid_class=QuadGrid):
        self.grid = grid_class(num_rows, num_cols)
        self.__evaluator = evaluator
        # Initialize all cells to dead.
        self.cells = [False] * num_rows * num_cols

    def get_cell_state(self, index):
        assert self.grid._is_valid_index(index)
        return self.cells[index]

    def set_cell_state(self, index, state=True):
        assert self.grid._is_valid_index(index)
        self.cells[index] = state

    def set_multiple_cell_states(self, indices, state=True):
        for index in indices:
            self.set_cell_state(index, state)

    def step(self):
        next = [False] * len(self.cells)
        for i in range(len(self.cells)):
            next[i] = self.__evaluator(self, i)
        self.cells = next

    # print defers to the underlying grid's print method.
    def print(self):
        self.grid._print(self.get_cell_state)
