"""Unit and property tests for Boolean logic. REQ-DS-004."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from engg_math.discrete_structures import (
    DomainError,
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


def test_gate_truth_values() -> None:
    assert and_(True, True)
    assert not and_(True, False)
    assert or_(False, True)
    assert not or_(False, False)
    assert not_(False)
    assert nand(True, False)
    assert not nand(True, True)
    assert nor(False, False)
    assert not nor(True, False)
    assert xor(True, False)
    assert not xor(True, True)
    assert xnor(True, True)
    assert not xnor(True, False)
    assert implies(False, False)
    assert not implies(True, False)


def test_truth_table_order_and_size() -> None:
    table = truth_table(and_, 2)
    assert [row for row, _ in table] == [
        (False, False),
        (False, True),
        (True, False),
        (True, True),
    ]
    assert [out for _, out in table] == [False, False, False, True]


def test_tautology_and_satisfiability() -> None:
    assert is_tautology(lambda a: a or not a, 1)  # noqa: SIM221
    assert not is_tautology(and_, 2)
    assert is_satisfiable(and_, 2)
    assert not is_satisfiable(lambda a: a and not a, 1)  # noqa: SIM220


def test_de_morgan_equivalence() -> None:
    assert are_equivalent(lambda a, b: not (a and b), lambda a, b: (not a) or (not b), 2)
    assert not are_equivalent(and_, or_, 2)


def test_truth_table_rejects_zero_inputs() -> None:
    with pytest.raises(DomainError):
        truth_table(and_, 0)


@given(st.lists(st.booleans(), min_size=1, max_size=8))
def test_nand_nor_are_negations(bits: list[bool]) -> None:
    assert nand(*bits) == (not and_(*bits))
    assert nor(*bits) == (not or_(*bits))
    assert xnor(*bits) == (not xor(*bits))
