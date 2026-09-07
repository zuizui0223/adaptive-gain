from itertools import product

from adaptive_gain import FiniteTask, Query, World, adaptive_minimum_resolution
from adaptive_gain.adaptive_safe_compression import (
    adaptive_refinement_compressed_minimum_resolution,
    adaptive_safe_compressed_minimum_resolution,
    target_relevant_query_classes,
    target_relevant_refinement_dominance,
)
from adaptive_gain.target_pair_incidence import target_pair_incidence_task


def _set_partitions(n):
    """Return canonical restricted-growth strings for all set partitions of range(n)."""
    rows = []

    def rec(prefix, next_label):
        if len(prefix) == n:
            rows.append(tuple(prefix))
            return
        for label in range(next_label + 1):
            prefix.append(label)
            rec(prefix, max(next_label, label + 1))
            prefix.pop()

    if n == 0:
        return ((),)
    rec([0], 1)
    return tuple(rows)


def _balanced_worlds():
    return (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )


def test_complete_four_world_partition_triples_preserve_exact_adaptive_cost():
    partitions = _set_partitions(4)
    assert len(partitions) == 15
    worlds = _balanced_worlds()
    checked = 0
    equivalent_states = refinement_states = 0
    equivalent_evaluated = refinement_evaluated = 0
    equivalent_pruned = refinement_pruned = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        direct = adaptive_minimum_resolution(task).minimum_worst_path_cost
        equivalent = adaptive_safe_compressed_minimum_resolution(task)
        refinement = adaptive_refinement_compressed_minimum_resolution(task)
        assert equivalent.minimum_worst_path_cost == direct
        assert equivalent.exact_direct_cost == direct
        assert equivalent.cost_agrees_with_direct_solver
        assert refinement.minimum_worst_path_cost == direct
        assert refinement.exact_direct_cost == direct
        assert refinement.cost_agrees_with_direct_solver
        equivalent_states += equivalent.search_states
        refinement_states += refinement.search_states
        equivalent_evaluated += equivalent.representative_queries_evaluated
        refinement_evaluated += refinement.nondominated_queries_evaluated
        equivalent_pruned += equivalent.dominated_query_occurrences_pruned
        refinement_pruned += refinement.refinement_dominated_query_occurrences_pruned
        checked += 1
    assert checked == 15 ** 3 == 3_375
    # Registered finite-universe computational benchmark, not a prevalence claim.
    assert (equivalent_states, refinement_states) == (12_361, 6_697)
    assert (equivalent_evaluated, refinement_evaluated) == (17_726, 7_514)
    assert (equivalent_pruned, refinement_pruned) == (4_246, 6_942)


def test_complete_two_query_partition_cost_grid_preserves_exact_adaptive_cost():
    partitions = _set_partitions(4)
    worlds = _balanced_worlds()
    checked = 0
    equivalent_states = refinement_states = 0
    for maps in product(partitions, repeat=2):
        for costs in product((1, 2), repeat=2):
            task = FiniteTask(
                worlds,
                tuple(
                    Query(f"q{i}", costs[i], outcomes)
                    for i, outcomes in enumerate(maps)
                ),
            )
            direct = adaptive_minimum_resolution(task).minimum_worst_path_cost
            equivalent = adaptive_safe_compressed_minimum_resolution(task)
            refinement = adaptive_refinement_compressed_minimum_resolution(task)
            assert equivalent.minimum_worst_path_cost == direct
            assert equivalent.cost_agrees_with_direct_solver
            assert refinement.minimum_worst_path_cost == direct
            assert refinement.cost_agrees_with_direct_solver
            equivalent_states += equivalent.search_states
            refinement_states += refinement.search_states
            checked += 1
    assert checked == (15 ** 2) * 4 == 900
    assert (equivalent_states, refinement_states) == (2_380, 1_960)


