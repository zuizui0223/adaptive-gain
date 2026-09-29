"""Exact detection-effort identities for observed binary link transitions.

These functions describe the observation map for a latent link that is
persistent across two periods. They do not model ecological gain or loss.

For any two binary observations Y_previous and Y_current, no independence
assumption is needed for the conservation identity

P(0 -> 1) - P(1 -> 0)
= P(Y_current = 1) - P(Y_previous = 1).

For a persistent latent link, if q_previous and q_current are the marginal
probabilities of detecting the link at least once in the two periods, the
right-hand side is q_current - q_previous.

The separate product formulas

P(observed gain) = (1 - q_previous) * q_current
P(observed loss) = q_previous * (1 - q_current)

require conditional independence of the two period-level detection events
given the persistent latent link. The gain/loss odds-ratio identity has the
same requirement.

With independent per-census detection p and n censuses,
q = 1 - (1 - p)**n.
"""

from __future__ import annotations

import math


def binary_transition_conservation(
    p00: float,
    p01: float,
    p10: float,
    p11: float,
) -> dict[str, float]:
    """Exact two-time binary flow identity, with no independence assumption.

    States use previous/current ordering: p01 is observed gain and p10 is
    observed loss.
    """
    probabilities = [float(p00), float(p01), float(p10), float(p11)]
    if any(value < 0.0 or value > 1.0 for value in probabilities):
        raise ValueError("joint probabilities must be in [0, 1]")
    if not math.isclose(sum(probabilities), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("joint probabilities must sum to 1")

    previous_presence = probabilities[2] + probabilities[3]
    current_presence = probabilities[1] + probabilities[3]
    return {
        "gain_minus_loss": probabilities[1] - probabilities[2],
        "current_minus_previous_presence": (
            current_presence - previous_presence
        ),
        "previous_presence": previous_presence,
        "current_presence": current_presence,
    }


def period_detection_probability(
    per_census_detection: float,
    census_count: int,
) -> float:
    """Probability of at least one detection in a period."""
    p = float(per_census_detection)
    n = int(census_count)
    if not 0.0 <= p <= 1.0:
        raise ValueError("per_census_detection must be in [0, 1]")
    if n < 0:
        raise ValueError("census_count must be non-negative")
    return 1.0 - (1.0 - p) ** n


def persistent_observed_transition_probabilities(
    q_previous: float,
    q_current: float,
) -> dict[str, float]:
    """Observed transition probabilities under period-level conditional independence.

    The difference identity q_current-q_previous is more general and does not
    itself require this independence assumption; this function additionally
    supplies the individual joint-cell probabilities using the product model.
    """
    q1 = float(q_previous)
    q2 = float(q_current)
    if not 0.0 <= q1 <= 1.0 or not 0.0 <= q2 <= 1.0:
        raise ValueError("period detection probabilities must be in [0, 1]")

    gain = (1.0 - q1) * q2
    loss = q1 * (1.0 - q2)
    stable_present = q1 * q2
    stable_absent = (1.0 - q1) * (1.0 - q2)

    return {
        "gain": gain,
        "loss": loss,
        "stable_present": stable_present,
        "stable_absent": stable_absent,
        "gain_minus_loss": gain - loss,
        "q_current_minus_q_previous": q2 - q1,
    }


def persistent_transition_from_census_effort(
    *,
    p_previous: float,
    n_previous: int,
    p_current: float,
    n_current: int,
) -> dict[str, float]:
    """Apply the exact identity from per-census detection and census counts."""
    q_previous = period_detection_probability(p_previous, n_previous)
    q_current = period_detection_probability(p_current, n_current)
    out = persistent_observed_transition_probabilities(
        q_previous,
        q_current,
    )
    return {
        "q_previous": q_previous,
        "q_current": q_current,
        **out,
    }


def observed_gain_log_odds_vs_loss(
    q_previous: float,
    q_current: float,
) -> float:
    """log[P(gain)/P(loss)] for a persistent link.

    Returns +/-inf at deterministic boundaries.
    """
    probs = persistent_observed_transition_probabilities(
        q_previous,
        q_current,
    )
    gain = probs["gain"]
    loss = probs["loss"]
    if gain == 0.0 and loss == 0.0:
        return 0.0
    if loss == 0.0:
        return math.inf
    if gain == 0.0:
        return -math.inf
    return math.log(gain / loss)



def dynamic_latent_observed_transition_table(
    *,
    psi_previous: float,
    colonization: float,
    extinction: float,
    q_previous: float,
    q_current: float,
) -> dict[str, float]:
    """Observed 2x2 table under a two-season latent-state/detection model.

    Assumes no false positives and period-level conditional independence of
    detection given latent states.
    """
    values = (
        float(psi_previous),
        float(colonization),
        float(extinction),
        float(q_previous),
        float(q_current),
    )
    if any(value < 0.0 or value > 1.0 for value in values):
        raise ValueError("all probabilities must be in [0, 1]")

    psi1, gamma, epsilon, q1, q2 = values
    psi2 = psi1 * (1.0 - epsilon) + (1.0 - psi1) * gamma

    observed_previous = psi1 * q1
    observed_current = psi2 * q2
    stable_present = psi1 * (1.0 - epsilon) * q1 * q2
    loss = observed_previous - stable_present
    gain = observed_current - stable_present
    stable_absent = 1.0 - stable_present - loss - gain

    return {
        "stable_absent": stable_absent,
        "gain": gain,
        "loss": loss,
        "stable_present": stable_present,
        "latent_previous": psi1,
        "latent_current": psi2,
        "latent_change": psi2 - psi1,
        "observed_previous": observed_previous,
        "observed_current": observed_current,
    }
