"""Unit tests for MathSet. REQ-DS-001."""

from engg_math.discrete_structures import MathSet


def test_duplicates_collapse() -> None:
    assert len(MathSet([1, 1, 2])) == 2


def test_operators_match_named_methods() -> None:
    a, b = MathSet([1, 2, 3]), MathSet([3, 4])
    assert a | b == MathSet([1, 2, 3, 4])
    assert a & b == MathSet([3])
    assert a - b == MathSet([1, 2])
    assert a ^ b == MathSet([1, 2, 4])
    assert MathSet([3]) <= a
    assert a.isdisjoint(MathSet([9]))


def test_power_set_has_two_to_the_n_subsets() -> None:
    power = MathSet("abc").power_set()
    assert power.cardinality == 8
    assert MathSet() in power


def test_cartesian_product_cardinality_and_membership() -> None:
    product = MathSet([1, 2]).cartesian_product(MathSet("xy"))
    assert product.cardinality == 4
    assert (1, "x") in product


def test_equality_hash_membership_and_repr() -> None:
    assert MathSet([1, 2]) == MathSet([2, 1])
    assert hash(MathSet([1, 2])) == hash(MathSet([2, 1]))
    assert MathSet([1]) != [1]
    assert 1 in MathSet([1])
    assert set(MathSet([2, 1])) == {1, 2}
    assert repr(MathSet([2, 1])) == "MathSet({1, 2})"
