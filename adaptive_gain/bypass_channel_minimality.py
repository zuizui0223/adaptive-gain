"""Sharp query-count minima for internal and external fixed bypass channels.

For one selected optimal adaptive policy let S be its distinct query union.
With positive query costs, if |S|<=2 then every query in S lies on one worst
root-to-leaf path: with one resource this is immediate; with two, one is the
root and any genuinely used second resource occurs below it.  Hence C_A=c(S)=U.
The containment C_A<=C_F<=C_U<=U then forces equality, so neither internal nor
external bypass is possible.

Consequences:
* positive internal union redundancy requires at least three declared queries;
* positive external shortcut discount requires at least four declared queries,
  because with exactly three union queries and only three declared resources
  there is no outside resource.

Registered controls attain both bounds exactly.
"""
from __future__ import annotations

from dataclasses import dataclass

from .frontier_transversals import frontier_transversal_policy_decomposition
from .witnesses import external_shortcut_control, routing_bypass_control


@dataclass(frozen=True)
class BypassChannelQueryMinimalityReceipt:
    internal_minimum_declared_queries: int
    external_minimum_declared_queries: int
    internal_witness_query_count: int
    internal_witness_redundancy: int
    external_witness_query_count: int
    external_witness_discount: int
    internal_bound_attained: bool
    external_bound_attained: bool
    scope: str = "positive_cost_selected_optimal_policy_bypass_channel_query_count_minimality"


def bypass_channel_query_minimality() -> BypassChannelQueryMinimalityReceipt:
    """Return executable witnesses for the sharp 3-query/4-query lower bounds."""
    internal_task = routing_bypass_control()
    external_task = external_shortcut_control()
    internal = frontier_transversal_policy_decomposition(internal_task)
    external = frontier_transversal_policy_decomposition(external_task)
    internal_count = len(internal_task.queries)
    external_count = len(external_task.queries)
    internal_value = internal.internal_union_redundancy or 0
    external_value = external.external_shortcut_discount or 0
    return BypassChannelQueryMinimalityReceipt(
        3,
        4,
        internal_count,
        internal_value,
        external_count,
        external_value,
        internal_count == 3 and internal_value > 0,
        external_count == 4 and external_value > 0,
    )
