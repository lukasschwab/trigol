<img width="1268" alt="Screen Shot 2020-01-05 at 6 44 17 PM" src="https://user-images.githubusercontent.com/4955943/71791916-a00c2200-302e-11ea-9ed8-0a3cb4997443.png">

# trigol

Playing around with triangle-tesselated toroidal Game of Life scenarios because I'm reading DeLanda's *Philosophy and Simulation.*

Used [Cellular Automata in the Triangular Tessellation (Bays)](https://wpmedia.wolfram.com/uploads/sites/13/2018/02/08-2-4.pdf) as a reference for standard rulesets.

## Usage

This is built more for REPL-fiddling than modular usage.

### Standard Game of Life

```python
import trigol, grid, evaluators, time
test = trigol.GameBoard(
  30, 100,
  grid_class=grid.QuadGrid,
  evaluator=evaluators.conway_evaluator
)

# Glider.
test.set_multiple_cell_states([11, 15, 20, 21, 22])
while True:
  test.step(); test.print(); time.sleep(0.5)
```

### Triangle-tesselated Game of Life

```python
import trigol, evaluators, grid
test = trigol.GameBoard(
  20, 20,
  evaluator=evaluators.tri4644,
  grid_class=grid.TriGrid12
)

# Glider... with triangles!
test.set_multiple_cell_states([45, 46, 65, 66, 65, 86, 104, 105])
while True:
  test.step(); test.print(); time.sleep(0.5)
```

## Notes

`Grid` can expose `get_polygon_coordinates`; drawing to SVG can look up the coordinates, then write the polygon to SVG.
