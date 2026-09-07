"""Public entrypoint for extremal finite adaptive-gain constructions and bounds."""

from .extremal_routing import (
    ExtremalRoutingReceipt,
    RatioThreeHalvesMinimalityReceipt,
    depth_two_fixed_cost_world_bound,
    extremal_routing_receipt,
    k_branch_routing_task,
    ratio_above_three_halves_minimality,
)

__all__ = [
    "ExtremalRoutingReceipt",
    "RatioThreeHalvesMinimalityReceipt",
    "depth_two_fixed_cost_world_bound",
    "extremal_routing_receipt",
    "k_branch_routing_task",
    "ratio_above_three_halves_minimality",
]
