"""Dimensionless loop gain for the endogenous community-feedback layer.

For an interior equilibrium of ``endogenous_community_feedback.py`` with
reward contrast ``Delta_s = s_high-s_low``, feedback slope ``eta``, and
phenotype response ``r=p_star(1-p_star)``, define

    L = -eta * Delta_s * r.

When Delta_s>0 and 0<=phi<1, the exact Jury conditions reduce to

    0 < L < 1.

The Jacobian discriminant is

    (1-phi) * [(1-phi) - 4L],

so a stable equilibrium is

    0 < L <= (1-phi)/4       stable nonoscillatory,
    (1-phi)/4 < L < 1       stable damped oscillatory,
    L >= 1                   strong-feedback oscillatory instability,
    L <= 0                   non-restoring / positive-feedback instability.

At L=1 and phi<1 the conjugate pair lies on the unit circle. Its critical
angle satisfies cos(theta_c)=(1+phi)/2, giving a critical local oscillation
period 2*pi/theta_c.

Inside the damped phase the conjugate modulus obeys

    rho^2 = phi + (1-phi)L
          = 1 - (1-phi)(1-L).

Therefore the exact local e-folding time is

    tau = -2 / log[1-(1-phi)(1-L)],

and near either the strong-feedback boundary L -> 1- or the long-memory
boundary phi -> 1-,

    tau ~ 2 / [(1-phi)(1-L)].

This is the branch's critical-slowing timescale.  The bifurcation and asymptotic
algebra are standard; the repository-specific input is that L contains the exact
adaptive/fixed structural gap contrast.
"""

from __future__ import annotations

from cmath import phase
from dataclasses import dataclass
from math import acos, inf, isfinite, log, pi, sqrt

from .core import FiniteTask, adaptive_gain_receipt
from .endogenous_community_feedback import FeedbackEquilibrium

_TOL = 1e-12


def task_structural_gap(task: FiniteTask) -> int:
    receipt = adaptive_gain_receipt(task)
    if receipt.adaptive_cost is None or receipt.fixed_cost is None:
        raise ValueError("task must be resolvable")
    return receipt.fixed_cost - receipt.adaptive_cost


def structural_gap_contrast(low_task: FiniteTask, high_task: FiniteTask) -> int:
    """Return Delta_g=(C_F-C_A)_high-(C_F-C_A)_low."""

    return task_structural_gap(high_task) - task_structural_gap(low_task)


def loop_gain_from_equilibrium(equilibrium: FeedbackEquilibrium) -> float:
    """Return L=-eta*Delta_s*p*(1-p) for an interior equilibrium."""

    if equilibrium.status != "interior_equilibrium":
        raise ValueError("loop gain requires an interior equilibrium")
    p = equilibrium.phenotype_frequency
    if p is None:
        raise ValueError("interior equilibrium lost phenotype frequency")
    return (
        -equilibrium.feedback_strength
        * equilibrium.reward_contrast
        * p
        * (1.0 - p)
    )


def structural_loop_gain(
    low_task: FiniteTask,
    high_task: FiniteTask,
    *,
    lambda_cost: float,
    feedback_strength: float,
    equilibrium_frequency: float,
) -> float:
    """Loop gain directly from exact structural gap contrast.

    The state-independent maintenance cost cancels from the reward contrast.
    """

    lam = float(lambda_cost)
    eta = float(feedback_strength)
    p = float(equilibrium_frequency)
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    if not isfinite(eta):
        raise ValueError("feedback_strength must be finite")
    if not 0.0 < p < 1.0:
        raise ValueError("equilibrium_frequency must lie strictly inside (0,1)")
    delta_g = structural_gap_contrast(low_task, high_task)
    return -eta * lam * delta_g * p * (1.0 - p)


def centered_loop_gain_from_gap_contrast(
    gap_contrast: float,
    *,
    lambda_cost: float,
    feedback_strength: float,
) -> float:
    """Loop gain at the centered equilibrium p*=1/2."""

    delta_g = float(gap_contrast)
    lam = float(lambda_cost)
    eta = float(feedback_strength)
    if not isfinite(delta_g):
        raise ValueError("gap_contrast must be finite")
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    if not isfinite(eta):
        raise ValueError("feedback_strength must be finite")
    return -eta * lam * delta_g / 4.0


def oscillation_threshold(community_memory: float) -> float:
    """Loop-gain threshold (1-phi)/4 for complex local eigenvalues."""

    phi = float(community_memory)
    if not isfinite(phi) or not 0.0 <= phi < 1.0:
        raise ValueError("community_memory must lie in [0,1)")
    return (1.0 - phi) / 4.0


def unit_circle_instability_period(community_memory: float) -> float:
    """Critical local oscillation period at the strong-feedback boundary L=1."""

    phi = float(community_memory)
    if not isfinite(phi) or not 0.0 <= phi < 1.0:
        raise ValueError("community_memory must lie in [0,1)")
    theta = acos((1.0 + phi) / 2.0)
    return 2.0 * pi / theta


def unit_circle_period_long_memory_asymptotic(community_memory: float) -> float:
    """Long-memory approximation 2*pi/sqrt(1-phi) to the L=1 period."""

    phi = float(community_memory)
    if not isfinite(phi) or not 0.0 <= phi < 1.0:
        raise ValueError("community_memory must lie in [0,1)")
    return 2.0 * pi / sqrt(1.0 - phi)


