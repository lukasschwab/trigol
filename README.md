# trigol

Playing around with triangle-tesselated toroidal Game of Life scenarios because I'm reading DeLanda's *Philosophy and Simulation.*

To-do items are noted inline.

## Usage

```python
import trigol, grid, evaluators, time
test = trigol.GameBoard(
  30, 100,
  grid_class=grid.QuadGrid,
  evaluator=evaluators.conway_evaluator
)

# Glider.
test.set_cell_state(5 + 10, True)
test.set_cell_state(10 + 10, True)
test.set_cell_state(11 + 10, True)
test.set_cell_state(12 + 10, True)
test.set_cell_state(1 + 10, True)
while True:
  test.step(); test.print(); time.sleep(0.5)
```

```python
import trigol, evaluators, grid
test = trigol.GameBoard(
  20, 20,
  evaluator=evaluators.tri4644,
  grid_class=grid.TriGrid12
)

# Glider... with triangles!
test.set_cell_state(45, True)
test.set_cell_state(46, True)
test.set_cell_state(65, True)
test.set_cell_state(66, True)
test.set_cell_state(85, True)
test.set_cell_state(105, True)
test.set_cell_state(104, True)
test.set_cell_state(86, True)
while True:
  test.step(); test.print(); time.sleep(0.5)
```

## Notes

`Grid` can expose `get_polygon_coordinates`; drawing to SVG can look up the coordinates, then write the polygon to SVG.
