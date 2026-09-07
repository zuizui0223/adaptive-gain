import pytest

from adaptive_gain import (
    ResidualIsomorphismLimitError,
    ResidualPairCoverInstance,
    minimal_strict_gain_standard_task,
    residual_automorphism_group,
    verify_residual_automorphism_group,
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


def test_minimal_strict_gain_normal_form_has_full_s3_query_automorphism():
    receipt = residual_automorphism_group(_minimal_instance())
    assert receipt.stable_query_color_class_sizes == (3,)
    assert receipt.allowed_color_preserving_permutations == 6
    assert receipt.automorphism_count == 6
    assert receipt.distinct_labeled_incidence_forms == 1
    assert receipt.query_orbits == ((0, 1, 2),)
    assert verify_residual_automorphism_group(_minimal_instance(), receipt)


def test_regular_color_collision_controls_have_eight_query_automorphisms():
    for instance in (_cycle8(), _two_cycles4()):
        receipt = residual_automorphism_group(instance)
        assert receipt.allowed_color_preserving_permutations == 24
        assert receipt.automorphism_count == 8
        assert receipt.distinct_labeled_incidence_forms == 3
        assert receipt.query_orbits == ((0, 1, 2, 3),)


def test_720_to_12_refinement_benchmark_has_only_one_distinct_labeled_form_after_automorphisms():
    receipt = residual_automorphism_group(_refinement_benchmark_instance())
    assert receipt.allowed_color_preserving_permutations == 12
    assert receipt.automorphism_count == 12
    assert receipt.distinct_labeled_incidence_forms == 1
    assert receipt.query_orbits == (
        (0, 1),
        (2, 3, 4),
        (5,),
        (6,),
        (7,),
    )


def test_automorphism_enumeration_fails_closed_at_declared_cap():
    with pytest.raises(ResidualIsomorphismLimitError):
        residual_automorphism_group(_cycle8(), max_permutations=6)
