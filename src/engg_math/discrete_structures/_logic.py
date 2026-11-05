"""Boolean gates and truth-table analysis."""

from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING

from ._errors import DomainError

if TYPE_CHECKING:
    from collections.abc import Callable


def and_(*inputs: bool) -> bool:
    """Conjunction of all inputs."""
    return all(inputs)


def or_(*inputs: bool) -> bool:
    """Disjunction of all inputs."""
    return any(inputs)


def not_(a: bool) -> bool:
    """Negation."""
    return not a


def nand(*inputs: bool) -> bool:
    """Negated conjunction."""
    return not all(inputs)


def nor(*inputs: bool) -> bool:
    """Negated disjunction."""
    return not any(inputs)


def xor(*inputs: bool) -> bool:
    """Return True when an odd number of inputs are true."""
    return sum(map(bool, inputs)) % 2 == 1


def xnor(*inputs: bool) -> bool:
    """Return True when an even number of inputs are true."""
    return not xor(*inputs)


def implies(a: bool, b: bool) -> bool:
    """Material implication ``a -> b``."""
    return (not a) or b


def truth_table(
    function: Callable[..., bool], n_inputs: int
) -> tuple[tuple[tuple[bool, ...], bool], ...]:
    """Evaluate ``function`` on all ``2**n_inputs`` rows, in binary counting order (False first)."""
    if n_inputs < 1:
        raise DomainError(f"n_inputs must be at least 1, got {n_inputs}")
    return tuple((row, bool(function(*row))) for row in product((False, True), repeat=n_inputs))


def is_tautology(function: Callable[..., bool], n_inputs: int) -> bool:
    """Whether ``function`` is true on every row."""
    return all(out for _, out in truth_table(function, n_inputs))


def is_satisfiable(function: Callable[..., bool], n_inputs: int) -> bool:
    """Whether ``function`` is true on at least one row."""
    return any(out for _, out in truth_table(function, n_inputs))


def are_equivalent(first: Callable[..., bool], second: Callable[..., bool], n_inputs: int) -> bool:
    """Whether both functions agree on every row."""
    return all(
        a == b
        for (_, a), (_, b) in zip(
            truth_table(first, n_inputs), truth_table(second, n_inputs), strict=True
        )
    )
