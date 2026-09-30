import math
from fractions import Fraction

from adaptive_gain.detection_effort_identity import (
    dynamic_latent_observed_transition_table,
)


def _fraction_table(psi, gamma, epsilon, q1, q2):
    psi2 = psi * (1 - epsilon) + (1 - psi) * gamma
    m1 = psi * q1
    m2 = psi2 * q2
    p11 = psi * (1 - epsilon) * q1 * q2
    p10 = m1 - p11
    p01 = m2 - p11
    p00 = 1 - p11 - p10 - p01
    return {
        "stable_absent": p00,
        "gain": p01,
        "loss": p10,
        "stable_present": p11,
        "latent_previous": psi,
        "latent_current": psi2,
        "latent_change": psi2 - psi,
    }


def test_exact_opposite_direction_witness_with_fractions():
    increase = _fraction_table(
        Fraction(1, 4),
        Fraction(7, 18),
        Fraction(1, 6),
        Fraction(4, 5),
        Fraction(3, 5),
    )
    decrease = _fraction_table(
        Fraction(1, 2),
        Fraction(1, 8),
        Fraction(3, 8),
        Fraction(2, 5),
        Fraction(4, 5),
    )

    expected = {
        "stable_absent": Fraction(3, 5),
        "gain": Fraction(1, 5),
        "loss": Fraction(1, 10),
        "stable_present": Fraction(1, 10),
    }
    for key, value in expected.items():
        assert increase[key] == value
        assert decrease[key] == value

    assert increase["latent_change"] == Fraction(1, 4)
    assert decrease["latent_change"] == -Fraction(1, 8)

    for row in (increase, decrease):
        for key in ("latent_previous", "latent_current"):
            assert Fraction(0, 1) < row[key] < Fraction(1, 1)


def test_implementation_reproduces_same_observed_table_with_opposite_latent_change():
    increase = dynamic_latent_observed_transition_table(
        psi_previous=1 / 4,
        colonization=7 / 18,
        extinction=1 / 6,
        q_previous=4 / 5,
        q_current=3 / 5,
    )
    decrease = dynamic_latent_observed_transition_table(
        psi_previous=1 / 2,
        colonization=1 / 8,
        extinction=3 / 8,
        q_previous=2 / 5,
        q_current=4 / 5,
    )

    for key, expected in (
        ("stable_absent", 3 / 5),
        ("gain", 1 / 5),
        ("loss", 1 / 10),
        ("stable_present", 1 / 10),
    ):
        assert math.isclose(increase[key], expected, abs_tol=1e-14)
        assert math.isclose(decrease[key], expected, abs_tol=1e-14)
        assert math.isclose(increase[key], decrease[key], abs_tol=1e-14)

    assert increase["latent_change"] > 0
    assert decrease["latent_change"] < 0


def test_same_observed_prevalence_increase_can_hide_opposite_latent_directions():
    increase = dynamic_latent_observed_transition_table(
        psi_previous=1 / 4,
        colonization=7 / 18,
        extinction=1 / 6,
        q_previous=4 / 5,
        q_current=3 / 5,
    )
    decrease = dynamic_latent_observed_transition_table(
        psi_previous=1 / 2,
        colonization=1 / 8,
        extinction=3 / 8,
        q_previous=2 / 5,
        q_current=4 / 5,
    )

    for row in (increase, decrease):
        assert row["observed_current"] > row["observed_previous"]

    assert increase["latent_current"] > increase["latent_previous"]
    assert decrease["latent_current"] < decrease["latent_previous"]


def test_opposite_direction_witness_is_strictly_interior():
    parameterizations = (
        (
            Fraction(1, 4),
            Fraction(7, 18),
            Fraction(1, 6),
            Fraction(4, 5),
            Fraction(3, 5),
        ),
        (
            Fraction(1, 2),
            Fraction(1, 8),
            Fraction(3, 8),
            Fraction(2, 5),
            Fraction(4, 5),
        ),
    )
    for params in parameterizations:
        assert all(Fraction(0, 1) < value < Fraction(1, 1) for value in params)
