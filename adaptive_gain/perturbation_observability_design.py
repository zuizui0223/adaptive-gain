"""Local perturbation/observation design for two-mode eco-evolutionary transients.

For a linearized two-dimensional system

    y[t+1] = J y[t]

with scalar observation

    x[t] = c^T y[t]

and initial perturbation ``v=y[0]``, the four-point Hankel visibility determinant

    R = x0*x2 - x1^2

factorizes exactly as

    R = det([c^T; c^T J]) * det([v, Jv]).

The first factor is an observation-side area; the second is a perturbation-side
excitation area.  Thus scalar non-observability can arise because the measured
coordinate hides one local mode, because the perturbation excites only one mode,
or both.

The algebra is standard 2x2 observability/controllability geometry.  The
repository-specific use is experimental: it tells the eco-evolutionary inverse
layer what kind of natural-history perturbation and measured response are needed
before attempting to assign biological timescales or structural sensing gain.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence

_TOL = 1e-12


def _vec2(values: Sequence[float], *, name: str) -> tuple[float, float]:
    if len(values) != 2:
        raise ValueError(f"{name} must have length 2")
    x, y = float(values[0]), float(values[1])
    if not isfinite(x) or not isfinite(y):
        raise ValueError(f"{name} entries must be finite")
    return x, y


def _mat2(values: Sequence[Sequence[float]]) -> tuple[tuple[float, float], tuple[float, float]]:
    if len(values) != 2 or any(len(row) != 2 for row in values):
        raise ValueError("matrix must be 2x2")
    a = tuple(tuple(float(x) for x in row) for row in values)
    if any(not isfinite(x) for row in a for x in row):
        raise ValueError("matrix entries must be finite")
    return a  # type: ignore[return-value]


def _mv(J: tuple[tuple[float, float], tuple[float, float]], v: tuple[float, float]) -> tuple[float, float]:
    return (
        J[0][0] * v[0] + J[0][1] * v[1],
        J[1][0] * v[0] + J[1][1] * v[1],
    )


def _row_times_matrix(c: tuple[float, float], J: tuple[tuple[float, float], tuple[float, float]]) -> tuple[float, float]:
    return (
        c[0] * J[0][0] + c[1] * J[1][0],
        c[0] * J[0][1] + c[1] * J[1][1],
    )


def _dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _det_rows(r1: tuple[float, float], r2: tuple[float, float]) -> float:
    return r1[0] * r2[1] - r1[1] * r2[0]


def _norm_sq(v: tuple[float, float]) -> float:
    return v[0] * v[0] + v[1] * v[1]


def scalar_trajectory_first_three(
    matrix: Sequence[Sequence[float]],
    observation: Sequence[float],
    perturbation: Sequence[float],
) -> tuple[float, float, float]:
    """Return ``(x0,x1,x2)`` for ``x_t=c^T J^t v``."""

    J = _mat2(matrix)
    c = _vec2(observation, name="observation")
    v = _vec2(perturbation, name="perturbation")
    Jv = _mv(J, v)
    JJv = _mv(J, Jv)
    return _dot(c, v), _dot(c, Jv), _dot(c, JJv)


def hankel_visibility(
    matrix: Sequence[Sequence[float]],
    observation: Sequence[float],
    perturbation: Sequence[float],
) -> float:
    """Return ``R=x0*x2-x1^2`` for the observed scalar transient."""

    x0, x1, x2 = scalar_trajectory_first_three(matrix, observation, perturbation)
    return x0 * x2 - x1 * x1


def observation_visibility_factor(
    matrix: Sequence[Sequence[float]],
    observation: Sequence[float],
) -> float:
    """Return ``det([c^T; c^T J])``."""

    J = _mat2(matrix)
    c = _vec2(observation, name="observation")
    return _det_rows(c, _row_times_matrix(c, J))


def perturbation_visibility_factor(
    matrix: Sequence[Sequence[float]],
    perturbation: Sequence[float],
) -> float:
    """Return ``det([v,Jv])``."""

    J = _mat2(matrix)
    v = _vec2(perturbation, name="perturbation")
    return _det_rows(v, _mv(J, v))


def factorized_visibility(
    matrix: Sequence[Sequence[float]],
    observation: Sequence[float],
    perturbation: Sequence[float],
) -> float:
    """Return the exact factorized Hankel visibility determinant."""

    return observation_visibility_factor(matrix, observation) * perturbation_visibility_factor(matrix, perturbation)


def normalized_observation_visibility(
    matrix: Sequence[Sequence[float]],
    observation: Sequence[float],
) -> float:
    """Scale-free observation-side visibility ``|O|/||c||^2``."""

    c = _vec2(observation, name="observation")
    scale = _norm_sq(c)
    if scale <= _TOL:
        raise ValueError("observation vector must be non-zero")
    return abs(observation_visibility_factor(matrix, c)) / scale


def normalized_perturbation_visibility(
    matrix: Sequence[Sequence[float]],
    perturbation: Sequence[float],
) -> float:
    """Scale-free perturbation-side visibility ``|C|/||v||^2``."""

    v = _vec2(perturbation, name="perturbation")
    scale = _norm_sq(v)
    if scale <= _TOL:
        raise ValueError("perturbation vector must be non-zero")
    return abs(perturbation_visibility_factor(matrix, v)) / scale


def normalized_hankel_visibility(
    matrix: Sequence[Sequence[float]],
    observation: Sequence[float],
    perturbation: Sequence[float],
) -> float:
    """Scale-free ``|R|/(||c||^2 ||v||^2)``."""

    c = _vec2(observation, name="observation")
    v = _vec2(perturbation, name="perturbation")
    cs = _norm_sq(c)
    vs = _norm_sq(v)
    if cs <= _TOL or vs <= _TOL:
        raise ValueError("observation and perturbation vectors must be non-zero")
    return abs(hankel_visibility(matrix, c, v)) / (cs * vs)


def symmetric_single_side_visibility(
    eigenvalue_1: float,
    eigenvalue_2: float,
    first_mode_weight: float,
    second_mode_weight: float,
) -> float:
    """Normalized one-side visibility in an orthonormal eigenbasis.

    For a symmetric local matrix with eigenvalues ``r1,r2`` and a vector whose
    coordinates in the orthonormal eigenbasis are ``(u1,u2)``, the normalized
    area is

        |r1-r2| * |u1*u2| / (u1^2+u2^2).
    """

    r1 = float(eigenvalue_1)
    r2 = float(eigenvalue_2)
    u1 = float(first_mode_weight)
    u2 = float(second_mode_weight)
    if not all(isfinite(x) for x in (r1, r2, u1, u2)):
        raise ValueError("inputs must be finite")
    scale = u1 * u1 + u2 * u2
    if scale <= _TOL:
        raise ValueError("mode weights must not both be zero")
    return abs(r1 - r2) * abs(u1 * u2) / scale


def symmetric_max_single_side_visibility(eigenvalue_1: float, eigenvalue_2: float) -> float:
    """Maximum normalized observation/excitation factor for a symmetric 2x2 system."""

    r1 = float(eigenvalue_1)
    r2 = float(eigenvalue_2)
    if not isfinite(r1) or not isfinite(r2):
        raise ValueError("eigenvalues must be finite")
    return abs(r1 - r2) / 2.0


def symmetric_max_hankel_visibility(eigenvalue_1: float, eigenvalue_2: float) -> float:
    """Maximum normalized ``|R|`` when both perturbation and observation are designable.

    The maximum is attained when both vectors have equal absolute weights on the
    two orthogonal eigenmodes.
    """

    side = symmetric_max_single_side_visibility(eigenvalue_1, eigenvalue_2)
    return side * side


@dataclass(frozen=True)
class VisibilityDesignSummary:
    hankel_visibility: float
    observation_factor: float
    perturbation_factor: float
    normalized_hankel_visibility: float
    normalized_observation_visibility: float
    normalized_perturbation_visibility: float
    scalar_modes_visible: bool
    observation_side_visible: bool
    perturbation_side_visible: bool


def summarize_visibility_design(
    matrix: Sequence[Sequence[float]],
    observation: Sequence[float],
    perturbation: Sequence[float],
    *,
    tolerance: float = 1e-10,
) -> VisibilityDesignSummary:
    """Collect the forward scalar-visibility factors for experiment auditing."""

    tol = float(tolerance)
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("tolerance must be finite and non-negative")
    R = hankel_visibility(matrix, observation, perturbation)
    O = observation_visibility_factor(matrix, observation)
    C = perturbation_visibility_factor(matrix, perturbation)
    return VisibilityDesignSummary(
        hankel_visibility=R,
        observation_factor=O,
        perturbation_factor=C,
        normalized_hankel_visibility=normalized_hankel_visibility(matrix, observation, perturbation),
        normalized_observation_visibility=normalized_observation_visibility(matrix, observation),
        normalized_perturbation_visibility=normalized_perturbation_visibility(matrix, perturbation),
        scalar_modes_visible=abs(R) > tol,
        observation_side_visible=abs(O) > tol,
        perturbation_side_visible=abs(C) > tol,
    )


@dataclass(frozen=True)
class CandidateDesignChoice:
    observation_index: int
    perturbation_index: int
    observation_score: float
    perturbation_score: float
    joint_score: float


def best_observation_candidate(
    matrix: Sequence[Sequence[float]],
    observations: Sequence[Sequence[float]],
) -> tuple[int, float]:
    """Return the index and normalized visibility of the best allowed observation."""

    if not observations:
        raise ValueError("observations must be non-empty")
    scores = [normalized_observation_visibility(matrix, c) for c in observations]
    index = max(range(len(scores)), key=lambda i: (scores[i], -i))
    return index, scores[index]


def best_perturbation_candidate(
    matrix: Sequence[Sequence[float]],
    perturbations: Sequence[Sequence[float]],
) -> tuple[int, float]:
    """Return the index and normalized visibility of the best allowed perturbation."""

    if not perturbations:
        raise ValueError("perturbations must be non-empty")
    scores = [normalized_perturbation_visibility(matrix, v) for v in perturbations]
    index = max(range(len(scores)), key=lambda i: (scores[i], -i))
    return index, scores[index]


def best_independent_candidate_design(
    matrix: Sequence[Sequence[float]],
    observations: Sequence[Sequence[float]],
    perturbations: Sequence[Sequence[float]],
) -> CandidateDesignChoice:
    """Optimize an independently feasible observation/perturbation Cartesian product.

    Because normalized visibility factorizes, the optimal pair is exactly the
    independently best observation and independently best perturbation.  This
    function deliberately assumes every listed observation can be paired with
    every listed perturbation.
    """

    oi, os = best_observation_candidate(matrix, observations)
    pi, ps = best_perturbation_candidate(matrix, perturbations)
    return CandidateDesignChoice(
        observation_index=oi,
        perturbation_index=pi,
        observation_score=os,
        perturbation_score=ps,
        joint_score=os * ps,
    )


def brute_force_candidate_design(
    matrix: Sequence[Sequence[float]],
    observations: Sequence[Sequence[float]],
    perturbations: Sequence[Sequence[float]],
) -> CandidateDesignChoice:
    """Enumerate all allowed Cartesian-product pairs for an audit cross-check."""

    if not observations or not perturbations:
        raise ValueError("observations and perturbations must be non-empty")
    best: CandidateDesignChoice | None = None
    for oi, c in enumerate(observations):
        os = normalized_observation_visibility(matrix, c)
        for pi, v in enumerate(perturbations):
            ps = normalized_perturbation_visibility(matrix, v)
            score = normalized_hankel_visibility(matrix, c, v)
            choice = CandidateDesignChoice(oi, pi, os, ps, score)
            if best is None or (score, -oi, -pi) > (best.joint_score, -best.observation_index, -best.perturbation_index):
                best = choice
    assert best is not None
    return best
