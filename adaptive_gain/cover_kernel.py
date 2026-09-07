"""Sound kernelization for bounded-cost fixed target-pair cover decisions.

This module preserves the exact yes/no question used by the integer proof layer:
does a fixed resolving bundle of cost <= B exist?  Before branching it repeatedly
applies three safe reductions to the current residual target-pair cover:

1. discard queries that are unaffordable or cover no still-uncovered pair;
2. force a query when some uncovered pair has exactly one remaining separator;
3. discard a dominated query q when another remaining query r covers every
   currently uncovered pair covered by q and cost(r) <= cost(q).

Equal-cost/equal-cover ties keep the lower declared query index, making the
kernel deterministic.  The reductions are exact for the bounded feasibility
question; they are not heuristic lower bounds.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .core import FiniteTask, adaptive_minimum_resolution, bundle_resolves


class CoverKernelLimitError(RuntimeError):
    """Kernelized exact search exceeded its declared canonical-state cap."""


@dataclass(frozen=True)
class KernelizedFixedBudgetDecision:
    budget: int
    fixed_resolver_exists_within_budget: bool
    feasible_bundle: tuple[str, ...] | None
    canonical_branch_states: int
    kernel_calls: int
    forced_query_selections: int
    dominated_query_removals: int
    inactive_or_unaffordable_query_removals: int
    complete_search: bool
    scope: str = "exact_kernelized_integer_target_pair_cover_budget_decision"


@dataclass(frozen=True)
class KernelizedAdaptiveGainAudit:
    adaptive_cost: int | None
    tested_fixed_budget: int | None
    strict_adaptive_gain: bool
    decision: KernelizedFixedBudgetDecision | None
    interpretation: str


def _rows(task: FiniteTask):
    rows = []
    for i, j in combinations(range(len(task.worlds)), 2):
        if task.worlds[i].target == task.worlds[j].target:
            continue
        separators = 0
        for q, query in enumerate(task.queries):
            if query.outcomes[i] != query.outcomes[j]:
                separators |= 1 << q
        rows.append((i, j, separators))
    return tuple(rows)


def _cover_masks(task: FiniteTask, rows):
    masks = []
    for q in range(len(task.queries)):
        mask = 0
        for p, (_, _, separators) in enumerate(rows):
            if separators & (1 << q):
                mask |= 1 << p
        masks.append(mask)
    return tuple(masks)


def kernelized_fixed_budget_cover_decision(
    task: FiniteTask, *, budget: int, max_states: int = 200_000
) -> KernelizedFixedBudgetDecision:
    """Solve bounded fixed-cover feasibility after exact residual kernelization.

    A dominated query q is removable at a residual state when some available r
    satisfies

        cover(q) intersect U  subseteq  cover(r) intersect U
        and cost(r) <= cost(q).

    Any completion containing q can replace q by r (or simply drop q if r is
    already present), never increasing cost and never losing coverage.  A pair
    with one remaining separator forces that query in every feasible completion.
    These rules are applied to a fixed point before every genuine branch.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(max_states) is not int or max_states < 1:
        raise ValueError("max_states must be a positive integer")

    rows = _rows(task)
    if not rows:
        return KernelizedFixedBudgetDecision(budget, True, (), 0, 1, 0, 0, 0, True)
    if any(separators == 0 for _, _, separators in rows):
        return KernelizedFixedBudgetDecision(budget, False, None, 0, 1, 0, 0, 0, True)

    query_count = len(task.queries)
    costs = tuple(query.cost for query in task.queries)
    covers = _cover_masks(task, rows)
    full_uncovered = (1 << len(rows)) - 1
    full_available = (1 << query_count) - 1

    memo: dict[tuple[int, int, int], tuple[bool, tuple[str, ...] | None]] = {}
    canonical_states = 0
    kernel_calls = 0
    forced_count = 0
    dominated_count = 0
    inactive_count = 0

    def reduce_state(uncovered: int, available: int, remaining: int):
        nonlocal kernel_calls, forced_count, dominated_count, inactive_count
        kernel_calls += 1
        forced: list[str] = []
        while True:
            changed = False

            # Unaffordable and currently inactive queries cannot occur in any
            # completion of this residual budget/coverage state.
            remove = []
            for q in range(query_count):
                bit = 1 << q
                if available & bit and (
                    costs[q] > remaining or not (covers[q] & uncovered)
                ):
                    remove.append(q)
            if remove:
                for q in remove:
                    available &= ~(1 << q)
                inactive_count += len(remove)
                changed = True

            if uncovered == 0:
                return "resolved", uncovered, available, remaining, tuple(forced)

            active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]
            unique_q = None
            for p in active_pairs:
                separator_mask = rows[p][2] & available
                separators = [
                    q for q in range(query_count) if separator_mask & (1 << q)
                ]
                if not separators:
                    return "infeasible", uncovered, available, remaining, tuple(forced)
                if len(separators) == 1:
                    unique_q = separators[0]
                    break

            if unique_q is not None:
                q = unique_q
                # Unaffordable queries were removed above, so a forced query is
                # necessarily payable at this residual state.
                forced.append(task.queries[q].name)
                forced_count += 1
                uncovered &= ~covers[q]
                available &= ~(1 << q)
                remaining -= costs[q]
                changed = True
                continue

            # Dominance is evaluated only on still-uncovered obligations.
            available_queries = [q for q in range(query_count) if available & (1 << q)]
            dominated: set[int] = set()
            for q in available_queries:
                q_cover = covers[q] & uncovered
                for r in available_queries:
                    if q == r:
                        continue
                    r_cover = covers[r] & uncovered
                    if q_cover & ~r_cover:
                        continue
                    if costs[r] > costs[q]:
                        continue
                    # Strict cover/cost improvement is enough.  For identical
                    # cover and cost retain the lower query index deterministically.
                    if (
                        costs[r] < costs[q]
                        or r_cover != q_cover
                        or r < q
                    ):
                        dominated.add(q)
                        break
            if dominated:
                for q in dominated:
                    available &= ~(1 << q)
                dominated_count += len(dominated)
                changed = True

            if not changed:
                return "branch", uncovered, available, remaining, tuple(forced)

    def solve(uncovered: int, available: int, remaining: int):
        nonlocal canonical_states
        status, uncovered, available, remaining, forced = reduce_state(
            uncovered, available, remaining
        )
        if status == "resolved":
            return True, forced
        if status == "infeasible":
            return False, None

        key = (uncovered, available, remaining)
        if key in memo:
            ok, suffix = memo[key]
            if ok:
                assert suffix is not None
                return True, forced + suffix
            return False, None
        canonical_states += 1
        if canonical_states > max_states:
            raise CoverKernelLimitError("kernelized cover search state cap reached")

        active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]

        def candidates(p: int):
            separator_mask = rows[p][2] & available
            return tuple(
                q for q in range(query_count) if separator_mask & (1 << q)
            )

        chosen = min(active_pairs, key=lambda p: (len(candidates(p)), p))
        choices = candidates(chosen)
        # reduce_state guarantees at least two available separators here.
        for q in choices:
            ok, child_bundle = solve(
                uncovered & ~covers[q],
                available & ~(1 << q),
                remaining - costs[q],
            )
            if ok:
                assert child_bundle is not None
                suffix = (task.queries[q].name,) + child_bundle
                memo[key] = (True, suffix)
                return True, forced + suffix

        memo[key] = (False, None)
        return False, None

    exists, bundle = solve(full_uncovered, full_available, budget)
    if exists:
        assert bundle is not None
        lookup = {query.name: query.cost for query in task.queries}
        if len(set(bundle)) != len(bundle):
            raise ArithmeticError("kernelized solver repeated a query")
        if sum(lookup[name] for name in bundle) > budget or not bundle_resolves(task, bundle):
            raise ArithmeticError("kernelized solver returned an invalid fixed bundle")
    return KernelizedFixedBudgetDecision(
        budget,
        exists,
        bundle,
        canonical_states,
        kernel_calls,
        forced_count,
        dominated_count,
        inactive_count,
        True,
    )


def selected_policy_kernelized_gain_audit(
    task: FiniteTask, *, max_states: int = 200_000
) -> KernelizedAdaptiveGainAudit:
    """Audit strict gain by exact kernelized fixed feasibility at B=C_A."""
    adaptive = adaptive_minimum_resolution(task)
    ca = adaptive.minimum_worst_path_cost
    if ca is None:
        return KernelizedAdaptiveGainAudit(
            None, None, False, None, "no resolving adaptive policy"
        )
    decision = kernelized_fixed_budget_cover_decision(
        task, budget=ca, max_states=max_states
    )
    strict = not decision.fixed_resolver_exists_within_budget
    return KernelizedAdaptiveGainAudit(
        ca,
        ca,
        strict,
        decision,
        (
            f"kernelized exact decision proves no fixed resolver of cost <= {ca}"
            if strict
            else f"kernelized exact decision found a fixed resolver of cost <= {ca}"
        ),
    )
