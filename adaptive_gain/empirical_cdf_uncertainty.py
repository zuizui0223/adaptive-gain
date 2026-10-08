"""Exploratory uncertainty checks for interval-censored first-probe CDFs.

These calculations regard individuals as independent binomial observations.
They do not account for experimental batches or the cohort restriction to
animals with zero pre-stimulus probing. Results are descriptive, not evidence
for an evolved adaptive-versus-fixed architecture.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class CDFComparison:
    first_k: int
    first_n: int
    second_k: int
    second_n: int
    first_fraction: float
    second_fraction: float
    difference: float
    first_wilson95: tuple[float, float]
    second_wilson95: tuple[float, float]
    fisher_two_sided_p: float


def wilson_interval(k: int, n: int, *, z: float = 1.959963984540054) -> tuple[float, float]:
    """Two-sided Wilson binomial confidence interval."""
    if type(n) is not int or n <= 0 or type(k) is not int or not (0 <= k <= n):
        raise ValueError("require integers 0 <= k <= n and n > 0")
    if not math.isfinite(z) or z <= 0:
        raise ValueError("z must be finite and positive")
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return center - half, center + half


def fisher_exact_two_sided(k1: int, n1: int, k2: int, n2: int) -> float:
    """Classical probability-ordering two-sided Fisher exact test."""
    for k, n in ((k1, n1), (k2, n2)):
        if type(k) is not int or type(n) is not int or n <= 0 or not (0 <= k <= n):
            raise ValueError("require integers 0 <= k <= n and n > 0")
    K = k1 + k2
    N = n1 + n2
    denom = math.comb(N, K)
    def pmf(k):
        return math.comb(n1, k) * math.comb(n2, K - k) / denom
    observed = pmf(k1)
    lower = max(0, K - n2)
    upper = min(n1, K)
    return min(1.0, sum(
        pmf(k) for k in range(lower, upper + 1)
        if pmf(k) <= observed + 1e-12
    ))


def compare_cdfs(k1: int, n1: int, k2: int, n2: int) -> CDFComparison:
    return CDFComparison(
        first_k=k1,
        first_n=n1,
        second_k=k2,
        second_n=n2,
        first_fraction=k1 / n1,
        second_fraction=k2 / n2,
        difference=k1 / n1 - k2 / n2,
        first_wilson95=wilson_interval(k1, n1),
        second_wilson95=wilson_interval(k2, n2),
        fisher_two_sided_p=fisher_exact_two_sided(k1, n1, k2, n2),
    )
