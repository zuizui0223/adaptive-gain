"""Side-theory witnesses for topology-to-sensing kernel requirements.

These witnesses do not construct a biological topology-to-sensing map. They only
show, inside the finite deterministic task class, that the two scalar-gap support
objects used by the proposed bridge carry independent information:

* adaptive continuation alone does not determine fixed cost;
* productive frontier alone does not determine adaptive cost.
"""

from __future__ import annotations

from .core import FiniteTask, Query, World


def same_frontier_different_adaptive_cost_collision() -> tuple[FiniteTask, FiniteTask]:
    """Return two tasks with identical minimal productive frontier but different C_A.

    Both tasks have five worlds, a 2+3 target split, three unit-cost binary queries,
    and minimal productive frontier consisting of the three singleton query edges.
    Consequently C_F=3 for both tasks.

    The first task has C_A=3, while the second has C_A=2.  Thus their structural
    gaps are 0 and 1 even though the fixed-side sufficient object is identical.
    """

    worlds = (
        World("w0", 0),
        World("w1", 0),
        World("w2", 1),
        World("w3", 1),
        World("w4", 1),
    )

    adaptive_expensive = FiniteTask(
        worlds,
        (
            Query("q0", 1, (0, 0, 0, 0, 1)),
            Query("q1", 1, (0, 0, 0, 1, 0)),
            Query("q2", 1, (0, 0, 1, 0, 0)),
        ),
    )

    adaptive_cheaper = FiniteTask(
        worlds,
        (
            Query("q0", 1, (0, 0, 0, 0, 1)),
            Query("q1", 1, (0, 1, 0, 0, 0)),
            Query("q2", 1, (0, 1, 1, 1, 0)),
        ),
    )

    return adaptive_expensive, adaptive_cheaper
