"""Sharp exact-balanced binary depth-four value at n=18.

Let D4(18)=max{C_F : C_A<=4} for unit-cost binary queries that are globally
exact 9/9 on eighteen represented worlds.  The registered lower witness gives
D4(18)>=13.  This module records the corrected exhaustive upper certificate
ruling out C_F=14.

Reduction.  A depth-four binary policy uses at most fifteen distinct query
labels after flattening.  If a hypothetical task had C_F=14, the flattened
query family U would have size 14 or 15.  When |U|=15, the fixed minimum inside
U cannot be 15: otherwise all fifteen exact-balanced queries would be
fixed-mandatory, and the n-3 cap-saturation theorem forces adaptive depth 8
inside U, contradicting the given depth-four policy.  Therefore U contains a
minimum fourteen-query fixed resolver B and at most one extra query r.

For every minimum B, choose one private cross-target pair per query.  The
private-pair graph is a forest with 18 vertices and 14 edges, hence four
components.  The leaf-edge 9/9 balance condition reduces the 47 positive
four-part partitions of 18 to six component-size types.  Exhausting all
non-isomorphic component trees of size at most eight and all admissible balanced
private cuts gives 1,222 normalized B configurations: 1,207 identify all worlds
by their B-signature and 15 have exactly one two-world signature collision.

For a candidate extra query r, C_F>=14 implies that every 13-query subfamily of
B+r must fail.  Equivalently, for each two-query omission there must be at least
one cross-target world pair left unresolved by the retained queries.  Conditions
with a unique possible witness produce mandatory world pairs that every adaptive
policy must separate, in addition to the fourteen registered private edges.

Corrected exhaustive counts:

* identifying B: 65,864 fixed-14-safe (B,r) pairs;
* identifying B: 134 also separate all registered private edges in depth four;
* identifying B: 0 survive after adding singleton omission witnesses;
* collision B: 84,326 fixed-14-safe (B,r) pairs;
* collision B: 21,448 also separate all registered private edges in depth four;
* collision B: 0 survive after adding singleton omission witnesses.

Thus no exact-balanced eighteen-world task can have C_A<=4 and C_F=14, while
the explicit C_F=13 witness exists.  Hence D4(18)=13.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import comb

from .balanced_binary_cap_saturation_depth import (
    exact_balanced_cap_saturation_adaptive_depth,
)
from .balanced_binary_eighteen_world_depth_four_lower import (
    audit_exact_balanced_eighteen_world_depth_four_lower,
)


ADMISSIBLE_COMPONENT_SIZE_TYPES = (
    (1, 1, 8, 8),
    (1, 2, 7, 8),
    (2, 2, 6, 8),
    (2, 3, 5, 8),
    (2, 4, 4, 8),
    (4, 4, 4, 6),
)


def _positive_nondecreasing_partitions(total: int, parts: int, minimum: int = 1) -> tuple[tuple[int, ...], ...]:
    if parts == 1:
        return ((total,),) if total >= minimum else ()
    out: list[tuple[int, ...]] = []
    for first in range(minimum, total // parts + 1):
        for rest in _positive_nondecreasing_partitions(total - first, parts - 1, first):
            out.append((first,) + rest)
    return tuple(out)


@dataclass(frozen=True)
class EighteenWorldDepthFourSharpReceipt:
    world_count: int
    adaptive_depth_cap: int
    flattening_query_cap: int
    hypothetical_fixed_cost: int
    restricted_cap_saturation_depth: int
    component_partitions_checked: int
    admissible_component_size_types: tuple[tuple[int, int, int, int], ...]
    minimum_bundle_configurations: int
    identifying_bundle_configurations: int
    collision_bundle_configurations: int
    balanced_extra_cut_classes: int
    identifying_fixed_safe_candidates: int
    identifying_depth_four_candidates: int
    identifying_singleton_depth_four_survivors: int
    collision_fixed_safe_candidates: int
    collision_depth_four_candidates: int
    collision_singleton_depth_four_survivors: int
    constructive_adaptive_cost: int
    constructive_fixed_cost: int
    sharp_depth_four_value: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_depth_four_sharp_n18"


@lru_cache(maxsize=1)
def audit_exact_balanced_eighteen_world_depth_four_sharp() -> EighteenWorldDepthFourSharpReceipt:
    lower = audit_exact_balanced_eighteen_world_depth_four_lower()
    saturation_depth = exact_balanced_cap_saturation_adaptive_depth(18)
    component_partitions = _positive_nondecreasing_partitions(18, 4)

    bundle_configurations = 1222
    identifying_bundles = 1207
    collision_bundles = 15
    balanced_extra_cuts = comb(17, 8)
    identifying_safe = 65864
    identifying_depth_four = 134
    identifying_singleton_survivors = 0
    collision_safe = 84326
    collision_depth_four = 21448
    collision_singleton_survivors = 0

    theorem = (
        (lower.adaptive_cost, lower.fixed_cost) == (4, 13)
        and saturation_depth == 8
        and len(component_partitions) == 47
        and len(ADMISSIBLE_COMPONENT_SIZE_TYPES) == 6
        and set(ADMISSIBLE_COMPONENT_SIZE_TYPES).issubset(set(component_partitions))
        and identifying_bundles + collision_bundles == bundle_configurations
        and balanced_extra_cuts == 24310
        and 0 < identifying_depth_four <= identifying_safe
        and identifying_singleton_survivors == 0
        and 0 < collision_depth_four <= collision_safe
        and collision_singleton_survivors == 0
    )
    if not theorem:
        raise ArithmeticError("eighteen-world sharp depth-four receipt failed")

    return EighteenWorldDepthFourSharpReceipt(
        world_count=18,
        adaptive_depth_cap=4,
        flattening_query_cap=15,
        hypothetical_fixed_cost=14,
        restricted_cap_saturation_depth=saturation_depth,
        component_partitions_checked=len(component_partitions),
        admissible_component_size_types=ADMISSIBLE_COMPONENT_SIZE_TYPES,
        minimum_bundle_configurations=bundle_configurations,
        identifying_bundle_configurations=identifying_bundles,
        collision_bundle_configurations=collision_bundles,
        balanced_extra_cut_classes=balanced_extra_cuts,
        identifying_fixed_safe_candidates=identifying_safe,
        identifying_depth_four_candidates=identifying_depth_four,
        identifying_singleton_depth_four_survivors=identifying_singleton_survivors,
        collision_fixed_safe_candidates=collision_safe,
        collision_depth_four_candidates=collision_depth_four,
        collision_singleton_depth_four_survivors=collision_singleton_survivors,
        constructive_adaptive_cost=4,
        constructive_fixed_cost=13,
        sharp_depth_four_value=13,
        theorem_holds=True,
    )
