"""Minimal closed community -> selection -> evolution -> community feedback.

This module adds one endogenous layer on top of the evolutionary-timescale
branch.  Two recurrent community states carry exact structural selection rewards
from finite sensing tasks.  The evolving contingent-architecture frequency p_t
changes the target occupancy of the high-opportunity community state, while the
current community occupancy q_t determines selection on p_t.

Let

    q_target(p) = q_base + eta * (p - 1/2),

with 0 <= q_target(p) <= 1 for all p in [0,1].  Community memory phi in [0,1)
relaxes occupancy toward that phenotype-dependent target:

    q_{t+1} = phi*q_t + (1-phi)*q_target(p_t).

If state-specific log-fitness rewards are s_low and s_high, evolution obeys the
exact haploid log-odds update

    logit(p_{t+1}) = logit(p_t) + s_low + (s_high-s_low)*q_t.

For an interior equilibrium, selection must vanish at

    q_star = -s_low / (s_high-s_low),

and ecological feedback must satisfy q_target(p_star)=q_star.

In coordinates (z=logit(p), q), the Jacobian is

    J = [[1, Delta_s],
         [(1-phi)*eta*p_star*(1-p_star), phi]].

The generic Jury conditions give local discrete-time stability.  When
Delta_s>0, 0<=phi<1, and the equilibrium is interior, they reduce to

    -1 / [Delta_s*p_star*(1-p_star)] < eta < 0.

Thus negative eco-evolutionary feedback stabilizes the interior equilibrium;
positive feedback destabilizes it; excessively strong negative feedback can
overshoot.  Community memory phi changes transient eigenvalues but not that
stability interval.

These feedback facts are standard dynamical-systems consequences.  The
repository-specific input is that s_low and s_high are generated from exact
adaptive/fixed sensing tasks.
"""

from __future__ import annotations

from cmath import sqrt as complex_sqrt
from dataclasses import dataclass
from math import isfinite

from .core import FiniteTask
from .structural_eco_evolution import (
    structural_selection_state,
    update_frequency_by_log_fitness_ratio,
)

_TOL = 1e-12


def _validate_feedback_geometry(
    q_base: float,
    feedback_strength: float,
    community_memory: float,
) -> tuple[float, float, float]:
    q0 = float(q_base)
    eta = float(feedback_strength)
    phi = float(community_memory)
    if not isfinite(q0) or not 0.0 <= q0 <= 1.0:
        raise ValueError("q_base must lie in [0,1]")
    if not isfinite(eta):
        raise ValueError("feedback_strength must be finite")
    if not isfinite(phi) or not 0.0 <= phi < 1.0:
        raise ValueError("community_memory must lie in [0,1)")
    q_min = q0 - abs(eta) / 2.0
    q_max = q0 + abs(eta) / 2.0
    if q_min < -_TOL or q_max > 1.0 + _TOL:
        raise ValueError(
            "q_base and feedback_strength must keep q_target(p) in [0,1] "
            "for every p in [0,1]"
        )
    return q0, eta, phi


def target_high_state_occupancy(
    phenotype_frequency: float,
    *,
    q_base: float,
    feedback_strength: float,
) -> float:
    p = float(phenotype_frequency)
    q0 = float(q_base)
    eta = float(feedback_strength)
    if not 0.0 <= p <= 1.0:
        raise ValueError("phenotype_frequency must lie in [0,1]")
    _validate_feedback_geometry(q0, eta, 0.0)
    value = q0 + eta * (p - 0.5)
    if value < 0.0 and abs(value) <= _TOL:
        value = 0.0
    if value > 1.0 and abs(value - 1.0) <= _TOL:
        value = 1.0
    return value


