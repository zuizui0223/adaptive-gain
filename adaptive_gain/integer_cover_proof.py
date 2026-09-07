"""Exact proof trees for bounded-cost fixed target-pair cover infeasibility.

To certify strict adaptive gain it is enough to prove that NO fixed resolving
bundle has cost <= C_A.  This module does that without enumerating every bundle:
choose one still-uncovered cross-target pair and branch over every affordable
query that can separate that pair.  If every branch is infeasible, the parent is
infeasible.  The resulting tree is a checkable integer certificate.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations

from .core import FiniteTask, adaptive_minimum_resolution


class IntegerCoverProofLimitError(RuntimeError):
    pass


@dataclass(frozen=True)
class CoverProofBranch:
    query: str
    child: "CoverProofNode"


@dataclass(frozen=True)
class CoverProofNode:
    status: str
    remaining_budget: int
    uncovered_world_pair: tuple[str, str] | None
    affordable_separator_queries: tuple[str, ...]
    branches: tuple[CoverProofBranch, ...]


@dataclass(frozen=True)
class FixedBudgetDecisionCertificate:
    budget: int
    fixed_resolver_exists_within_budget: bool
    feasible_bundle: tuple[str, ...] | None
    infeasibility_proof: CoverProofNode | None
    states_visited: int
    complete_search: bool
    scope: str = "exact_integer_cross_target_pair_cover_budget_decision"


@dataclass(frozen=True)
class IntegerCoverAdaptiveGainCertificate:
    adaptive_cost: int | None
    tested_fixed_budget: int | None
    strict_adaptive_gain_certified_without_fixed_optimum: bool
    fixed_budget_decision: FixedBudgetDecisionCertificate | None
    interpretation: str


def _rows(task: FiniteTask):
    rows = []
    for i, j in combinations(range(len(task.worlds)), 2):
        if task.worlds[i].target == task.worlds[j].target:
            continue
        mask = 0
        for q, query in enumerate(task.queries):
            if query.outcomes[i] != query.outcomes[j]:
                mask |= 1 << q
        rows.append((i, j, mask))
    return tuple(rows)


def fixed_budget_cover_decision(
    task: FiniteTask, *, budget: int, max_states: int = 200_000
) -> FixedBudgetDecisionCertificate:
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(max_states) is not int or max_states < 1:
        raise ValueError("max_states must be a positive integer")
    rows = _rows(task)
    if not rows:
        return FixedBudgetDecisionCertificate(budget, True, (), None, 1, True)
    if any(mask == 0 for _, _, mask in rows):
        i, j, _ = next(row for row in rows if row[2] == 0)
        node = CoverProofNode(
            "unseparable_pair", budget,
            (task.worlds[i].name, task.worlds[j].name), (), ()
        )
        return FixedBudgetDecisionCertificate(budget, False, None, node, 1, True)

    costs = tuple(q.cost for q in task.queries)
    full_available = (1 << len(task.queries)) - 1
    full_uncovered = (1 << len(rows)) - 1
    cover_masks = []
    for q in range(len(task.queries)):
        cover = 0
        for p, (_, _, separators) in enumerate(rows):
            if separators & (1 << q):
                cover |= 1 << p
        cover_masks.append(cover)
    states = 0

    @lru_cache(None)
    def search(uncovered: int, available: int, remaining: int):
        nonlocal states
        states += 1
        if states > max_states:
            raise IntegerCoverProofLimitError("integer cover proof state cap reached")
        if uncovered == 0:
            return True, (), None

        active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]
        def affordable(p):
            sep = rows[p][2] & available
            return tuple(q for q in range(len(task.queries))
                         if sep & (1 << q) and costs[q] <= remaining)
        chosen = min(active_pairs, key=lambda p: (len(affordable(p)), p))
        candidates = affordable(chosen)
        i, j, _ = rows[chosen]
        pair_name = (task.worlds[i].name, task.worlds[j].name)
        if not candidates:
            node = CoverProofNode("no_affordable_separator", remaining, pair_name, (), ())
            return False, None, node

        proof_branches = []
        for q in candidates:
            ok, bundle, child = search(
                uncovered & ~cover_masks[q],
                available & ~(1 << q),
                remaining - costs[q],
            )
            if ok:
                return True, (task.queries[q].name,) + bundle, None
            assert child is not None
            proof_branches.append(CoverProofBranch(task.queries[q].name, child))
        node = CoverProofNode(
            "all_affordable_separators_infeasible", remaining, pair_name,
            tuple(task.queries[q].name for q in candidates), tuple(proof_branches),
        )
        return False, None, node

    exists, bundle, proof = search(full_uncovered, full_available, budget)
    return FixedBudgetDecisionCertificate(
        budget, exists, bundle, proof, states, True
    )


def selected_policy_integer_cover_gain_certificate(
    task: FiniteTask, *, max_states: int = 200_000
) -> IntegerCoverAdaptiveGainCertificate:
    adaptive = adaptive_minimum_resolution(task)
    ca = adaptive.minimum_worst_path_cost
    if ca is None:
        return IntegerCoverAdaptiveGainCertificate(
            None, None, False, None, "no resolving adaptive policy"
        )
    decision = fixed_budget_cover_decision(task, budget=ca, max_states=max_states)
    strict = not decision.fixed_resolver_exists_within_budget
    return IntegerCoverAdaptiveGainCertificate(
        ca, ca, strict, decision,
        (f"proved no fixed resolver of cost <= {ca}; therefore C_F > C_A"
         if strict else
         f"found a fixed resolver of cost <= adaptive cost {ca}; no strict cost gain"),
    )
