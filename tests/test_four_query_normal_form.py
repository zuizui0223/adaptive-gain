from fractions import Fraction

from adaptive_gain import Query
from adaptive_gain.four_query_normal_form import (
    FOUR_QUERY_STRICT_EXTENSION_SIGNATURES,
    enumerate_balanced_four_query_universe,
    four_query_normal_form_receipt,
)
from adaptive_gain.minimal_normal_form import minimal_strict_gain_standard_task
from adaptive_gain.core import FiniteTask


def _extend_standard(kind: str) -> FiniteTask:
    base = minimal_strict_gain_standard_task()
    if kind == "null":
        extra = Query("q_extra_null", 1, (0, 0, 0, 0))
    elif kind == "terminal":
        extra = Query("q_extra_terminal", 1, base.queries[0].outcomes)
    elif kind == "routing":
        extra = Query("q_extra_routing", 1, base.queries[1].outcomes)
    else:
        raise ValueError(kind)
    return FiniteTask(base.worlds, base.queries + (extra,))


def test_three_registered_four_query_extensions_have_expected_normal_forms():
    null = four_query_normal_form_receipt(_extend_standard("null"))
    terminal = four_query_normal_form_receipt(_extend_standard("terminal"))
    routing = four_query_normal_form_receipt(_extend_standard("routing"))

    assert null.canonical_separator_signature == (0, 3, 5, 9)
    assert null.extension_class == "null_query_extension"
    assert null.strict_three_query_deletion_count == 1

    assert terminal.canonical_separator_signature == (3, 3, 5, 9)
    assert terminal.extension_class == "duplicate_terminal_extension"
    assert terminal.strict_three_query_deletion_count == 2

    assert routing.canonical_separator_signature == (3, 5, 9, 9)
    assert routing.extension_class == "duplicate_routing_extension"
    assert routing.strict_three_query_deletion_count == 2

    for receipt in (null, terminal, routing):
        assert receipt.matches_strict_extension_normal_form
        assert receipt.exact_strict_gain
        assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
        assert receipt.classification_agrees_with_exact_solver


def test_complete_65536_four_query_universe_has_only_three_reducible_strict_extensions():
    summary = enumerate_balanced_four_query_universe()
    assert summary.total_tasks == 65_536
    assert summary.unresolved_tasks == 14_896
    assert dict(summary.cost_pair_counts) == {
        "1:1": 27_120,
        "2:2": 19_680,
        "2:3": 3_840,
        "None:None": 14_896,
    }
    assert summary.strict_gain_tasks == 3_840
    assert dict(summary.strict_extension_class_counts) == {
        "duplicate_routing_extension": 768,
        "duplicate_terminal_extension": 1_536,
        "null_query_extension": 1_536,
    }
    assert dict(summary.strict_deletion_count_distribution) == {
        1: 1_536,
        2: 2_304,
    }
    assert summary.all_strict_tasks_have_minimal_strict_deletion
    assert summary.strict_gain_cost_pairs == ((2, 3),)
    assert summary.maximum_strict_cost_ratio == Fraction(3, 2)
    assert summary.classification_disagreement_count == 0
    assert set(FOUR_QUERY_STRICT_EXTENSION_SIGNATURES) == {
        (0, 3, 5, 9),
        (3, 3, 5, 9),
        (3, 5, 9, 9),
    }
