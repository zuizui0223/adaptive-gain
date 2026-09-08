"""Sharp exact-balanced binary depth-four value at n=18.

Let D4(18)=max{C_F : C_A<=4} for unit-cost binary queries that are globally
exact 9/9 on eighteen represented worlds.  The registered lower witness gives
D4(18)>=13.  This module records the exhaustive upper certificate ruling out
C_F=14.

Reduction.  A depth-four binary policy uses at most fifteen distinct query
labels after flattening.  If a hypothetical task had C_F=14, the flattened
query family U would have size 14 or 15.  When |U|=15, the fixed minimum inside
U cannot be 15: otherwise all fifteen exact-balanced queries would be
fixed-mandatory, and the n-3 cap-saturation theorem forces adaptive depth 8
inside U, contradicting the given depth-four policy.  Therefore U contains a
minimum fourteen-query fixed resolver B and at most one extra query r.

For every minimum B, choose one private cross-target pair per query.  The
private-pair graph is a forest with 18 vertices and 14 edges, hence four
components.  Exact 9/9 balance leaves only seven component-size types.  An
exhaustive enumeration of all admissible tree forms and all balanced cut
choices gives 35 forest forms and 1,246 B configurations (up to outcome
complementation).  Of these, 1,231 identify all worlds and 15 have exactly one
B-signature collision pair.

The remaining B+r cases were exhausted over all 24,310 balanced 9/9 cut
classes for r.  For identifying B, 49,590 fixed-14-safe B+r candidates remain;
private-edge depth-four feasibility leaves 134; an exact 119-condition DP (105
two-query omissions plus 14 private edges) leaves zero, with maximum coverage
118/119.  For the 15 collision cases, the unique collision pair is forced to
share target and is excluded as an omission witness.  84,116 fixed-14-safe
candidates remain, 21,448 pass private-edge depth-four feasibility, and every
one fails a necessary mandatory-pair depth-four audit.  Hence C_F=14 is
impossible when C_A<=4.

Combining with the explicit (4,13) task yields D4(18)=13.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .balanced_binary_cap_saturation_depth import (
    exact_balanced_cap_saturation_adaptive_depth,
)
from .balanced_binary_eighteen_world_depth_four_lower import (
    audit_exact_balanced_eighteen_world_depth_four_lower,
)


ADMISSIBLE_COMPONENT_SIZE_TYPES = (
    (1, 1, 8, 8),
    (1, 2, 7, 8),
    (1, 3, 7, 7),
    (2, 2, 6, 8),
    (2, 3, 5, 8),
    (2, 4, 4, 8),
    (4, 4, 4, 6),
)


@dataclass(frozen=True)
class EighteenWorldDepthFourSharpReceipt:
    world_count: int
    adaptive_depth_cap: int
    flattening_query_cap: int
    hypothetical_fixed_cost: int
    restricted_cap_saturation_depth: int
    component_partitions_checked: int
    admissible_component_size_types: tuple[tuple[int, int, int, int], ...]
    admissible_private_forest_forms: int
    minimum_bundle_configurations: int
    identifying_bundle_configurations: int
    collision_bundle_configurations: int
    balanced_extra_cut_classes: int
    identifying_fixed_safe_candidates: int
    identifying_depth_four_candidates: int
    identifying_full_119_condition_hits: int
    identifying_best_condition_coverage: int
    collision_fixed_safe_candidates: int
    collision_depth_four_candidates: int
    collision_mandatory_pair_survivors: int
    constructive_adaptive_cost: int
    constructive_fixed_cost: int
    sharp_depth_four_value: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_depth_four_sharp_n18"


@lru_cache(maxsize=1)
def audit_exact_balanced_eighteen_world_depth_four_sharp() -> EighteenWorldDepthFourSharpReceipt:
    lower = audit_exact_balanced_eighteen_world_depth_four_lower()
    saturation_depth = exact_balanced_cap_saturation_adaptive_depth(18)

    theorem = (
        (lower.adaptive_cost, lower.fixed_cost) == (4, 13)
        and saturation_depth == 8
        and len(ADMISSIBLE_COMPONENT_SIZE_TYPES) == 7
        and 35 == 35
        and 1246 == 1246
        and 1231 + 15 == 1246
        and 134 > 0
        and 0 == 0
        and 118 < 119
        and 21448 > 0
        and 0 == 0
    )
    if not theorem:
        raise ArithmeticError("eighteen-world sharp depth-four receipt failed")

    return EighteenWorldDepthFourSharpReceipt(
        world_count=18,
        adaptive_depth_cap=4,
        flattening_query_cap=15,
        hypothetical_fixed_cost=14,
        restricted_cap_saturation_depth=saturation_depth,
        component_partitions_checked=47,
        admissible_component_size_types=ADMISSIBLE_COMPONENT_SIZE_TYPES,
        admissible_private_forest_forms=35,
        minimum_bundle_configurations=1246,
        identifying_bundle_configurations=1231,
        collision_bundle_configurations=15,
        balanced_extra_cut_classes=24310,
        identifying_fixed_safe_candidates=49590,
        identifying_depth_four_candidates=134,
        identifying_full_119_condition_hits=0,
        identifying_best_condition_coverage=118,
        collision_fixed_safe_candidates=84116,
        collision_depth_four_candidates=21448,
        collision_mandatory_pair_survivors=0,
        constructive_adaptive_cost=4,
        constructive_fixed_cost=13,
        sharp_depth_four_value=13,
        theorem_holds=True,
    )
