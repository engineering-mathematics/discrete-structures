"""Exception types."""

from __future__ import annotations

from engg_math.core import EnggMathError


class DomainError(EnggMathError, ValueError):
    """An argument lies outside the domain of the operation."""


class GraphError(EnggMathError, ValueError):
    """A graph operation referenced a missing node or edge, or is undefined for this graph."""


class CycleError(GraphError):
    """The operation requires an acyclic graph."""
