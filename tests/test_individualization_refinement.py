from itertools import product

import pytest

from adaptive_gain import (
    IndividualizationRefinementLimitError,
    ResidualPairCoverInstance,
    individualization_refined_canonical_signature,
    minimal_strict_gain_standard_task,
    refined_canonical_residual_pair_cover_signature,
)


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


def test_individualization_reduces_regular_color_collision_from_24_to_8_leaves():
    for instance in (_cycle8(), _two_cycles4()):
        refined = refined_canonical_residual_pair_cover_signature(instance)
        assert refined.permutations_examined == 24
        ir = individualization_refined_canonical_signature(instance)
        assert ir.signature == refined.signature
        assert ir.canonical_leaves == 8
        assert ir.canonical_leaves < refined.permutations_examined


def test_individualization_still_distinguishes_nonisomorphic_regular_controls():
    left = individualization_refined_canonical_signature(_cycle8())
    right = individualization_refined_canonical_signature(_two_cycles4())
    assert left.signature != right.signature


def test_minimal_strict_gain_normal_form_exposes_true_s3_query_symmetry():
    task = minimal_strict_gain_standard_task()
    instance = _minimal_instance_from_maps(tuple(query.outcomes for query in task.queries))
    refined = refined_canonical_residual_pair_cover_signature(instance)
    ir = individualization_refined_canonical_signature(instance)
    assert refined.permutations_examined == 6
    assert ir.canonical_leaves == 6
    assert ir.signature == refined.signature


def test_individualization_signature_matches_exact_refined_canonicalizer_on_all_4096_minimal_tasks():
    patterns = tuple(product((0, 1), repeat=4))
    for maps in product(patterns, repeat=3):
        instance = _minimal_instance_from_maps(maps)
        refined = refined_canonical_residual_pair_cover_signature(instance)
        ir = individualization_refined_canonical_signature(instance)
        assert ir.signature == refined.signature


def test_individualization_fails_closed_at_declared_search_cap():
    with pytest.raises(IndividualizationRefinementLimitError):
        individualization_refined_canonical_signature(_cycle8(), max_nodes=1)
