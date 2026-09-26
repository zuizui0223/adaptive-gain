import pytest

from adaptive_gain.empirical_rewiring import (
    adjacent_transition_series,
    network_from_rows,
    networks_by_period_from_rows,
    transition_rewiring_receipt,
)


def test_pure_shared_species_link_change_is_rewiring():
    previous = {("p1", "q1"): 2, ("p2", "q2"): 1}
    current = {("p1", "q2"): 4, ("p2", "q1"): 3}

    receipt = transition_rewiring_receipt(previous, current)

    assert receipt.shared_plant_count == 2
    assert receipt.shared_pollinator_count == 2
    assert receipt.shared_species_dyad_count == 4
    assert receipt.shared_species_rewiring_count == 4
    assert receipt.species_turnover_link_count == 0
    assert receipt.total_link_turnover_count == 4
    assert receipt.link_jaccard_dissimilarity == 1.0
    assert receipt.exact_partition


def test_pure_species_replacement_is_not_called_rewiring():
    previous = {("old_plant", "old_pollinator"): 1}
    current = {("new_plant", "new_pollinator"): 1}

    receipt = transition_rewiring_receipt(previous, current)

    assert receipt.shared_species_dyad_count == 0
    assert receipt.shared_species_rewiring_count == 0
    assert receipt.species_turnover_link_count == 2
    assert receipt.rewiring_opportunity_rate is None
    assert receipt.exact_partition


def test_mixed_turnover_partition_is_exact():
    previous = {
        ("p1", "q1"): 1,
        ("p2", "q2"): 1,
        ("old", "q1"): 1,
    }
    current = {
        ("p1", "q2"): 1,
        ("p2", "q1"): 1,
        ("new", "q1"): 1,
    }

    receipt = transition_rewiring_receipt(previous, current)

    assert receipt.shared_species_rewiring_count == 4
    assert receipt.species_turnover_link_count == 2
    assert receipt.total_link_turnover_count == 6
    assert receipt.shared_species_rewiring_fraction_of_union == pytest.approx(4 / 6)
    assert receipt.species_turnover_fraction_of_union == pytest.approx(2 / 6)
    assert receipt.exact_partition


def test_compatibility_mask_is_opportunity_qc_not_response_filter():
    previous = {("p1", "q1"): 1, ("p2", "q2"): 1}
    current = {("p1", "q2"): 1, ("p2", "q1"): 1}
    permitted = {
        ("p1", "q1"),
        ("p1", "q2"),
        ("p2", "q1"),
    }

    receipt = transition_rewiring_receipt(
        previous,
        current,
        permitted_dyads=permitted,
    )

    assert receipt.shared_species_rewiring_count == 4
    assert receipt.permitted_shared_dyad_count == 3
    assert receipt.changed_shared_outside_permitted_count == 1
    assert receipt.rewiring_opportunity_rate == 1.0


def test_network_row_builders_sum_duplicate_dyads_and_drop_zeroes():
    network = network_from_rows(
        [
            ("p1", "q1", 2),
            ("p1", "q1", 3),
            ("p2", "q2", 0),
        ]
    )
    assert network == {("p1", "q1"): 5.0}

    networks = networks_by_period_from_rows(
        [
            (2006, "p1", "q1", 2),
            (2006, "p1", "q1", 1),
            (2007, "p1", "q2", 4),
        ]
    )
    assert networks == {
        2006: {("p1", "q1"): 3.0},
        2007: {("p1", "q2"): 4.0},
    }


def test_invalid_weights_are_rejected():
    with pytest.raises(ValueError):
        network_from_rows([("p1", "q1", -1)])
    with pytest.raises(ValueError):
        transition_rewiring_receipt({("p1", "q1"): float("nan")}, {})


def test_adjacent_series_uses_frozen_period_order():
    networks = {
        2006: {("p1", "q1"): 1, ("p2", "q2"): 1},
        2007: {("p1", "q2"): 1, ("p2", "q1"): 1},
        2008: {("p1", "q1"): 1, ("p2", "q2"): 1},
    }

    series = adjacent_transition_series(
        networks,
        period_order=(2006, 2007, 2008),
    )

    assert [(row.previous_period, row.current_period) for row in series] == [
        (2006, 2007),
        (2007, 2008),
    ]
    assert all(row.receipt.shared_species_rewiring_count == 4 for row in series)


def test_adjacent_series_rejects_duplicate_or_missing_periods():
    networks = {2006: {("p1", "q1"): 1}, 2007: {("p1", "q1"): 1}}
    with pytest.raises(ValueError):
        adjacent_transition_series(networks, period_order=(2006, 2006))
    with pytest.raises(ValueError):
        adjacent_transition_series(networks, period_order=(2006, 2008))
