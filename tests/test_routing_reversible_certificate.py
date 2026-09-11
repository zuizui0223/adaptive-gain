from __future__ import annotations

from fractions import Fraction

import pytest

from adaptive_gain.routing_reversible_certificate import (
    RepresentationCertificateError,
    ReversibleMutationCertificate,
    full_phase_is_modal_from_certificate,
    neutral_layer_masses,
    representation_certificate_receipt,
    selected_detailed_balance_holds,
    selected_layer_distribution_from_tilt,
    selected_stationary_distribution,
    selected_stationary_flow,
    shortest_support_distance_to_gain,
    validate_reversible_mutation_certificate,
)


def _uniform_gain_chain_q2() -> ReversibleMutationCertificate:
    return ReversibleMutationCertificate(
        gains=(0, 1, 2),
        proposal=(
            (Fraction(1, 2), Fraction(1, 2), Fraction(0, 1)),
            (Fraction(1, 2), Fraction(0, 1), Fraction(1, 2)),
            (Fraction(0, 1), Fraction(1, 2), Fraction(1, 2)),
        ),
        neutral_measure=(Fraction(1, 3),) * 3,
        start_state=0,
    )


def _biased_gain_chain_q2() -> ReversibleMutationCertificate:
    return ReversibleMutationCertificate(
        gains=(0, 1, 2),
        proposal=(
            (Fraction(1, 2), Fraction(1, 2), Fraction(0, 1)),
            (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
            (Fraction(0, 1), Fraction(1, 2), Fraction(1, 2)),
        ),
        neutral_measure=(Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
        start_state=0,
    )


def _uniform_four_state_path() -> ReversibleMutationCertificate:
    return ReversibleMutationCertificate(
        gains=(0, 0, 1, 2),
        proposal=(
            (Fraction(3, 4), Fraction(1, 4), 0, 0),
            (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4), 0),
            (0, Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)),
            (0, 0, Fraction(1, 4), Fraction(3, 4)),
        ),
        neutral_measure=(Fraction(1, 4),) * 4,
        start_state=0,
    )


def _uniform_four_state_shortcut() -> ReversibleMutationCertificate:
    return ReversibleMutationCertificate(
        gains=(0, 0, 1, 2),
        proposal=(
            (Fraction(1, 2), Fraction(1, 4), 0, Fraction(1, 4)),
            (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4), 0),
            (0, Fraction(1, 4), Fraction(3, 4), 0),
            (Fraction(1, 4), 0, 0, Fraction(3, 4)),
        ),
        neutral_measure=(Fraction(1, 4),) * 4,
        start_state=0,
    )


def _q1_branch_product_certificate() -> ReversibleMutationCertificate:
    # States: (0,0),(0,1),(1,0),(1,1); gain=min coordinate.
    return ReversibleMutationCertificate(
        gains=(0, 0, 0, 1),
        proposal=(
            (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), 0),
            (Fraction(1, 4), Fraction(1, 2), 0, Fraction(1, 4)),
            (Fraction(1, 4), 0, Fraction(1, 2), Fraction(1, 4)),
            (0, Fraction(1, 4), Fraction(1, 4), Fraction(1, 2)),
        ),
        neutral_measure=(Fraction(1, 4),) * 4,
        start_state=0,
    )


def test_nonuniform_reversible_kernel_has_exact_selected_stationary_law() -> None:
    cert = _biased_gain_chain_q2()
    validate_reversible_mutation_certificate(cert)
    assert neutral_layer_masses(cert) == (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4))

    # N=2, a=2 -> theta=2.  mu*theta^g gives raw weights (1/4,1,1).
    expected = (Fraction(1, 9), Fraction(4, 9), Fraction(4, 9))
    assert selected_stationary_distribution(cert, 2, 2) == expected
    assert selected_stationary_flow(cert, 2, 2) == expected
    assert selected_detailed_balance_holds(cert, 2, 2) is True


