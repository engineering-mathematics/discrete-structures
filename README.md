# engg-math-discrete-structures

Sets, combinatorics, Boolean logic and directed graphs for `engg_math`. Validated inputs, typed errors,
no printing.

```bash
pip install engg-math-discrete-structures
```

```python
from engg_math.discrete_structures import (
    MathSet,
    DirectedGraph,
    combination_count,
    truth_table,
    xor,
)

MathSet([1, 2]) | MathSet([2, 3])  # MathSet({1, 2, 3})
combination_count(52, 5)  # 2598960
truth_table(xor, 2)  # rows in counting order, False first
g = DirectedGraph([("a", "b"), ("b", "c")])
g.topological_order()  # ('a', 'b', 'c')
```

## API

| Area | Names |
|---|---|
| Sets | `MathSet` (union, intersection, difference, symmetric difference, power set, Cartesian product) |
| Counting | `factorial`, `permutation_count`, `combination_count`, `multiset_count`, `catalan`; lazy `permutations`, `combinations` |
| Logic | `and_`, `or_`, `not_`, `nand`, `nor`, `xor`, `xnor`, `implies`, `truth_table`, `is_tautology`, `is_satisfiable`, `are_equivalent` |
| Graphs | `DirectedGraph` (degrees, reachability, topological order, Dijkstra shortest path, `tree_text`) |
| Errors | `DomainError`, `GraphError`, `CycleError` (all subclass `EnggMathError`) |

## Scope of 0.1

Rich tree rendering, schematic drawing and graph plotting from the legacy package are not included;
they return as optional `viz` features. Parallel edges are not supported.

## Development

```bash
uv sync
uv run pytest && uv run ruff check && uv run mypy && uv run lint-imports
```

Licensed under Apache-2.0.
