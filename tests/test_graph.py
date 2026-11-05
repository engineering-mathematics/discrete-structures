"""Unit and property tests for DirectedGraph. REQ-DS-005."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from engg_math.discrete_structures import CycleError, DirectedGraph, GraphError


def diamond() -> DirectedGraph:
    return DirectedGraph([("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")])


def test_structure_queries() -> None:
    g = diamond()
    assert len(g) == 4
    assert "a" in g
    assert g.edge_count == 4
    assert g.successors("a") == ("b", "c")
    assert g.predecessors("d") == ("b", "c")
    assert g.in_degree("d") == 2
    assert g.out_degree("a") == 2
    assert g.has_edge("a", "b")
    assert not g.has_edge("b", "a")
    assert repr(g) == "DirectedGraph(nodes=4, edges=4)"


def test_topological_order_respects_edges() -> None:
    g = diamond()
    order = g.topological_order()
    for source, target in g.edges:
        assert order.index(source) < order.index(target)


def test_cycle_detected() -> None:
    g = DirectedGraph([(1, 2), (2, 1)])
    assert not g.is_dag()
    with pytest.raises(CycleError):
        g.topological_order()


def test_reachability_excludes_source() -> None:
    assert diamond().reachable("a") == {"b", "c", "d"}
    assert diamond().reachable("d") == frozenset()


def test_shortest_path_uses_weights() -> None:
    g = DirectedGraph()
    g.add_edge("a", "b", 1.0)
    g.add_edge("b", "c", 1.0)
    g.add_edge("a", "c", 5.0)
    assert g.shortest_path("a", "c") == ("a", "b", "c")
    assert g.weight("a", "c") == 5.0


def test_shortest_path_errors() -> None:
    g = DirectedGraph([("a", "b")])
    g.add_node("z")
    with pytest.raises(GraphError, match="no path"):
        g.shortest_path("a", "z")
    g.add_edge("b", "z", -1.0)
    with pytest.raises(GraphError, match="non-negative"):
        g.shortest_path("a", "z")


@pytest.mark.parametrize("weight", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_weight_rejected(weight: float) -> None:
    with pytest.raises(GraphError, match="finite"):
        DirectedGraph().add_edge(1, 2, weight)


def test_missing_nodes_and_edges_raise() -> None:
    g = DirectedGraph([(1, 2)])
    with pytest.raises(GraphError):
        g.successors(9)
    with pytest.raises(GraphError):
        g.weight(2, 1)
    with pytest.raises(GraphError):
        g.reachable(9)


def test_tree_text_marks_cycles() -> None:
    g = DirectedGraph([("r", "x"), ("x", "r"), ("r", "y")])
    assert g.tree_text("r") == "'r'\n  'x'\n    'r' (cycle)\n  'y'"


@given(st.lists(st.tuples(st.integers(0, 6), st.integers(0, 6)), max_size=20))
def test_degree_sums_equal_edge_count(edges: list[tuple[int, int]]) -> None:
    g = DirectedGraph(edges)
    assert sum(g.in_degree(n) for n in g.nodes) == g.edge_count
    assert sum(g.out_degree(n) for n in g.nodes) == g.edge_count


@given(st.lists(st.tuples(st.integers(0, 6), st.integers(0, 6)), max_size=20))
def test_topological_order_exists_iff_acyclic(edges: list[tuple[int, int]]) -> None:
    g = DirectedGraph(edges)
    if g.is_dag():
        order = g.topological_order()
        assert all(order.index(s) < order.index(t) for s, t in g.edges)
    else:
        with pytest.raises(CycleError):
            g.topological_order()