def phenotype_dependent_transition_matrix(
    phenotype_frequency: float,
    *,
    q_base: float,
    feedback_strength: float,
    community_memory: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Two-state transition matrix with stationary high-state occupancy q_target(p).

    States are ordered (low, high).  The nonstationary eigenvalue is exactly
    ``community_memory``.
    """

    q0, eta, phi = _validate_feedback_geometry(
        q_base, feedback_strength, community_memory
    )
    q = target_high_state_occupancy(
        phenotype_frequency,
        q_base=q0,
        feedback_strength=eta,
    )
    low_to_high = (1.0 - phi) * q
    high_to_low = (1.0 - phi) * (1.0 - q)
    return (
        (1.0 - low_to_high, low_to_high),
        (high_to_low, 1.0 - high_to_low),
    )


def structural_feedback_rewards(
    low_task: FiniteTask,
    high_task: FiniteTask,
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
) -> tuple[float, float]:
    low = structural_selection_state(
        low_task,
        lambda_cost=lambda_cost,
        control_cost=control_cost,
    ).log_fitness_ratio
    high = structural_selection_state(
        high_task,
        lambda_cost=lambda_cost,
        control_cost=control_cost,
    ).log_fitness_ratio
    return low, high


def mean_selection_at_occupancy(
    high_state_occupancy: float,
    low_reward: float,
    high_reward: float,
) -> float:
    q = float(high_state_occupancy)
    if not 0.0 <= q <= 1.0:
        raise ValueError("high_state_occupancy must lie in [0,1]")
    low = float(low_reward)
    high = float(high_reward)
    if not isfinite(low) or not isfinite(high):
        raise ValueError("rewards must be finite")
    return low + (high - low) * q


def feedback_step(
    phenotype_frequency: float,
    high_state_occupancy: float,
    *,
    low_reward: float,
    high_reward: float,
    q_base: float,
    feedback_strength: float,
    community_memory: float,
) -> tuple[float, float, float]:
    """One simultaneous mean-field eco-evolutionary update.

    Returns ``(p_next, q_next, current_mean_selection)``.
    """

    p = float(phenotype_frequency)
    q = float(high_state_occupancy)
    if not 0.0 <= p <= 1.0:
        raise ValueError("phenotype_frequency must lie in [0,1]")
    if not 0.0 <= q <= 1.0:
        raise ValueError("high_state_occupancy must lie in [0,1]")
    q0, eta, phi = _validate_feedback_geometry(
        q_base, feedback_strength, community_memory
    )
    selection = mean_selection_at_occupancy(q, low_reward, high_reward)
    p_next = update_frequency_by_log_fitness_ratio(p, selection)
    q_target = target_high_state_occupancy(
        p,
        q_base=q0,
        feedback_strength=eta,
    )
    q_next = phi * q + (1.0 - phi) * q_target
    return p_next, q_next, selection


@dataclass(frozen=True)
class FeedbackEquilibrium:
    status: str
    phenotype_frequency: float | None
    high_state_occupancy: float | None
    low_reward: float
    high_reward: float
    reward_contrast: float
    q_base: float
    feedback_strength: float
    community_memory: float
    jacobian_trace: float | None
    jacobian_determinant: float | None
    eigenvalues: tuple[complex, complex] | None
    jury_conditions: tuple[float, float, float] | None
    locally_stable: bool


def interior_feedback_equilibrium(
    *,
    low_reward: float,
    high_reward: float,
    q_base: float,
    feedback_strength: float,
    community_memory: float,
) -> FeedbackEquilibrium:
    """Return the unique candidate interior equilibrium and local stability audit."""

    low = float(low_reward)
    high = float(high_reward)
    if not isfinite(low) or not isfinite(high):
        raise ValueError("rewards must be finite")
    q0, eta, phi = _validate_feedback_geometry(
        q_base, feedback_strength, community_memory
    )
    delta = high - low
    if abs(delta) <= _TOL:
        return FeedbackEquilibrium(
            "no_reward_contrast",
            None, None, low, high, delta, q0, eta, phi,
            None, None, None, None, False,
        )
    q_star = -low / delta
    if not 0.0 < q_star < 1.0:
        return FeedbackEquilibrium(
            "selection_zero_outside_interior_community_range",
            None, q_star, low, high, delta, q0, eta, phi,
            None, None, None, None, False,
        )
    if abs(eta) <= _TOL:
        return FeedbackEquilibrium(
            "no_frequency_feedback",
            None, q_star, low, high, delta, q0, eta, phi,
            None, None, None, None, False,
        )
    p_star = 0.5 + (q_star - q0) / eta
    if not 0.0 < p_star < 1.0:
        return FeedbackEquilibrium(
            "equilibrium_frequency_outside_unit_interval",
            p_star, q_star, low, high, delta, q0, eta, phi,
            None, None, None, None, False,
        )

    response = p_star * (1.0 - p_star)
    trace = 1.0 + phi
    determinant = phi - delta * (1.0 - phi) * eta * response
    discriminant = trace * trace - 4.0 * determinant
    root = complex_sqrt(discriminant)
    eigenvalues = ((trace + root) / 2.0, (trace - root) / 2.0)

    jury1 = 1.0 - trace + determinant
    jury2 = 1.0 + trace + determinant
    jury3 = 1.0 - determinant
    stable = jury1 > _TOL and jury2 > _TOL and jury3 > _TOL

    return FeedbackEquilibrium(
        "interior_equilibrium",
        p_star,
        q_star,
        low,
        high,
        delta,
        q0,
        eta,
        phi,
        trace,
        determinant,
        eigenvalues,
        (jury1, jury2, jury3),
        stable,
    )


def structural_feedback_equilibrium(
    low_task: FiniteTask,
    high_task: FiniteTask,
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
    q_base: float = 0.5,
    feedback_strength: float = 0.0,
    community_memory: float = 0.0,
) -> FeedbackEquilibrium:
    low, high = structural_feedback_rewards(
        low_task,
        high_task,
        lambda_cost=lambda_cost,
        control_cost=control_cost,
    )
    return interior_feedback_equilibrium(
        low_reward=low,
        high_reward=high,
        q_base=q_base,
        feedback_strength=feedback_strength,
        community_memory=community_memory,
    )


def simulate_structural_feedback(
    low_task: FiniteTask,
    high_task: FiniteTask,
    *,
    initial_frequency: float,
    initial_high_occupancy: float,
    generations: int,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
    q_base: float = 0.5,
    feedback_strength: float = 0.0,
    community_memory: float = 0.0,
) -> tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...]]:
    """Return phenotype-frequency, community-occupancy, and selection paths.

    Frequency and occupancy paths include the initial state; selection contains
    one value per generation.
    """

    H = int(generations)
    if H < 0:
        raise ValueError("generations must be non-negative")
    low, high = structural_feedback_rewards(
        low_task,
        high_task,
        lambda_cost=lambda_cost,
        control_cost=control_cost,
    )
    p = float(initial_frequency)
    q = float(initial_high_occupancy)
    if not 0.0 <= p <= 1.0 or not 0.0 <= q <= 1.0:
        raise ValueError("initial frequency and occupancy must lie in [0,1]")
    _validate_feedback_geometry(q_base, feedback_strength, community_memory)

    p_path = [p]
    q_path = [q]
    s_path = []
    for _ in range(H):
        p, q, selection = feedback_step(
            p,
            q,
            low_reward=low,
            high_reward=high,
            q_base=q_base,
            feedback_strength=feedback_strength,
            community_memory=community_memory,
        )
        p_path.append(p)
        q_path.append(q)
        s_path.append(selection)
    return tuple(p_path), tuple(q_path), tuple(s_path)