def test_same_mixed_continuation_with_different_pure_partition_prunes_expensive_query():
    worlds = (
        World("a0", 0), World("a1", 0), World("a2", 0),
        World("b0", 1), World("b1", 1),
    )
    task = FiniteTask(
        worlds,
        (
            # Both queries have the same only target-mixed child {a0,b0}.
            # They differ only in how the already-resolved a1/a2 pure branch is split.
            Query("cheap_route", 1, ("x", "a", "a", "x", "b")),
            Query("expensive_route", 2, ("x", "a1", "a2", "x", "b")),
            Query("finish", 1, ("u", "v", "v", "v", "v")),
        ),
    )
    incidence = target_pair_incidence_task(task)
    classes = target_relevant_query_classes(
        incidence,
        world_mask=(1 << len(worlds)) - 1,
    )
    route_class = next(
        row for row in classes if set(row.member_query_names) == {"cheap_route", "expensive_route"}
    )
    assert route_class.minimum_cost == 1
    assert route_class.representative_query_name == "cheap_route"
    assert route_class.dominated_query_names == ("expensive_route",)

    compressed = adaptive_safe_compressed_minimum_resolution(task)
    direct = adaptive_minimum_resolution(task)
    assert compressed.minimum_worst_path_cost == direct.minimum_worst_path_cost == 2
    assert compressed.dominated_query_occurrences_pruned > 0
    assert compressed.representative_queries_evaluated < compressed.raw_query_candidates_seen


def test_strict_target_relevant_refinement_safely_dominates_coarser_expensive_query():
    worlds = _balanced_worlds()
    task = FiniteTask(
        worlds,
        (
            # fine separates every cross-target pair that coarse separates, plus one more.
            Query("fine", 1, (0, 1, 0, 2)),
            Query("coarse", 2, (0, 0, 0, 1)),
            Query("finish", 1, (0, 0, 1, 0)),
        ),
    )
    incidence = target_pair_incidence_task(task)
    frontier = target_relevant_refinement_dominance(
        incidence,
        world_mask=(1 << len(worlds)) - 1,
    )
    fine = next(row for row in frontier if row.dominating_query_name == "fine")
    assert "coarse" in fine.dominated_query_names

    direct = adaptive_minimum_resolution(task)
    compressed = adaptive_refinement_compressed_minimum_resolution(task)
    assert direct.minimum_worst_path_cost == compressed.minimum_worst_path_cost == 2
    assert compressed.refinement_dominated_query_occurrences_pruned > 0
    assert compressed.nondominated_queries_evaluated < compressed.raw_query_candidates_seen


def test_equal_cost_equivalent_queries_are_interchangeable_not_double_counted():
    worlds = _balanced_worlds()
    task = FiniteTask(
        worlds,
        (
            Query("route_a", 1, (0, 0, 0, 1)),
            Query("route_b", 1, ("x", "x", "x", "y")),
            Query("finish", 1, (0, 1, 1, 0)),
        ),
    )
    equivalent = adaptive_safe_compressed_minimum_resolution(task)
    refinement = adaptive_refinement_compressed_minimum_resolution(task)
    assert equivalent.cost_agrees_with_direct_solver
    assert equivalent.dominated_query_occurrences_pruned > 0
    assert refinement.cost_agrees_with_direct_solver
    assert refinement.refinement_dominated_query_occurrences_pruned > 0


def test_no_progress_equivalence_class_is_skipped_without_changing_cost():
    worlds = _balanced_worlds()
    task = FiniteTask(
        worlds,
        (
            Query("constant_a", 1, (0, 0, 0, 0)),
            Query("constant_b", 2, ("z", "z", "z", "z")),
            Query("direct", 1, (0, 0, 1, 1)),
        ),
    )
    equivalent = adaptive_safe_compressed_minimum_resolution(task)
    refinement = adaptive_refinement_compressed_minimum_resolution(task)
    assert equivalent.minimum_worst_path_cost == 1
    assert equivalent.no_progress_query_occurrences_skipped >= 2
    assert equivalent.cost_agrees_with_direct_solver
    assert refinement.minimum_worst_path_cost == 1
    assert refinement.no_progress_query_occurrences_skipped >= 1
    assert refinement.cost_agrees_with_direct_solver
