"""Exact symmetric-noise extension of the minimal temporal routing model.

The model preserves the four-world strict-gain semantics while allowing the
routing cue and specialist cues to be observed through independent binary
symmetric channels. Reliabilities are restricted to [1/2, 1]; below-chance
binary cues can be relabelled.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

from .temporal_routing import FIXED_QUERY_PAIRS, left_outcome, right_outcome

QueryName = Literal["route", "left", "right"]
RoutingRule = Literal["persistence", "alternation"]


def _probability(value: float, name: str) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")
    return value


def _reliability(value: float, name: str) -> float:
    value = float(value)
    if not 0.5 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0.5, 1]")
    return value


def temporal_signal(rho: float) -> float:
    """Signed lag-one binary-context predictability: phi = 2*rho - 1."""
    rho = _probability(rho, "rho")
    return 2.0 * rho - 1.0


def routing_signal(routing_reliability: float) -> float:
    """Chance-centred routing-cue reliability eta_R = 2*a - 1."""
    a = _reliability(routing_reliability, "routing_reliability")
    return 2.0 * a - 1.0


def specialist_signal(specialist_reliability: float) -> float:
    """Chance-centred specialist reliability eta_S = 2*b - 1."""
    b = _reliability(specialist_reliability, "specialist_reliability")
    return 2.0 * b - 1.0


def fixed_accuracy_formula(specialist_reliability: float) -> float:
    """Exact Bayes accuracy of every two-query fixed pair."""
    b = _reliability(specialist_reliability, "specialist_reliability")
    return 0.5 + (2.0 * b - 1.0) / 4.0


def signed_routing_term(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
) -> float:
    """Signed advantage of persistence-following over the fixed baseline."""
    return (
        temporal_signal(rho)
        * routing_signal(routing_reliability)
        * specialist_signal(specialist_reliability)
        / 4.0
    )


def noisy_gain_formula(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
) -> float:
    """Exact optimal fixed-versus-contingent Bayes-accuracy gain."""
    return abs(signed_routing_term(rho, routing_reliability, specialist_reliability))


def _bsc(bit: int, reliability: float) -> tuple[tuple[int, float], tuple[int, float]]:
    return ((int(bit), reliability), (1 - int(bit), 1.0 - reliability))


def _base_outcome(query: QueryName, target: int, context: int) -> int:
    if query == "left":
        return left_outcome(target, context)
    if query == "right":
        return right_outcome(target, context)
    raise ValueError(f"not a specialist query: {query}")


def _state_probability(target: int, context0: int, context1: int, rho: float) -> float:
    del target
    transition = rho if context1 == context0 else 1.0 - rho
    return 0.25 * transition


def _bayes_accuracy(joint: dict[tuple[object, ...], list[float]]) -> float:
    return sum(max(target_mass) for target_mass in joint.values())


def noisy_fixed_pair_accuracy(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
    pair: tuple[QueryName, QueryName],
) -> float:
    """Enumerate exact Bayes accuracy for one precommitted two-query pair."""
    rho = _probability(rho, "rho")
    a = _reliability(routing_reliability, "routing_reliability")
    b = _reliability(specialist_reliability, "specialist_reliability")
    if pair not in FIXED_QUERY_PAIRS and tuple(reversed(pair)) not in FIXED_QUERY_PAIRS:
        raise ValueError(f"pair must be one of {FIXED_QUERY_PAIRS}")

    joint: dict[tuple[object, ...], list[float]] = defaultdict(lambda: [0.0, 0.0])
    for target in (0, 1):
        for context0 in (0, 1):
            for context1 in (0, 1):
                p_state = _state_probability(target, context0, context1, rho)
                distribution: dict[tuple[int, ...], float] = {(): 1.0}
                for query in pair:
                    reliability = a if query == "route" else b
                    latent = context0 if query == "route" else _base_outcome(query, target, context1)
                    updated: dict[tuple[int, ...], float] = defaultdict(float)
                    for history, p_history in distribution.items():
                        for observation, p_obs in _bsc(latent, reliability):
                            updated[history + (observation,)] += p_history * p_obs
                    distribution = updated
                for observation, p_obs in distribution.items():
                    joint[observation][target] += p_state * p_obs
    return _bayes_accuracy(joint)


def best_noisy_fixed_two_query_accuracy(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
) -> float:
    """Best exact Bayes accuracy across all two-query fixed pairs."""
    return max(
        noisy_fixed_pair_accuracy(
            rho,
            routing_reliability,
            specialist_reliability,
            pair,
        )
        for pair in FIXED_QUERY_PAIRS
    )


def _terminal_query(observed_route: int, rule: RoutingRule) -> QueryName:
    if rule == "persistence":
        return "right" if observed_route == 0 else "left"
    if rule == "alternation":
        return "left" if observed_route == 0 else "right"
    raise ValueError("rule must be 'persistence' or 'alternation'")


def noisy_adaptive_two_query_accuracy(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
    rule: RoutingRule,
) -> float:
    """Enumerate Bayes accuracy for route-first contingent specialist sensing."""
    rho = _probability(rho, "rho")
    a = _reliability(routing_reliability, "routing_reliability")
    b = _reliability(specialist_reliability, "specialist_reliability")

    joint: dict[tuple[object, ...], list[float]] = defaultdict(lambda: [0.0, 0.0])
    for target in (0, 1):
        for context0 in (0, 1):
            for context1 in (0, 1):
                p_state = _state_probability(target, context0, context1, rho)
                for observed_route, p_route in _bsc(context0, a):
                    query = _terminal_query(observed_route, rule)
                    latent_specialist = _base_outcome(query, target, context1)
                    for observed_specialist, p_specialist in _bsc(latent_specialist, b):
                        observation = (observed_route, query, observed_specialist)
                        joint[observation][target] += p_state * p_route * p_specialist
    return _bayes_accuracy(joint)


def optimal_noisy_adaptive_two_query_accuracy(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
) -> float:
    """Best exact accuracy of persistence- versus alternation-following routing."""
    return max(
        noisy_adaptive_two_query_accuracy(
            rho, routing_reliability, specialist_reliability, "persistence"
        ),
        noisy_adaptive_two_query_accuracy(
            rho, routing_reliability, specialist_reliability, "alternation"
        ),
    )


def noisy_temporal_adaptive_gain(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
) -> float:
    """Exact contingent-sensing gain over the best two-query fixed bundle."""
    return optimal_noisy_adaptive_two_query_accuracy(
        rho, routing_reliability, specialist_reliability
    ) - best_noisy_fixed_two_query_accuracy(
        rho, routing_reliability, specialist_reliability
    )


def optimal_noisy_routing_rule(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
) -> str:
    """Qualitative optimal rule; returns indifferent whenever exact gain is zero."""
    term = signed_routing_term(rho, routing_reliability, specialist_reliability)
    if term > 0.0:
        return "persistence"
    if term < 0.0:
        return "alternation"
    return "indifferent"


def noisy_evolutionary_net_gain(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
    *,
    accuracy_value: float = 1.0,
    routing_control_cost: float = 0.0,
) -> float:
    """Fitness-scaled noisy routing gain after an extra contingent-control cost."""
    if accuracy_value < 0.0:
        raise ValueError("accuracy_value must be nonnegative")
    if routing_control_cost < 0.0:
        raise ValueError("routing_control_cost must be nonnegative")
    return (
        accuracy_value
        * noisy_gain_formula(rho, routing_reliability, specialist_reliability)
        - routing_control_cost
    )


@dataclass(frozen=True)
class NoisyTemporalRoutingReceipt:
    rho: float
    routing_reliability: float
    specialist_reliability: float
    temporal_signal: float
    routing_signal: float
    specialist_signal: float
    fixed_accuracy: float
    persistence_accuracy: float
    alternation_accuracy: float
    optimal_adaptive_accuracy: float
    adaptive_gain: float
    optimal_rule: str


def noisy_temporal_routing_receipt(
    rho: float,
    routing_reliability: float,
    specialist_reliability: float,
) -> NoisyTemporalRoutingReceipt:
    fixed = best_noisy_fixed_two_query_accuracy(
        rho, routing_reliability, specialist_reliability
    )
    persistence = noisy_adaptive_two_query_accuracy(
        rho, routing_reliability, specialist_reliability, "persistence"
    )
    alternation = noisy_adaptive_two_query_accuracy(
        rho, routing_reliability, specialist_reliability, "alternation"
    )
    adaptive = max(persistence, alternation)
    return NoisyTemporalRoutingReceipt(
        rho=float(rho),
        routing_reliability=float(routing_reliability),
        specialist_reliability=float(specialist_reliability),
        temporal_signal=temporal_signal(rho),
        routing_signal=routing_signal(routing_reliability),
        specialist_signal=specialist_signal(specialist_reliability),
        fixed_accuracy=fixed,
        persistence_accuracy=persistence,
        alternation_accuracy=alternation,
        optimal_adaptive_accuracy=adaptive,
        adaptive_gain=adaptive - fixed,
        optimal_rule=optimal_noisy_routing_rule(
            rho, routing_reliability, specialist_reliability
        ),
    )
