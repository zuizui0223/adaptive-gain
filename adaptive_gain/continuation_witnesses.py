"""Finite controls for the scope of adaptive continuation bisimulation."""
from .core import FiniteTask, Query, World


def continuation_fixed_cost_collision() -> tuple[FiniteTask, FiniteTask]:
    """Same recursive cost class, but (C_A,C_F)=(2,3) versus (2,2).

    The shared abstract graph forgets which identical-cost query is reused across
    separate branches. That information is essential to the fixed comparator.
    """
    worlds = tuple(World(f"w{i}", i // 2) for i in range(4))
    strict = FiniteTask(worlds, (
        Query("left", 1, (0, 0, 0, 1)),
        Query("right", 1, (0, 1, 0, 0)),
        Query("route", 1, (0, 1, 1, 0)),
    ))
    bypass = FiniteTask(worlds, (
        Query("left", 1, (0, 0, 0, 1)),
        Query("bypass", 1, (0, 1, 0, 1)),
        Query("route", 1, (0, 1, 1, 0)),
    ))
    return strict, bypass


def equal_value_different_continuations() -> tuple[FiniteTask, FiniteTask]:
    """Both adaptive costs are 2, but one direct step is not two serial steps."""
    direct = FiniteTask((World("no", 0), World("yes", 1)), (
        Query("direct", 2, (0, 1)),
    ))
    xor = FiniteTask(tuple(World(f"w{i}", t) for i, t in enumerate((0, 1, 1, 0))), (
        Query("u", 1, (0, 0, 1, 1)),
        Query("v", 1, (0, 1, 0, 1)),
    ))
    return direct, xor
