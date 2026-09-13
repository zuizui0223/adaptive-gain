"""Published-fit anchor for the Voje et al. (2024) C. andinus OUBM result.

This module deliberately separates two evidential levels:

1. a *published-fit witness*, which takes the reported sample size, parameter
   count, AICc, and half-life as fixed published summaries; and
2. an *independent raw-data refit*, which is not claimed here and remains a
   separate gate until the archived data and analysis script are executed.

The reciprocal-congruence theorem proved elsewhere in this package acts on the
fitted observed-trait law.  Therefore a published-fit witness is already enough
to demonstrate non-uniqueness of the mechanistic half-life interpretation
conditional on the reported OUBM fit, while not pretending to reproduce the
optimization from raw observations.
"""

from __future__ import annotations

from dataclasses import dataclass

from .adaptation_halflife_identifiability import direct_half_life_from_reported


VOJE_ANDINUS_N = 266
VOJE_OUBM_K = 4
VOJE_OUBM_AICC = -153.573
VOJE_OUBM_AICC_WEIGHT = 1.0
VOJE_REPORTED_HALF_LIFE_YEARS = 12.0
VOJE_REPORTED_STATIONARY_VARIANCE = 0.015


@dataclass(frozen=True)
class PublishedFitWitness:
    """One reciprocal member attached to the published C. andinus fit."""

    response_fraction: float
    published_aicc: float
    implied_log_likelihood: float
    reported_half_life_years: float
    direct_trait_half_life_years: float


def aicc(log_likelihood: float, k: int, n: int) -> float:
    """Small-sample corrected AIC under the standard AICc convention."""

    if k < 0:
        raise ValueError("k must be non-negative")
    if n <= k + 1:
        raise ValueError("AICc requires n > k + 1")
    correction = 2.0 * k * (k + 1) / (n - k - 1)
    return -2.0 * float(log_likelihood) + 2.0 * k + correction


def log_likelihood_from_aicc(aicc_value: float, k: int, n: int) -> float:
    """Invert the standard AICc formula for a reported AICc value."""

    if k < 0:
        raise ValueError("k must be non-negative")
    if n <= k + 1:
        raise ValueError("AICc requires n > k + 1")
    correction = 2.0 * k * (k + 1) / (n - k - 1)
    return (2.0 * k + correction - float(aicc_value)) / 2.0


def published_andinus_log_likelihood() -> float:
    """Implied log-likelihood from the published AICc, K, and n summaries."""

    return log_likelihood_from_aicc(
        VOJE_OUBM_AICC,
        VOJE_OUBM_K,
        VOJE_ANDINUS_N,
    )


def reciprocal_direct_half_life_years(response_fraction: float) -> float:
    """Direct-response half-life for a congruent reciprocal realization."""

    return direct_half_life_from_reported(
        VOJE_REPORTED_HALF_LIFE_YEARS,
        response_fraction,
    )


def published_fit_witness(response_fraction: float) -> PublishedFitWitness:
    """Attach a reciprocal causal interpretation to the published OUBM fit.

    The observed-trait likelihood and therefore the reported model-fit score are
    unchanged by the exact congruence construction; only the mechanistic
    decomposition of the fitted relaxation rate changes.
    """

    direct_half = reciprocal_direct_half_life_years(response_fraction)
    return PublishedFitWitness(
        response_fraction=float(response_fraction),
        published_aicc=VOJE_OUBM_AICC,
        implied_log_likelihood=published_andinus_log_likelihood(),
        reported_half_life_years=VOJE_REPORTED_HALF_LIFE_YEARS,
        direct_trait_half_life_years=direct_half,
    )
