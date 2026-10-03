"""Minimal temporal extension of the four-world strict adaptive-gain normal form.

The hidden state during one sensing episode is (target, context). The target is
held fixed over the two sensing steps while the binary context can persist or
flip. A routing observation reveals the initial context. The two terminal
queries are exactly the branch-specific queries of the minimal deterministic
normal form.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

QueryName = Literal["route", "left", "right"]
RoutingRule = Literal["persistence", "alternation"]

FIXED_QUERY_PAIRS: tuple[tuple[QueryName, QueryName], ...] = (
    ("route", "left"),
    ("route", "right"),
    ("left", "right"),
)


def _validate_rho(rho: float) -> float:
    rho = float(rho)
    if not 0.0 <= rho <= 1.0:
        raise ValueError("rho must lie in [0, 1]")
    return rho


def temporal_autocorrelation(rho: float) -> float:
    """Return the signed binary-context autocorrelation phi = 2*rho - 1."""
    rho = _validate_rho(rho)
    return 2.0 * rho - 1.0


def left_outcome(target: int, context: int) -> int:
    """Left specialist: diagnostic in context 1, constant 0 in context 0."""
    return int(target) if int(context) == 1 else 0


def right_outcome(target: int, context: int) -> int:
    """Right specialist: diagnostic in context 0, constant 1 in context 1."""
    return int(target) if int(context) == 0 else 1


def _query_outcome(query: QueryName, target: int, context0: int, context1: int) -> int:
    if query == "route":
        return int(context0)
    if query == "left":
        return left_outcome(target, context1)
    if query == "right":
        return right_outcome(target, context1)
    raise ValueError(f"unknown query: {query}")


def _state_probability(target: int, context0: int, context1: int, rho: float) -> float:
    transition = rho if context1 == context0 else 1.0 - rho
    return 0.25 * transition


def _bayes_accuracy(joint_by_observation: dict[tuple[object, ...], list[float]]) -> float:
    return sum(max(target_mass) for target_mass in joint_by_observation.values())


def fixed_pair_accuracy(rho: float, pair: tuple[QueryName, QueryName]) -> float:
    """Bayes-optimal target accuracy for a precommitted two-query bundle."""
    rho = _validate_rho(rho)
    if pair not in FIXED_QUERY_PAIRS and tuple(reversed(pair)) not in FIXED_QUERY_PAIRS:
        raise ValueError(f"pair must be one of {FIXED_QUERY_PAIRS}")
    joint: dict[tuple[object, ...], list[float]] = defaultdict(lambda: [0.0, 0.0])
    for target in (0, 1):
        for context0 in (0, 1):
            for context1 in (0, 1):
                probability = _state_probability(target, context0, context1, rho)
                observation = tuple(
                    _query_outcome(query, target, context0, context1) for query in pair
                )
                joint[observation][target] += probability
    return _bayes_accuracy(joint)


def best_fixed_two_query_accuracy(rho: float) -> float:
    """Best Bayes accuracy among all two-query fixed bundles in the minimal core."""
    rho = _validate_rho(rho)
    return max(fixed_pair_accuracy(rho, pair) for pair in FIXED_QUERY_PAIRS)


def _terminal_query(context0: int, rule: RoutingRule) -> QueryName:
    if rule == "persistence":
        return "right" if context0 == 0 else "left"
    if rule == "alternation":
        return "left" if context0 == 0 else "right"
    raise ValueError("rule must be 'persistence' or 'alternation'")


def adaptive_two_query_accuracy(rho: float, rule: RoutingRule) -> float:
    """Bayes accuracy after route-first, then an outcome-contingent terminal query."""
    rho = _validate_rho(rho)
    joint: dict[tuple[object, ...], list[float]] = defaultdict(lambda: [0.0, 0.0])
    for target in (0, 1):
        for context0 in (0, 1):
            query = _terminal_query(context0, rule)
            for context1 in (0, 1):
                probability = _state_probability(target, context0, context1, rho)
                terminal = _query_outcome(query, target, context0, context1)
                observation = (context0, query, terminal)
                joint[observation][target] += probability
    return _bayes_accuracy(joint)


def optimal_adaptive_two_query_accuracy(rho: float) -> float:
    """Best of persistence-following and alternation-following contingent routing."""
    rho = _validate_rho(rho)
    return max(
        adaptive_two_query_accuracy(rho, "persistence"),
        adaptive_two_query_accuracy(rho, "alternation"),
    )


def optimal_routing_rule(rho: float) -> str:
    """Return the optimal qualitative rule; at rho=1/2 both rules tie."""
    rho = _validate_rho(rho)
    if rho > 0.5:
        return "persistence"
    if rho < 0.5:
        return "alternation"
    return "indifferent"


def temporal_adaptive_gain(rho: float) -> float:
    """Accuracy gain of the best two-query adaptive policy over the best fixed pair."""
    rho = _validate_rho(rho)
    return optimal_adaptive_two_query_accuracy(rho) - best_fixed_two_query_accuracy(rho)


def evolutionary_net_gain(
    rho: float,
    *,
    accuracy_value: float = 1.0,
    routing_control_cost: float = 0.0,
) -> float:
    """Fitness-scaled gain after a cost for maintaining/using contingent control."""
    if accuracy_value < 0.0:
        raise ValueError("accuracy_value must be nonnegative")
    if routing_control_cost < 0.0:
        raise ValueError("routing_control_cost must be nonnegative")
    return accuracy_value * temporal_adaptive_gain(rho) - routing_control_cost


@dataclass(frozen=True)
class TemporalRoutingReceipt:
    rho: float
    temporal_autocorrelation: float
    fixed_two_query_accuracy: float
    persistence_accuracy: float
    alternation_accuracy: float
    optimal_adaptive_accuracy: float
    optimal_rule: str
    adaptive_accuracy_gain: float


def temporal_routing_receipt(rho: float) -> TemporalRoutingReceipt:
    rho = _validate_rho(rho)
    persistence = adaptive_two_query_accuracy(rho, "persistence")
    alternation = adaptive_two_query_accuracy(rho, "alternation")
    fixed = best_fixed_two_query_accuracy(rho)
    adaptive = max(persistence, alternation)
    return TemporalRoutingReceipt(
        rho=rho,
        temporal_autocorrelation=temporal_autocorrelation(rho),
        fixed_two_query_accuracy=fixed,
        persistence_accuracy=persistence,
        alternation_accuracy=alternation,
        optimal_adaptive_accuracy=adaptive,
        optimal_rule=optimal_routing_rule(rho),
        adaptive_accuracy_gain=adaptive - fixed,
    )
