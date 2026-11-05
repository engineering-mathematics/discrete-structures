"""Weighted directed graph."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import networkx as nx

from ._errors import CycleError, GraphError

if TYPE_CHECKING:
    from collections.abc import Hashable, Iterable


class DirectedGraph:
    """Directed graph with optional edge weights; self-loops allowed, parallel edges not."""

    def __init__(self, edges: Iterable[tuple[Hashable, Hashable]] = ()) -> None:
        """Build from ``(source, target)`` pairs."""
        self._g: Any = nx.DiGraph()  # networkx stubs vary across releases
        for source, target in edges:
            self.add_edge(source, target)

    def __len__(self) -> int:
        """Return the number of nodes."""
        return int(self._g.number_of_nodes())

    def __contains__(self, node: object) -> bool:
        """Whether ``node`` is in the graph."""
        return node in self._g

    def __repr__(self) -> str:
        """Unambiguous summary."""
        return f"DirectedGraph(nodes={len(self)}, edges={self.edge_count})"

    def _require(self, node: Hashable) -> None:
        if node not in self._g:
            raise GraphError(f"node {node!r} is not in the graph")

    @property
    def nodes(self) -> tuple[Hashable, ...]:
        """Nodes in insertion order."""
        return tuple(self._g.nodes)

    @property
    def edges(self) -> tuple[tuple[Hashable, Hashable], ...]:
        """``(source, target)`` pairs."""
        return tuple(self._g.edges)

    @property
    def edge_count(self) -> int:
        """Number of edges."""
        return int(self._g.number_of_edges())

    def add_node(self, node: Hashable) -> None:
        """Add an isolated node (no-op if present)."""
        self._g.add_node(node)

    def add_edge(self, source: Hashable, target: Hashable, weight: float = 1.0) -> None:
        """Add or overwrite an edge, creating missing nodes. ``weight`` must be finite."""
        if not weight == weight or weight in (float("inf"), float("-inf")):  # noqa: PLR0124
            raise GraphError(f"edge weight must be finite, got {weight}")
        self._g.add_edge(source, target, weight=float(weight))

    def has_edge(self, source: Hashable, target: Hashable) -> bool:
        """Whether the directed edge exists."""
        return bool(self._g.has_edge(source, target))

    def weight(self, source: Hashable, target: Hashable) -> float:
        """Weight of an existing edge."""
        if not self.has_edge(source, target):
            raise GraphError(f"edge {source!r} -> {target!r} is not in the graph")
        return float(self._g[source][target]["weight"])

    def successors(self, node: Hashable) -> tuple[Hashable, ...]:
        """Targets of edges leaving ``node``."""
        self._require(node)
        return tuple(self._g.successors(node))

    def predecessors(self, node: Hashable) -> tuple[Hashable, ...]:
        """Return the sources of edges entering ``node``."""
        self._require(node)
        return tuple(self._g.predecessors(node))

    def in_degree(self, node: Hashable) -> int:
        """Return the number of incoming edges."""
        self._require(node)
        return int(self._g.in_degree(node))

    def out_degree(self, node: Hashable) -> int:
        """Return the number of outgoing edges."""
        self._require(node)
        return int(self._g.out_degree(node))

    def is_dag(self) -> bool:
        """Whether the graph has no directed cycle."""
        return bool(nx.is_directed_acyclic_graph(self._g))

    def topological_order(self) -> tuple[Hashable, ...]:
        """Return a topological ordering; raise :class:`CycleError` if the graph has a cycle."""
        if not self.is_dag():
            raise CycleError("topological order is undefined for a graph with a cycle")
        return tuple(nx.topological_sort(self._g))

    def reachable(self, source: Hashable) -> frozenset[Hashable]:
        """Nodes reachable from ``source`` by a directed path (excluding ``source`` itself)."""
        self._require(source)
        return frozenset(nx.descendants(self._g, source))

    def shortest_path(self, source: Hashable, target: Hashable) -> tuple[Hashable, ...]:
        """Minimum-weight path (Dijkstra); weights must be non-negative."""
        self._require(source)
        self._require(target)
        if any(w < 0 for _, _, w in self._g.edges(data="weight")):
            raise GraphError("shortest_path requires non-negative edge weights")
        try:
            return tuple(nx.dijkstra_path(self._g, source, target, weight="weight"))
        except nx.NetworkXNoPath as exc:
            raise GraphError(f"no path from {source!r} to {target!r}") from exc

    def tree_text(self, root: Hashable) -> str:
        """Indented text rendering of the tree of successors below ``root``.

        Nodes already shown on the current branch are marked ``(cycle)`` and not expanded.
        """
        self._require(root)
        lines: list[str] = []

        def walk(node: Hashable, depth: int, branch: tuple[Hashable, ...]) -> None:
            if node in branch:
                lines.append(f"{'  ' * depth}{node!r} (cycle)")
                return
            lines.append(f"{'  ' * depth}{node!r}")
            for child in self._g.successors(node):
                walk(child, depth + 1, (*branch, node))

        walk(root, 0, ())
        return "\n".join(lines)
