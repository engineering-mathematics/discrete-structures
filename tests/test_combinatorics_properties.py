"""Property tests for counting identities. REQ-DS-003."""

import math

from hypothesis import given
from hypothesis import strategies as st

from engg_math.discrete_structures import catalan, combination_count, multiset_count


@given(st.integers(0, 40), st.data())
def test_pascal_rule(n: int, data: st.DataObject) -> None:
    k = data.draw(st.integers(1, max(n, 1)))
    if 1 <= k <= n:
        assert combination_count(n + 1, k) == combination_count(n, k) + combination_count(n, k - 1)


@given(st.integers(0, 40), st.data())
def test_combination_symmetry(n: int, data: st.DataObject) -> None:
    k = data.draw(st.integers(0, n))
    assert combination_count(n, k) == combination_count(n, n - k)


@given(st.integers(1, 30), st.integers(0, 30))
def test_multiset_is_combination_of_extended_pool(n: int, k: int) -> None:
    assert multiset_count(n, k) == math.comb(n + k - 1, k)


@given(st.integers(0, 30))
def test_catalan_recurrence(n: int) -> None:
    assert catalan(n + 1) == sum(catalan(i) * catalan(n - i) for i in range(n + 1))
