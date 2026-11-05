"""Immutable finite sets."""

from __future__ import annotations

from itertools import chain, combinations, product
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Hashable, Iterable, Iterator


class MathSet:
    """Immutable finite set with the standard set algebra."""

    __slots__ = ("_items",)

    def __init__(self, items: Iterable[Hashable] = ()) -> None:
        """Build from any iterable of hashable items; duplicates collapse."""
        self._items: frozenset[Hashable] = frozenset(items)

    def __contains__(self, item: object) -> bool:
        """Membership test."""
        return item in self._items

    def __iter__(self) -> Iterator[Hashable]:
        """Iterate in arbitrary order."""
        return iter(self._items)

    def __len__(self) -> int:
        """Cardinality."""
        return len(self._items)

    def __eq__(self, other: object) -> bool:
        """Set equality."""
        if not isinstance(other, MathSet):
            return NotImplemented
        return self._items == other._items

    def __hash__(self) -> int:
        """Hash consistent with equality."""
        return hash(self._items)

    def __repr__(self) -> str:
        """Unambiguous form with elements sorted by ``repr`` for stable output."""
        body = ", ".join(sorted(map(repr, self._items)))
        return f"MathSet({{{body}}})"

    def __or__(self, other: MathSet) -> MathSet:
        """Union."""
        return self.union(other)

    def __and__(self, other: MathSet) -> MathSet:
        """Intersection."""
        return self.intersection(other)

    def __sub__(self, other: MathSet) -> MathSet:
        """Difference."""
        return self.difference(other)

    def __xor__(self, other: MathSet) -> MathSet:
        """Symmetric difference."""
        return self.symmetric_difference(other)

    def __le__(self, other: MathSet) -> bool:
        """Subset."""
        return self.issubset(other)

    @property
    def cardinality(self) -> int:
        """Number of elements."""
        return len(self._items)

    def union(self, other: MathSet) -> MathSet:
        """Elements in either set."""
        return MathSet(self._items | other._items)

    def intersection(self, other: MathSet) -> MathSet:
        """Elements in both sets."""
        return MathSet(self._items & other._items)

    def difference(self, other: MathSet) -> MathSet:
        """Elements of ``self`` not in ``other``."""
        return MathSet(self._items - other._items)

    def symmetric_difference(self, other: MathSet) -> MathSet:
        """Elements in exactly one of the sets."""
        return MathSet(self._items ^ other._items)

    def issubset(self, other: MathSet) -> bool:
        """Whether every element of ``self`` is in ``other``."""
        return self._items <= other._items

    def isdisjoint(self, other: MathSet) -> bool:
        """Whether the sets share no element."""
        return self._items.isdisjoint(other._items)

    def power_set(self) -> MathSet:
        """All ``2**n`` subsets; the result holds ``MathSet`` elements."""
        elems = tuple(self._items)
        subsets = chain.from_iterable(combinations(elems, r) for r in range(len(elems) + 1))
        return MathSet(MathSet(s) for s in subsets)

    def cartesian_product(self, other: MathSet) -> MathSet:
        """Ordered pairs ``(a, b)`` with ``a`` in ``self`` and ``b`` in ``other``."""
        pairs: Any = product(self._items, other._items)
        return MathSet(pairs)
