import math

import pytest

from adaptive_gain import FiniteTask, Query, World, target_entropy_bits


def test_nonhashable_target_is_rejected_at_task_construction():
    with pytest.raises(ValueError, match="target values must be hashable"):
        FiniteTask((World("w", ["bad"]),), ())


def test_nonhashable_query_outcome_is_rejected_at_task_construction():
    with pytest.raises(ValueError, match="query outcome values must be hashable"):
        FiniteTask((World("w", 0),), (Query("q", 1, (["bad"],)),))


def test_nan_like_target_and_outcome_labels_are_rejected():
    with pytest.raises(ValueError, match="reflexive"):
        FiniteTask((World("w", float("nan")),), ())
    with pytest.raises(ValueError, match="reflexive"):
        FiniteTask((World("w", 0),), (Query("q", 1, (float("nan"),)),))


def test_nonfinite_information_weights_are_rejected():
    task = FiniteTask((World("a", 0), World("b", 1)), ())
    for bad in ((math.nan, 1.0), (math.inf, 1.0), (1.0, math.inf)):
        with pytest.raises(ValueError, match="finite"):
            target_entropy_bits(task, bad)


def test_huge_finite_weights_are_scaled_before_normalization():
    task = FiniteTask((World("a", 0), World("b", 1)), ())
    value = target_entropy_bits(task, (1e308, 1e308))
    assert value == pytest.approx(1.0)
