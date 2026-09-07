from itertools import product

import pytest

from adaptive_gain import (
    ResidualIsomorphismLimitError,
    ResidualPairCoverInstance,
    individualization_refined_canonical_signature,
    minimal_strict_gain_standard_task,
    orbit_pruned_individualization_canonical_signature,
)


def _minimal_instance():
    task = minimal_strict_gain_standard_task()
    rows = []
    for i in (0, 1):
        for j in (2, 3):
            mask = 0
            for q, query in enumerate(task.queries):
                if query.outcomes[i] != query.outcomes[j]:
                    mask |= 1 << q
            rows.append(mask)
    return ResidualPairCoverInstance((1, 1, 1), tuple(rows), 2)


def _cycle8():
    return ResidualPairCoverInstance(
        (1, 1, 1, 1),
        (0b0011, 0b0110, 0b1100, 0b1001),
        2,
    )


def _two_cycles4():
    return ResidualPairCoverInstance(
        (1, 1, 1, 1),
        (0b0011, 0b0011, 0b1100, 0b1100),
        2,
    )


def _refinement_benchmark_instance():
    rows = []
    for q in (0, 1):
        rows.extend(((1 << q) | (1 << 6),) * 2)
    for q in (2, 3, 4):
        rows.append((1 << q) | (1 << 6))
        rows.append((1 << q) | (1 << 7))
    rows.extend(((1 << 5) | (1 << 7),) * 2)
    return ResidualPairCoverInstance((1, 1, 1, 1, 1, 1, 2, 3), tuple(rows), 4)


def _minimal_instance_from_maps(maps):
    rows = []
    for i in (0, 1):
        for j in (2, 3):
            mask = 0
            for q, outcomes in enumerate(maps):
                if outcomes[i] != outcomes[j]:
                    mask |= 1 << q
            rows.append(mask)
    return ResidualPairCoverInstance((1, 1, 1), tuple(rows), 2)


def test_orbit_pruning_collapses_minimal_s3_normal_form_to_one_leaf():
    instance = _minimal_instance()
    ordinary = individualization_refined_canonical_signature(instance)
    pruned = orbit_pruned_individualization_canonical_signature(instance)
    assert ordinary.canonical_leaves == 6
    assert pruned.canonical_leaves == 1
    assert pruned.root_automorphism_count == 6
    assert pruned.signature == ordinary.signature
    assert pruned.orbit_pruned_branches == 3


def test_orbit_pruning_collapses_regular_controls_to_one_leaf():
    for instance in (_cycle8(), _two_cycles4()):
        ordinary = individualization_refined_canonical_signature(instance)
        pruned = orbit_pruned_individualization_canonical_signature(instance)
        assert ordinary.canonical_leaves == 8
        assert pruned.canonical_leaves == 1
        assert pruned.root_automorphism_count == 8
        assert pruned.signature == ordinary.signature


def test_orbit_pruning_collapses_refinement_benchmark_remaining_symmetry():
    instance = _refinement_benchmark_instance()
    ordinary = individualization_refined_canonical_signature(instance)
    pruned = orbit_pruned_individualization_canonical_signature(instance)
    assert ordinary.canonical_leaves == 12
    assert pruned.canonical_leaves == 1
    assert pruned.root_automorphism_count == 12
    assert pruned.signature == ordinary.signature


def test_orbit_pruned_and_unpruned_ir_signatures_match_on_all_4096_minimal_tasks():
    patterns = tuple(product((0, 1), repeat=4))
    for maps in product(patterns, repeat=3):
        instance = _minimal_instance_from_maps(maps)
        ordinary = individualization_refined_canonical_signature(instance)
        pruned = orbit_pruned_individualization_canonical_signature(instance)
        assert pruned.signature == ordinary.signature


def test_orbit_pruning_fails_closed_when_automorphism_certification_cap_is_too_small():
    with pytest.raises(ResidualIsomorphismLimitError):
        orbit_pruned_individualization_canonical_signature(
            _minimal_instance(), max_automorphism_permutations=5
        )
