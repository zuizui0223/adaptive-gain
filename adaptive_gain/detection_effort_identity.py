"""Exact detection-effort identities for observed binary link transitions.

These functions describe the observation map for a latent link that is
persistent across two periods. They do not model ecological gain or loss.

If q_previous and q_current are the probabilities of detecting the persistent
link at least once in the two periods, then:

P(observed gain) = (1 - q_previous) * q_current
P(observed loss) = q_previous * (1 - q_current)

and therefore

P(observed gain) - P(observed loss) = q_current - q_previous.

With independent per-census detection p and n censuses,
q = 1 - (1 - p)**n.
"""

from __future__ import annotations

import math


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
    """Observed binary transition probabilities for a persistent latent link."""
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
