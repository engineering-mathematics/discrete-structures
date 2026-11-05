"""Sets, combinatorics, Boolean logic and directed graphs."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from ._combinatorics import (
    catalan,
    combination_count,
    combinations,
    factorial,
    multiset_count,
    permutation_count,
    permutations,
)
from ._errors import CycleError, DomainError, GraphError
from ._graph import DirectedGraph
from ._logic import (
    and_,
    are_equivalent,
    implies,
    is_satisfiable,
    is_tautology,
    nand,
    nor,
    not_,
    or_,
    truth_table,
    xnor,
    xor,
)
from ._sets import MathSet

try:
    __version__ = version("engg-math-discrete-structures")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"

__all__ = [
    "CycleError",
    "DirectedGraph",
    "DomainError",
    "GraphError",
    "MathSet",
    "__version__",
    "and_",
    "are_equivalent",
    "catalan",
    "combination_count",
    "combinations",
    "factorial",
    "implies",
    "is_satisfiable",
    "is_tautology",
    "multiset_count",
    "nand",
    "nor",
    "not_",
    "or_",
    "permutation_count",
    "permutations",
    "truth_table",
    "xnor",
    "xor",
]
