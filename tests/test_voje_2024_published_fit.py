import math

import pytest

from adaptive_gain.voje_2024_published_fit import (
    VOJE_ANDINUS_N,
    VOJE_OUBM_AICC,
    VOJE_OUBM_K,
    VOJE_REPORTED_HALF_LIFE_YEARS,
    aicc,
    log_likelihood_from_aicc,
    published_andinus_log_likelihood,
    published_fit_witness,
    reciprocal_direct_half_life_years,
)


def test_published_aicc_round_trip():
    log_likelihood = published_andinus_log_likelihood()
    assert log_likelihood == pytest.approx(80.86312835249042)
    assert aicc(log_likelihood, VOJE_OUBM_K, VOJE_ANDINUS_N) == pytest.approx(
        VOJE_OUBM_AICC
    )


def test_reciprocal_half_life_witnesses():
    assert reciprocal_direct_half_life_years(0.5) == pytest.approx(24.0)
    assert reciprocal_direct_half_life_years(0.25) == pytest.approx(48.0)
    assert reciprocal_direct_half_life_years(0.1) == pytest.approx(120.0)


def test_published_fit_witness_preserves_fit_summary():
    witness = published_fit_witness(0.5)
    assert witness.published_aicc == VOJE_OUBM_AICC
    assert witness.reported_half_life_years == VOJE_REPORTED_HALF_LIFE_YEARS
    assert witness.direct_trait_half_life_years == pytest.approx(24.0)
    assert witness.implied_log_likelihood == pytest.approx(
        published_andinus_log_likelihood()
    )


def test_aicc_validation():
    with pytest.raises(ValueError):
        aicc(0.0, -1, 10)
    with pytest.raises(ValueError):
        aicc(0.0, 4, 5)
    with pytest.raises(ValueError):
        log_likelihood_from_aicc(0.0, 4, 5)


def test_response_fraction_validation_is_inherited():
    for q in (0.0, 1.0, -0.1, 1.1):
        with pytest.raises(ValueError):
            reciprocal_direct_half_life_years(q)


def test_lower_endpoint_is_the_reported_half_life():
    values = [reciprocal_direct_half_life_years(q) for q in (0.9, 0.5, 0.1)]
    assert all(value > VOJE_REPORTED_HALF_LIFE_YEARS for value in values)
    assert math.isclose(
        reciprocal_direct_half_life_years(0.999999),
        VOJE_REPORTED_HALF_LIFE_YEARS / 0.999999,
    )
