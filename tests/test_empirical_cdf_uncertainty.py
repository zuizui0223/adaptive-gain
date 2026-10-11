"""Targeted sampling-uncertainty checks for the published Uehara binned counts.

These tests intentionally use only frozen individual-count receipts, not the
raw spreadsheet. The comparisons are exploratory, not confirmatory.
"""
import json
from pathlib import Path

import pytest

from adaptive_gain.empirical_cdf_uncertainty import (
    compare_cdfs,
    fisher_exact_two_sided,
    wilson_interval,
)


def test_anopheles_sample_cdf_crossing_has_large_sampling_uncertainty():
    minute_one = compare_cdfs(12, 14, 15, 18)
    minute_four = compare_cdfs(12, 14, 16, 18)
    assert minute_one.difference == pytest.approx(0.023809523809523725)
    assert minute_four.difference == pytest.approx(-0.031746031746031744)
    assert minute_one.fisher_two_sided_p == pytest.approx(1.0)
    assert minute_four.fisher_two_sided_p == pytest.approx(1.0)

    for result in (minute_one, minute_four):
        first_lo, first_hi = result.first_wilson95
        second_lo, second_hi = result.second_wilson95
        assert max(first_lo, second_lo) < min(first_hi, second_hi)


def test_larger_species_contrast_is_supported_at_first_minute():
    gambiae_vs_albopictus = compare_cdfs(12, 14, 10, 38)
    aegypti_vs_albopictus = compare_cdfs(18, 28, 10, 38)
    assert gambiae_vs_albopictus.difference == pytest.approx(0.593984962406015)
    assert gambiae_vs_albopictus.fisher_two_sided_p == pytest.approx(
        0.00024983858870414826
    )
    assert aegypti_vs_albopictus.fisher_two_sided_p == pytest.approx(
        0.0027053452731295533
    )


def test_wilson_boundary_counts_are_valid():
    lo, hi = wilson_interval(0, 10)
    assert lo >= 0.0
    assert 0.0 < hi < 0.5
    lo, hi = wilson_interval(10, 10)
    assert lo > 0.5
    assert hi <= 1.0 + 1e-12


def test_fisher_exact_two_sided_is_symmetric():
    assert fisher_exact_two_sided(12, 14, 15, 18) == pytest.approx(
        fisher_exact_two_sided(15, 18, 12, 14)
    )


def test_invalid_counts_are_rejected():
    with pytest.raises(ValueError):
        wilson_interval(11, 10)
    with pytest.raises(ValueError):
        compare_cdfs(5, 4, 0, 2)



def test_uncertainty_receipt_matches_frozen_individual_event_counts():
    root = Path(__file__).resolve().parents[1]
    source = json.loads(
        (root / "validation" / "uehara_binned_first_probe_v1.json").read_text()
    )
    audit = json.loads(
        (root / "validation" / "uehara_cdf_uncertainty_v1.json").read_text()
    )

    def first_k(name, minute):
        data = source["species"][name]
        return (
            sum(data["first_probe_interval_counts"][:minute]),
            data["n_primary"],
        )

    scenarios = (
        ("Anopheles gambiae", "Anopheles stephensi", 1),
        ("Anopheles gambiae", "Anopheles stephensi", 4),
        ("Anopheles gambiae", "Aedes albopictus", 1),
        ("Aedes aegypti", "Aedes albopictus", 1),
    )
    for frozen, (first, second, minute) in zip(audit["comparisons"], scenarios):
        k1, n1 = first_k(first, minute)
        k2, n2 = first_k(second, minute)
        observed = compare_cdfs(k1, n1, k2, n2)
        assert frozen["minute_end"] == minute
        assert frozen["first"]["k"] == k1
        assert frozen["first"]["n"] == n1
        assert frozen["second"]["k"] == k2
        assert frozen["second"]["n"] == n2
        assert frozen["fraction_difference"] == pytest.approx(observed.difference)
        assert frozen["fisher_two_sided_p"] == pytest.approx(
            observed.fisher_two_sided_p
        )
