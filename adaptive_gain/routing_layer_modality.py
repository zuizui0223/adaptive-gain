"""Exact aggregate-layer modality for finite weakest-branch routing spaces.

This module isolates the routing-specific combinatorics from the established
origin-fixation machinery.  For x in {0,...,q}^k with gain g(x)=min_i x_i,
the gain-r layer has multiplicity

    D_r = (q-r+1)^k - (q-r)^k.

Under a symmetric per-gain stationary tilt theta, aggregate layer mass is
proportional to D_r * theta^r.  The full-gain layer is modal exactly when

theta >= 2^k - 1.

For k>=2, equality produces a two-layer tie between gains q and q-1 only;
strict inequality above the threshold makes the full-gain layer uniquely modal.
"""
from __future__ import annotations

from fractions import Fraction

from ._exact_rational import as_exact_fraction


def _positive_int(value: int, *, name: str) -> int:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def weakest_branch_layer_degeneracy(
    max_gain: int,
    branch_count: int,
    gain_layer: int,
) -> int:
    """Exact number of vectors in {0,...,q}^k with minimum coordinate r."""

    q = _positive_int(max_gain, name="max_gain")
    k = _positive_int(branch_count, name="branch_count")
    r = gain_layer
    if type(r) is not int or not (0 <= r <= q):
        raise ValueError("gain_layer must be an integer in [0,max_gain]")
    return (q - r + 1) ** k - (q - r) ** k


def distance_layer_degeneracy(branch_count: int, steps_below_full: int) -> int:
    """A_s=(s+1)^k-s^k for the layer s steps below full gain."""

    k = _positive_int(branch_count, name="branch_count")
    s = steps_below_full
    if type(s) is not int or s < 0:
        raise ValueError("steps_below_full must be a nonnegative integer")
    return (s + 1) ** k - s**k


def aggregate_modal_tilt_threshold(branch_count: int) -> int:
    """Sharp theta threshold for the full-gain layer to be aggregate-modal."""

    k = _positive_int(branch_count, name="branch_count")
    return 2**k - 1


def degeneracy_chain_bound_is_strict(branch_count: int, steps_below_full: int) -> bool:
    """Check A_s < (2^k-1)^s for k>=2 and s>=2.

    The non-strict bound follows by encoding a distance-s routing state as a
    nested sequence of s nonempty subsets of k branch labels and then dropping
    the nesting constraint.  For k>=2 and s>=2 that relaxation is strict: for
    example ({1},{2},...) is an admissible arbitrary subset sequence but is not
    nested.
    """

    k = _positive_int(branch_count, name="branch_count")
    s = steps_below_full
    if k < 2:
        raise ValueError("strict bound requires branch_count >= 2")
    if type(s) is not int or s < 2:
        raise ValueError("strict bound requires steps_below_full >= 2")
    threshold = aggregate_modal_tilt_threshold(k)
    return distance_layer_degeneracy(k, s) < threshold**s


def aggregate_layer_weights(
    max_gain: int,
    branch_count: int,
    theta: Fraction | int,
) -> tuple[Fraction, ...]:
    """Unnormalized aggregate stationary weights indexed by gain layer."""

    q = _positive_int(max_gain, name="max_gain")
    k = _positive_int(branch_count, name="branch_count")
    tilt = as_exact_fraction(theta, name="theta")
    if tilt <= 0:
        raise ValueError("theta must be positive")
    return tuple(
        Fraction(weakest_branch_layer_degeneracy(q, k, r)) * tilt**r
        for r in range(q + 1)
    )


def modal_gain_layers(
    max_gain: int,
    branch_count: int,
    theta: Fraction | int,
) -> tuple[int, ...]:
    """Gain layers attaining maximal aggregate stationary mass."""

    weights = aggregate_layer_weights(max_gain, branch_count, theta)
    maximum = max(weights)
    return tuple(r for r, weight in enumerate(weights) if weight == maximum)


def threshold_modal_gain_layers(max_gain: int, branch_count: int) -> tuple[int, ...]:
    """Exact modal layers at theta=2^k-1.

    For k>=2 and q>=1 only q-1 and q tie.  For k=1, theta=1 and every layer
    has multiplicity one, so every gain layer ties.
    """

    q = _positive_int(max_gain, name="max_gain")
    k = _positive_int(branch_count, name="branch_count")
    return modal_gain_layers(q, k, aggregate_modal_tilt_threshold(k))


def minimum_population_size_for_modal_full_layer(
    branch_count: int,
    fitness_step: Fraction | int,
) -> int | None:
    """Smallest N>=2 with a^(N-1) >= 2^k-1; None if never reached."""

    k = _positive_int(branch_count, name="branch_count")
    a = as_exact_fraction(fitness_step, name="fitness_step")
    if a < 1:
        raise ValueError("fitness_step must be at least one")
    threshold = aggregate_modal_tilt_threshold(k)
    if a == 1:
        return 2 if threshold == 1 else None
    n = 2
    while a ** (n - 1) < threshold:
        n += 1
    return n


def minimum_population_size_for_unique_modal_full_layer(
    branch_count: int,
    fitness_step: Fraction | int,
) -> int | None:
    """Smallest N>=2 with a^(N-1) > 2^k-1; None if never reached."""

    k = _positive_int(branch_count, name="branch_count")
    a = as_exact_fraction(fitness_step, name="fitness_step")
    if a < 1:
        raise ValueError("fitness_step must be at least one")
    if a == 1:
        return None
    threshold = aggregate_modal_tilt_threshold(k)
    n = 2
    while a ** (n - 1) <= threshold:
        n += 1
    return n
