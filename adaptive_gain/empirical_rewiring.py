"""Stage-1 empirical diagnostics for repeated bipartite interaction networks.

These utilities intentionally stop before decision-equivalence inference. They
partition observed link turnover into changes among species shared by adjacent
networks and changes involving species turnover, while exposing the size of the
shared dyad opportunity set.

The shared-species component is an operational feasibility diagnostic for the
post-freeze rewiring program. It is not advertised as a new additive
network-beta-diversity metric.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Hashable, Iterable, Mapping, Sequence

Species = Hashable
Dyad = tuple[Species, Species]


def _clean_network(network: Mapping[Dyad, float]) -> dict[Dyad, float]:
    out: dict[Dyad, float] = {}
    for dyad, weight in network.items():
        if not isinstance(dyad, tuple) or len(dyad) != 2:
            raise ValueError("network keys must be (plant, pollinator) dyads")
        plant, pollinator = dyad
        if plant is None or pollinator is None:
            raise ValueError("species labels cannot be None")
        value = float(weight)
        if not isfinite(value) or value < 0:
            raise ValueError("interaction weights must be finite and non-negative")
        if value > 0:
            out[(plant, pollinator)] = value
    return out


def network_from_rows(
    rows: Iterable[Sequence[object]],
) -> dict[Dyad, float]:
    """Build one weighted network from (plant, pollinator, weight) rows.

    Duplicate dyads are summed. Zero-weight rows are accepted and ignored.
    """

    out: dict[Dyad, float] = {}
    for row in rows:
        if len(row) != 3:
            raise ValueError("each row must contain plant, pollinator, weight")
        plant, pollinator, weight = row
        if plant is None or pollinator is None:
            raise ValueError("species labels cannot be None")
        value = float(weight)
        if not isfinite(value) or value < 0:
            raise ValueError("interaction weights must be finite and non-negative")
        if value == 0:
            continue
        dyad = (plant, pollinator)
        out[dyad] = out.get(dyad, 0.0) + value
    return out


def networks_by_period_from_rows(
    rows: Iterable[Sequence[object]],
) -> dict[Hashable, dict[Dyad, float]]:
    """Build weighted networks from (period, plant, pollinator, weight) rows."""

    out: dict[Hashable, dict[Dyad, float]] = {}
    for row in rows:
        if len(row) != 4:
            raise ValueError("each row must contain period, plant, pollinator, weight")
        period, plant, pollinator, weight = row
        bucket = out.setdefault(period, {})
        value = float(weight)
        if not isfinite(value) or value < 0:
            raise ValueError("interaction weights must be finite and non-negative")
        if plant is None or pollinator is None:
            raise ValueError("species labels cannot be None")
        if value == 0:
            continue
        dyad = (plant, pollinator)
        bucket[dyad] = bucket.get(dyad, 0.0) + value
    return out


@dataclass(frozen=True)
class RewiringTransitionReceipt:
    previous_link_count: int
    current_link_count: int
    union_link_count: int
    shared_plant_count: int
    shared_pollinator_count: int
    shared_species_dyad_count: int
    permitted_shared_dyad_count: int
    stable_shared_link_count: int
    shared_species_gain_count: int
    shared_species_loss_count: int
    species_turnover_gain_count: int
    species_turnover_loss_count: int
    changed_shared_outside_permitted_count: int
    total_link_turnover_count: int

    @property
    def shared_species_rewiring_count(self) -> int:
        return self.shared_species_gain_count + self.shared_species_loss_count

    @property
    def species_turnover_link_count(self) -> int:
        return self.species_turnover_gain_count + self.species_turnover_loss_count

    @property
    def exact_partition(self) -> bool:
        return (
            self.total_link_turnover_count
            == self.shared_species_rewiring_count + self.species_turnover_link_count
        )

    @property
    def link_jaccard_dissimilarity(self) -> float:
        if self.union_link_count == 0:
            return 0.0
        return self.total_link_turnover_count / self.union_link_count

    @property
    def shared_species_rewiring_fraction_of_union(self) -> float:
        if self.union_link_count == 0:
            return 0.0
        return self.shared_species_rewiring_count / self.union_link_count

    @property
    def species_turnover_fraction_of_union(self) -> float:
        if self.union_link_count == 0:
            return 0.0
        return self.species_turnover_link_count / self.union_link_count

    @property
    def rewiring_opportunity_rate(self) -> float | None:
        """Changed shared-species links per permitted shared dyad.

        None means that no shared permitted dyad exists, so a rewiring rate
        is not estimable for that transition.
        """

        if self.permitted_shared_dyad_count == 0:
            return None
        permitted_changed = (
            self.shared_species_rewiring_count
            - self.changed_shared_outside_permitted_count
        )
        return permitted_changed / self.permitted_shared_dyad_count


def transition_rewiring_receipt(
    previous: Mapping[Dyad, float],
    current: Mapping[Dyad, float],
    *,
    permitted_dyads: Iterable[Dyad] | None = None,
) -> RewiringTransitionReceipt:
    """Partition adjacent-network link turnover by species persistence.

    A changed link is counted as shared-species rewiring when both endpoint
    species occur in both adjacent networks. Otherwise the changed link is
    assigned to the species-turnover component.

    permitted_dyads is an optional independently defined compatibility set.
    It affects only the opportunity denominator and QC count; it never erases
    observed links. This prevents a compatibility model from silently
    manufacturing a cleaner rewiring response.
    """

    prev = _clean_network(previous)
    curr = _clean_network(current)
    prev_links = set(prev)
    curr_links = set(curr)

    prev_plants = {p for p, _ in prev_links}
    curr_plants = {p for p, _ in curr_links}
    prev_pollinators = {q for _, q in prev_links}
    curr_pollinators = {q for _, q in curr_links}

    shared_plants = prev_plants & curr_plants
    shared_pollinators = prev_pollinators & curr_pollinators
    shared_dyads = {
        (plant, pollinator)
        for plant in shared_plants
        for pollinator in shared_pollinators
    }

    gains = curr_links - prev_links
    losses = prev_links - curr_links
    shared_gains = gains & shared_dyads
    shared_losses = losses & shared_dyads
    turnover_gains = gains - shared_dyads
    turnover_losses = losses - shared_dyads

    if permitted_dyads is None:
        permitted_shared = shared_dyads
        outside = set()
    else:
        permitted = set(permitted_dyads)
        for dyad in permitted:
            if not isinstance(dyad, tuple) or len(dyad) != 2:
                raise ValueError("permitted_dyads must contain dyad tuples")
        permitted_shared = shared_dyads & permitted
        outside = (shared_gains | shared_losses) - permitted_shared

    receipt = RewiringTransitionReceipt(
        previous_link_count=len(prev_links),
        current_link_count=len(curr_links),
        union_link_count=len(prev_links | curr_links),
        shared_plant_count=len(shared_plants),
        shared_pollinator_count=len(shared_pollinators),
        shared_species_dyad_count=len(shared_dyads),
        permitted_shared_dyad_count=len(permitted_shared),
        stable_shared_link_count=len(prev_links & curr_links & shared_dyads),
        shared_species_gain_count=len(shared_gains),
        shared_species_loss_count=len(shared_losses),
        species_turnover_gain_count=len(turnover_gains),
        species_turnover_loss_count=len(turnover_losses),
        changed_shared_outside_permitted_count=len(outside),
        total_link_turnover_count=len(prev_links ^ curr_links),
    )
    if not receipt.exact_partition:
        raise AssertionError("internal turnover partition failed")
    return receipt


@dataclass(frozen=True)
class PeriodTransition:
    previous_period: Hashable
    current_period: Hashable
    receipt: RewiringTransitionReceipt


def adjacent_transition_series(
    networks: Mapping[Hashable, Mapping[Dyad, float]],
    *,
    period_order: Sequence[Hashable] | None = None,
    permitted_dyads: Iterable[Dyad] | None = None,
) -> tuple[PeriodTransition, ...]:
    """Return receipts for adjacent periods in an explicitly frozen order."""

    if period_order is None:
        try:
            order = tuple(sorted(networks))
        except TypeError as exc:
            raise ValueError(
                "period_order is required when period labels are not mutually sortable"
            ) from exc
    else:
        order = tuple(period_order)

    if len(set(order)) != len(order):
        raise ValueError("period_order contains duplicates")
    missing = [period for period in order if period not in networks]
    if missing:
        raise ValueError(f"period_order contains missing periods: {missing!r}")

    permitted = None if permitted_dyads is None else tuple(permitted_dyads)
    out = []
    for previous_period, current_period in zip(order, order[1:]):
        out.append(
            PeriodTransition(
                previous_period=previous_period,
                current_period=current_period,
                receipt=transition_rewiring_receipt(
                    networks[previous_period],
                    networks[current_period],
                    permitted_dyads=permitted,
                ),
            )
        )
    return tuple(out)
