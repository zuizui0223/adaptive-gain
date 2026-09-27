"""Conservative planning calculations for the direct routeability experiment.

This module deliberately separates nuisance parameters that may come from an
architecture-neutral procedural pilot from the confirmatory routeability effect.
The focal H1/H2 effect size must be supplied as an external probability-scale
SESOI; it must not be estimated from the confirmatory contrast or copied from
the exact 0.25 information ceiling.

The calculator uses a conservative Bernoulli variance bound p(1-p) <= 1/4 and
a repeated-trial design effect. It is a screening calculation for balanced
individuals-per-cell, not a substitute for final GLMM simulation once pilot
nuisance parameters and colony structure are frozen.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from statistics import NormalDist


ALLOWED_SESOI_PROVENANCE = {
    "external_biological_criterion",
    "independent_prior_study",
    "practical_decision_threshold",
}

FORBIDDEN_EFFECT_PROVENANCE = {
    "theoretical_information_ceiling",
    "focal_confirmatory_pilot",
    "posthoc_observed_interaction",
}


def _probability(value: float, name: str, *, open_interval: bool = False) -> float:
    out = float(value)
    if open_interval:
        valid = 0.0 < out < 1.0
    else:
        valid = 0.0 <= out < 1.0
    if not valid:
        bounds = "(0,1)" if open_interval else "[0,1)"
        raise ValueError(f"{name} must be in {bounds}")
    return out


def _round_up_multiple(value: int, multiple: int) -> int:
    if multiple <= 0:
        raise ValueError("multiple must be positive")
    return multiple * ceil(value / multiple)


@dataclass(frozen=True)
class RouteabilityPilotNuisance:
    trial_icc: float
    randomized_individual_dropout: float
    full_information_success: float
    timeout_fraction: float
    source: str
    focal_architecture_access_contrast_opened: bool = False

    def validated(self) -> "RouteabilityPilotNuisance":
        _probability(self.trial_icc, "trial_icc")
        _probability(
            self.randomized_individual_dropout,
            "randomized_individual_dropout",
        )
        _probability(
            self.full_information_success,
            "full_information_success",
            open_interval=True,
        )
        _probability(self.timeout_fraction, "timeout_fraction")
        if not self.source.strip():
            raise ValueError("pilot nuisance source must be non-empty")
        if self.focal_architecture_access_contrast_opened:
            raise ValueError(
                "pilot nuisance input cannot come from an opened focal architecture-access contrast"
            )
        return self


@dataclass(frozen=True)
class RouteabilitySESoi:
    h1_probability_interaction: float
    h2_probability_localization: float
    provenance: str

    def validated(self) -> "RouteabilitySESoi":
        for name, value in (
            ("h1_probability_interaction", self.h1_probability_interaction),
            ("h2_probability_localization", self.h2_probability_localization),
        ):
            out = float(value)
            if not 0.0 < out < 1.0:
                raise ValueError(f"{name} must be in (0,1)")
        if self.provenance in FORBIDDEN_EFFECT_PROVENANCE:
            raise ValueError(
                f"forbidden SESOI provenance: {self.provenance}"
            )
        if self.provenance not in ALLOWED_SESOI_PROVENANCE:
            raise ValueError(
                "SESOI provenance must be an explicitly allowed external source"
            )
        return self


@dataclass(frozen=True)
class RouteabilityPlanningReceipt:
    alpha_two_sided: float
    target_power: float
    trials_per_individual: int
    trial_icc: float
    repeated_trial_design_effect: float
    h1_sesoi: float
    h2_sesoi: float
    h1_complete_individuals_per_cell: int
    h2_complete_individuals_per_cell: int
    required_complete_individuals_per_cell: int
    randomized_individual_dropout: float
    randomized_individuals_per_cell: int
    factorial_cell_count: int
    randomized_total_individuals: int
    counterbalance_multiple: int
    method: str


def conservative_routeability_planning_receipt(
    nuisance: RouteabilityPilotNuisance,
    sesoi: RouteabilitySESoi,
    *,
    trials_per_individual: int,
    alpha_two_sided: float = 0.05,
    target_power: float = 0.80,
    counterbalance_multiple: int = 4,
) -> RouteabilityPlanningReceipt:
    """Return a conservative balanced-cell screening sample-size receipt.

    H1 is a four-cell difference-in-differences at B=2. H2 is the frozen
    localization contrast Delta_B2 - 0.5*(Delta_B1 + Delta_B3). With the
    Bernoulli variance bound 1/4, the corresponding independent-cell variance
    multipliers are 1.0 for H1 and 1.5 for H2 before the repeated-trial design
    effect.
    """

    nuisance.validated()
    sesoi.validated()
    if type(trials_per_individual) is not int or trials_per_individual < 1:
        raise ValueError("trials_per_individual must be a positive integer")
    if not 0.0 < alpha_two_sided < 1.0:
        raise ValueError("alpha_two_sided must be in (0,1)")
    if not 0.0 < target_power < 1.0:
        raise ValueError("target_power must be in (0,1)")
    if type(counterbalance_multiple) is not int or counterbalance_multiple < 1:
        raise ValueError("counterbalance_multiple must be a positive integer")

    design_effect = 1.0 + (trials_per_individual - 1) * nuisance.trial_icc
    normal = NormalDist()
    z_alpha = normal.inv_cdf(1.0 - alpha_two_sided / 2.0)
    z_power = normal.inv_cdf(target_power)
    z2 = (z_alpha + z_power) ** 2

    def complete_n(variance_multiplier: float, delta: float) -> int:
        raw = (
            z2
            * variance_multiplier
            * design_effect
            / (trials_per_individual * delta * delta)
        )
        return max(1, ceil(raw))

    h1_n = complete_n(1.0, sesoi.h1_probability_interaction)
    h2_n = complete_n(1.5, sesoi.h2_probability_localization)
    complete = max(h1_n, h2_n)

    retention = 1.0 - nuisance.randomized_individual_dropout
    randomized_raw = ceil(complete / retention)
    randomized = _round_up_multiple(
        randomized_raw, counterbalance_multiple
    )

    return RouteabilityPlanningReceipt(
        alpha_two_sided=alpha_two_sided,
        target_power=target_power,
        trials_per_individual=trials_per_individual,
        trial_icc=nuisance.trial_icc,
        repeated_trial_design_effect=design_effect,
        h1_sesoi=sesoi.h1_probability_interaction,
        h2_sesoi=sesoi.h2_probability_localization,
        h1_complete_individuals_per_cell=h1_n,
        h2_complete_individuals_per_cell=h2_n,
        required_complete_individuals_per_cell=complete,
        randomized_individual_dropout=nuisance.randomized_individual_dropout,
        randomized_individuals_per_cell=randomized,
        factorial_cell_count=12,
        randomized_total_individuals=12 * randomized,
        counterbalance_multiple=counterbalance_multiple,
        method=(
            "conservative probability-scale screening using Bernoulli variance bound, "
            "repeated-trial design effect, balanced independent treatment cells, "
            "and external SESOI; final GLMM simulation still required"
        ),
    )
