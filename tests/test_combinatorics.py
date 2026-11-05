"""Unit tests for counting and enumeration. REQ-DS-002."""

import math

import pytest

from engg_math.discrete_structures import (
    DomainError,
    catalan,
    combination_count,
    combinations,
    factorial,
    multiset_count,
    permutation_count,
    permutations,
)


def test_known_values() -> None:
    assert factorial(5) == 120
    assert permutation_count(5, 2) == 20
    assert combination_count(5, 2) == 10
    assert multiset_count(3, 2) == 6
    assert [catalan(n) for n in range(6)] == [1, 1, 2, 5, 14, 42]


def test_multiset_count_with_no_types() -> None:
    assert multiset_count(0, 0) == 1
    assert multiset_count(0, 3) == 0


def test_enumeration_matches_counts() -> None:
    items = "abcd"
    assert len(list(permutations(items, 2))) == permutation_count(4, 2)
    assert len(list(permutations(items))) == math.factorial(4)
    assert len(list(combinations(items, 2))) == combination_count(4, 2)


@pytest.mark.parametrize(
    "call",
    [
        lambda: factorial(-1),
        lambda: permutation_count(3, 4),
        lambda: combination_count(3, -1),
        lambda: multiset_count(-1, 1),
        lambda: catalan(-2),
        lambda: permutations("ab", 3),
        lambda: combinations("ab", 3),
    ],
)
def test_out_of_domain_raises(call: object) -> None:
    with pytest.raises(DomainError):
        call()  # type: ignore[operator]
