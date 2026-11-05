"""Counting and enumeration."""

from __future__ import annotations

import math
from itertools import combinations as _combinations
from itertools import permutations as _permutations
from typing import TYPE_CHECKING

from ._errors import DomainError

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence


def _nonneg(name: str, value: int) -> None:
    if value < 0:
        raise DomainError(f"{name} must be a non-negative integer, got {value}")


def _pair(n: int, k: int) -> None:
    _nonneg("n", n)
    _nonneg("k", k)
    if k > n:
        raise DomainError(f"k must not exceed n, got k={k}, n={n}")


def factorial(n: int) -> int:
    """``n!`` for integer ``n >= 0``."""
    _nonneg("n", n)
    return math.factorial(n)


def permutation_count(n: int, k: int) -> int:
    """Ordered selections of ``k`` from ``n`` distinct items."""
    _pair(n, k)
    return math.perm(n, k)


def combination_count(n: int, k: int) -> int:
    """Unordered selections of ``k`` from ``n`` distinct items."""
    _pair(n, k)
    return math.comb(n, k)


def multiset_count(n: int, k: int) -> int:
    """Unordered selections of ``k`` from ``n`` types with repetition allowed."""
    _nonneg("n", n)
    _nonneg("k", k)
    if n == 0:
        return int(k == 0)
    return math.comb(n + k - 1, k)


def catalan(n: int) -> int:
    """Return the ``n``-th Catalan number."""
    _nonneg("n", n)
    return math.comb(2 * n, n) // (n + 1)


def permutations(items: Sequence[object], k: int | None = None) -> Iterator[tuple[object, ...]]:
    """Lazily yield ordered ``k``-selections (all items when ``k`` is None)."""
    size = len(items) if k is None else k
    _pair(len(items), size)
    return _permutations(items, size)


def combinations(items: Sequence[object], k: int) -> Iterator[tuple[object, ...]]:
    """Lazily yield unordered ``k``-selections."""
    _pair(len(items), k)
    return _combinations(items, k)
