"""Small structural witnesses for proof-symmetry audits.

These are synthetic pair-cover decision structures. They are not empirical data
and do not replace the scientific models in PAYOFF, MROD, or BALANCE.
"""
from __future__ import annotations

from .core import FiniteTask, Query, World


def cycle_branch_symmetry_control() -> FiniteTask:
    """Four-query C4 incidence with a two-to-one local branch-orbit reduction.

    The cross-target separator rows are, up to row order,

        0011, 0110, 1001, 1100.

    At fixed budget 1 the chosen obligation has two affordable separators. The
    weighted residual incidence has dihedral query symmetry, so those two branch
    queries lie in one exact automorphism orbit. One representative infeasibility
    proof plus an explicit child transport therefore covers both branches.
    """
    worlds = (
        World("a", 0),
        World("b", 0),
        World("c", 1),
        World("d", 1),
    )
    queries = (
        Query("q0", 1, (0, 1, 1, 0)),
        Query("q1", 1, (0, 1, 1, 1)),
        Query("q2", 1, (0, 1, 0, 1)),
        Query("q3", 1, (0, 1, 0, 0)),
    )
    return FiniteTask(worlds, queries)
