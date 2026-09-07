from itertools import product

from adaptive_gain import FiniteTask, Query, World, adaptive_gain_receipt, task_pair_antichain_bound
from adaptive_gain.five_world_normal_form import five_world_irreducible_standard_task
from adaptive_gain.target_pair_incidence import (
    pair_incidence_adaptive_minimum_resolution,
    pair_incidence_fixed_minimum_resolution,
    pair_incidence_sufficiency_audit,
    target_pair_incidence_task,
)


def _restricted_growth_partitions(n: int):
    rows = []
    def rec(prefix, maximum):
        if len(prefix) == n:
            rows.append(tuple(prefix))
            return
        for value in range(maximum + 2):
            rec(prefix + (value,), max(maximum, value))
    rec((0,), 0)
    return tuple(rows)


def _same_minimal_kernel_no_gain_control():
    worlds = (
        World("a0", 0), World("a1", 0),
        World("b0", 1), World("b1", 1), World("b2", 1),
    )
    return FiniteTask(
        worlds,
        (
            Query("q0", 1, (0, 0, 0, 0, 1)),
            Query("q1", 1, (0, 0, 0, 1, 0)),
            Query("q2", 1, (0, 0, 1, 0, 0)),
        ),
    )


def test_pair_incidence_solver_matches_new_irreducible_five_world_core():
    task = five_world_irreducible_standard_task()
    incidence = target_pair_incidence_task(task)
    adaptive = pair_incidence_adaptive_minimum_resolution(incidence)
    fixed = pair_incidence_fixed_minimum_resolution(incidence)
    assert adaptive.minimum_worst_path_cost == 2
    assert set(adaptive.optimal_first_queries) == {"q_route_left", "q_route_right"}
    assert fixed.minimum_cost == 3
    assert pair_incidence_sufficiency_audit(task).exact_costs_agree


def test_same_minimal_fixed_kernel_can_have_different_adaptive_costs():
    gain = five_world_irreducible_standard_task()
    no_gain = _same_minimal_kernel_no_gain_control()
    gain_kernel = task_pair_antichain_bound(gain)
    no_gain_kernel = task_pair_antichain_bound(no_gain)
    assert gain_kernel.canonical_signatures == no_gain_kernel.canonical_signatures == (1, 2, 4)
    assert (adaptive_gain_receipt(gain).adaptive_cost, adaptive_gain_receipt(gain).fixed_cost) == (2, 3)
    assert (adaptive_gain_receipt(no_gain).adaptive_cost, adaptive_gain_receipt(no_gain).fixed_cost) == (3, 3)
    assert target_pair_incidence_task(gain).query_separation_masks != target_pair_incidence_task(no_gain).query_separation_masks


def test_full_pair_incidence_matches_direct_solver_for_all_four_world_query_partitions():
    # Bell(4)=15 possible unlabeled set partitions per query, including
    # multi-valued outcomes.  This checks 15^3=3,375 deterministic tasks rather
    # than only binary query maps.
    partitions = _restricted_growth_partitions(4)
    assert len(partitions) == 15
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    disagreements = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        audit = pair_incidence_sufficiency_audit(task)
        disagreements += int(not audit.exact_costs_agree)
    assert disagreements == 0


def test_pair_incidence_ignores_target_pure_outcome_splitting_safely():
    worlds = (World("a0", 0), World("a1", 0), World("b0", 1), World("b1", 1))
    coarse = FiniteTask(worlds, (Query("q", 1, (0, 0, 1, 1)),))
    split_pure = FiniteTask(worlds, (Query("q", 1, (0, 2, 1, 1)),))
    left = target_pair_incidence_task(coarse)
    right = target_pair_incidence_task(split_pure)
    assert left.query_separation_masks == right.query_separation_masks
    assert pair_incidence_sufficiency_audit(coarse).exact_costs_agree
    assert pair_incidence_sufficiency_audit(split_pure).exact_costs_agree
    assert pair_incidence_adaptive_minimum_resolution(left).minimum_worst_path_cost == 1
    assert pair_incidence_adaptive_minimum_resolution(right).minimum_worst_path_cost == 1