def test_raw_multiplicity_is_not_enough_when_neutral_mutation_measure_is_biased() -> None:
    uniform = _uniform_gain_chain_q2()
    biased = _biased_gain_chain_q2()
    # Both have one genotype per gain level.  Only the neutral mutation measure differs.
    assert tuple(uniform.gains.count(r) for r in range(3)) == (1, 1, 1)
    assert tuple(biased.gains.count(r) for r in range(3)) == (1, 1, 1)

    assert selected_layer_distribution_from_tilt(uniform, 2) == (
        Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)
    )
    assert selected_layer_distribution_from_tilt(biased, 2) == (
        Fraction(1, 9), Fraction(4, 9), Fraction(4, 9)
    )
    assert full_phase_is_modal_from_certificate(uniform, 2) is True
    assert full_phase_is_modal_from_certificate(biased, 2) is True  # tied with gain 1


def test_support_graph_and_neutral_layer_mass_are_independent_representation_coordinates() -> None:
    path = _uniform_four_state_path()
    shortcut = _uniform_four_state_shortcut()
    assert neutral_layer_masses(path) == neutral_layer_masses(shortcut) == (
        Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)
    )
    assert selected_layer_distribution_from_tilt(path, 3) == selected_layer_distribution_from_tilt(shortcut, 3)

    # Same gains and same neutral mutation masses, but topology alone changes access.
    assert shortest_support_distance_to_gain(path, 2) == 3
    assert shortest_support_distance_to_gain(shortcut, 2) == 1


def test_uniform_symmetric_special_case_recovers_q1_branch_product_degeneracy() -> None:
    cert = _q1_branch_product_certificate()
    assert neutral_layer_masses(cert) == (Fraction(3, 4), Fraction(1, 4))
    # Multiplying by the common factor 4 recovers genotype counts (3,1).
    assert selected_layer_distribution_from_tilt(cert, 8) == (Fraction(3, 11), Fraction(8, 11))
    assert full_phase_is_modal_from_certificate(cert, 2) is False
    assert full_phase_is_modal_from_certificate(cert, 3) is True
    assert shortest_support_distance_to_gain(cert, 1) == 2


def test_receipt_separates_accessibility_from_stationary_occupancy() -> None:
    cert = _uniform_four_state_shortcut()
    receipt = representation_certificate_receipt(cert, population_size=3, fitness_step=2)
    assert receipt.required_gap == 2
    assert receipt.state_count == 4
    assert receipt.neutral_layer_masses == (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))
    assert receipt.shortest_distances == (0, 1, 1)
    assert receipt.selected_stationary_verified is True


def test_validation_rejects_nonreversible_or_disconnected_certificates() -> None:
    bad_reversibility = ReversibleMutationCertificate(
        gains=(0, 1),
        proposal=((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 4), Fraction(3, 4))),
        neutral_measure=(Fraction(1, 2), Fraction(1, 2)),
        start_state=0,
    )
    with pytest.raises(RepresentationCertificateError, match="not reversible"):
        validate_reversible_mutation_certificate(bad_reversibility)

    disconnected = ReversibleMutationCertificate(
        gains=(0, 1),
        proposal=((1, 0), (0, 1)),
        neutral_measure=(Fraction(1, 2), Fraction(1, 2)),
        start_state=0,
    )
    with pytest.raises(RepresentationCertificateError, match="connected"):
        validate_reversible_mutation_certificate(disconnected)


def test_validation_rejects_missing_gain_level_and_bad_target() -> None:
    missing = ReversibleMutationCertificate(
        gains=(0, 2),
        proposal=((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 2), Fraction(1, 2))),
        neutral_measure=(Fraction(1, 2), Fraction(1, 2)),
        start_state=0,
    )
    with pytest.raises(RepresentationCertificateError, match="every gain level"):
        validate_reversible_mutation_certificate(missing)
    with pytest.raises(ValueError, match=r"\[0,q\]"):
        shortest_support_distance_to_gain(_uniform_gain_chain_q2(), 3)