def transient_regime(equilibrium: FeedbackEquilibrium) -> str:
    """Classify the local feedback regime using exact loop-gain boundaries."""

    if equilibrium.status != "interior_equilibrium":
        return "no_interior_equilibrium"
    if equilibrium.reward_contrast <= _TOL:
        return "unsupported_nonpositive_reward_contrast"
    L = loop_gain_from_equilibrium(equilibrium)
    if L <= _TOL:
        return "unstable_nonrestoring_feedback"
    if L >= 1.0 - _TOL:
        return "unstable_negative_feedback_overshoot"
    threshold = oscillation_threshold(equilibrium.community_memory)
    if L > threshold + _TOL:
        return "stable_damped_oscillation"
    return "stable_nonoscillatory"


def damped_phase_spectral_radius(loop_gain: float, community_memory: float) -> float:
    """Exact conjugate-pair modulus in the stable damped phase."""

    L = float(loop_gain)
    phi = float(community_memory)
    if not isfinite(L):
        raise ValueError("loop_gain must be finite")
    threshold = oscillation_threshold(phi)
    if not threshold < L < 1.0:
        raise ValueError("requires stable damped phase: (1-phi)/4 < L < 1")
    return sqrt(phi + (1.0 - phi) * L)


def damping_time_from_loop_gain(loop_gain: float, community_memory: float) -> float:
    """Exact local e-folding time in the stable damped phase.

    Since rho^2 = 1-epsilon with epsilon=(1-phi)(1-L),

        tau = -1/log(rho) = -2/log(1-epsilon).
    """

    rho = damped_phase_spectral_radius(loop_gain, community_memory)
    return -1.0 / log(rho)


def critical_slowing_approximation(loop_gain: float, community_memory: float) -> float:
    """Leading approximation 2/[(1-phi)(1-L)] near the stable boundary."""

    L = float(loop_gain)
    phi = float(community_memory)
    # Reuse phase validation rather than silently extending the formula outside
    # the damped stable region.
    damped_phase_spectral_radius(L, phi)
    epsilon = (1.0 - phi) * (1.0 - L)
    return 2.0 / epsilon


def critical_slowing_scaled_ratio(loop_gain: float, community_memory: float) -> float:
    """tau*(1-phi)*(1-L)/2, which tends to one at critical slowing."""

    L = float(loop_gain)
    phi = float(community_memory)
    tau = damping_time_from_loop_gain(L, phi)
    return tau * (1.0 - phi) * (1.0 - L) / 2.0


def local_spectral_radius(equilibrium: FeedbackEquilibrium) -> float:
    """Maximum local eigenvalue modulus for an interior equilibrium."""

    if equilibrium.status != "interior_equilibrium" or equilibrium.eigenvalues is None:
        raise ValueError("spectral radius requires an interior equilibrium")
    return max(abs(value) for value in equilibrium.eigenvalues)


def local_damping_time(equilibrium: FeedbackEquilibrium) -> float:
    """Local e-folding generations -1/log(rho) for a stable equilibrium."""

    rho = local_spectral_radius(equilibrium)
    if rho >= 1.0 - _TOL:
        return inf
    if rho <= _TOL:
        return 0.0
    return -1.0 / log(rho)


def local_oscillation_period(equilibrium: FeedbackEquilibrium) -> float | None:
    """Local oscillation period in generations for a complex stable pair."""

    if transient_regime(equilibrium) != "stable_damped_oscillation":
        return None
    assert equilibrium.eigenvalues is not None
    angle = abs(phase(equilibrium.eigenvalues[0]))
    if angle <= _TOL:
        return None
    return 2.0 * pi / angle


def k_branch_centered_loop_gain(
    branch_count: int,
    *,
    lambda_cost: float,
    feedback_strength: float,
) -> float:
    """Centered L for a gap-0 control vs k-branch family (gap k-1)."""

    k = int(branch_count)
    if k < 2:
        raise ValueError("branch_count must be at least 2")
    return centered_loop_gain_from_gap_contrast(
        k - 1,
        lambda_cost=lambda_cost,
        feedback_strength=feedback_strength,
    )


def binary_family_centered_loop_gain(
    routing_depth: int,
    *,
    lambda_cost: float,
    feedback_strength: float,
) -> float:
    """Centered L for a gap-0 control vs binary extremal routing family.

    Existing family theorem: C_A=d+1, C_F=2^d, so Delta_g=2^d-(d+1).
    """

    d = int(routing_depth)
    if d < 1:
        raise ValueError("routing_depth must be positive")
    delta_g = (1 << d) - (d + 1)
    return centered_loop_gain_from_gap_contrast(
        delta_g,
        lambda_cost=lambda_cost,
        feedback_strength=feedback_strength,
    )


@dataclass(frozen=True)
class LoopGainSummary:
    loop_gain: float
    oscillation_threshold: float
    regime: str
    spectral_radius: float
    damping_time: float
    oscillation_period: float | None


def summarize_loop_gain(equilibrium: FeedbackEquilibrium) -> LoopGainSummary:
    if equilibrium.status != "interior_equilibrium":
        raise ValueError("summary requires an interior equilibrium")
    L = loop_gain_from_equilibrium(equilibrium)
    return LoopGainSummary(
        loop_gain=L,
        oscillation_threshold=oscillation_threshold(equilibrium.community_memory),
        regime=transient_regime(equilibrium),
        spectral_radius=local_spectral_radius(equilibrium),
        damping_time=local_damping_time(equilibrium),
        oscillation_period=local_oscillation_period(equilibrium),
    )
