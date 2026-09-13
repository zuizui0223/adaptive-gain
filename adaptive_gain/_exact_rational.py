"""Shared exact-rational input validation for exact routing calculations."""
from __future__ import annotations

from fractions import Fraction


def as_exact_fraction(value: Fraction | int, *, name: str) -> Fraction:
    """Return an exact Fraction, rejecting floats and non-declared numeric types."""
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value, 1)
    if isinstance(value, float):
        raise TypeError(
            f"{name} must be Fraction or int; float breaks exact rational arithmetic"
        )
    raise TypeError(f"{name} must be Fraction or int for exact rational arithmetic")
