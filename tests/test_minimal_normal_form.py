from itertools import product

from adaptive_gain import FiniteTask, Query, World, adaptive_gain_receipt
from adaptive_gain.minimal_normal_form import (
    MINIMAL_STRICT_GAIN_SIGNATURE,
    canonical_minimal_separator_signature,
    minimal_normal_form_receipt,
    minimal_strict_gain_standard_task,
    standard_raw_symmetry_orbit_size,
)


def test_standard_normal_form_has_exact_cost_gap_and_signature():
    task = minimal_strict_gain_standard_task()
    receipt = minimal_normal_form_receipt(task)
    assert receipt.canonical_separator_signature == MINIMAL_STRICT_GAIN_SIGNATURE == (3, 5, 9)
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
    assert receipt.matches_unique_strict_gain_normal_form
    assert receipt.exact_strict_gain
    assert receipt.classification_agrees_with_exact_solver


def test_standard_raw_symmetry_orbit_has_exactly_192_labeled_tasks():
    assert standard_raw_symmetry_orbit_size() == 192


def test_minimal_signature_is_exact_iff_classifier_on_all_4096_labeled_tasks():
    targets = (0, 0, 1, 1)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    patterns = tuple(product((0, 1), repeat=4))
    strict = normal_form = false_positive = false_negative = 0
    strict_signatures = set()
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, outcomes) for j, outcomes in enumerate(maps)),
        )
        exact = adaptive_gain_receipt(task).strict_adaptive_gain
        signature = canonical_minimal_separator_signature(task)
        predicted = signature == MINIMAL_STRICT_GAIN_SIGNATURE
        strict += int(exact)
        normal_form += int(predicted)
        false_positive += int(predicted and not exact)
        false_negative += int(exact and not predicted)
        if exact:
            strict_signatures.add(signature)
    assert strict == 192
    assert normal_form == 192
    assert false_positive == 0
    assert false_negative == 0
    assert strict_signatures == {MINIMAL_STRICT_GAIN_SIGNATURE}


def test_scope_rejects_unbalanced_target_multiplicity():
    task = FiniteTask(
        (World("a", 0), World("b", 0), World("c", 0), World("d", 1)),
        (
            Query("q0", 1, (0, 0, 0, 1)),
            Query("q1", 1, (0, 0, 1, 0)),
            Query("q2", 1, (0, 1, 0, 0)),
        ),
    )
    try:
        canonical_minimal_separator_signature(task)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError outside 2+2 minimal scope")
