"""Sound kernelization for bounded-cost fixed target-pair cover decisions.

This module preserves the exact yes/no question used by the integer proof layer:
does a fixed resolving bundle of cost <= B exist? Before branching it repeatedly
applies four safe reductions to the current residual target-pair cover:

1. discard queries that are unaffordable or cover no still-uncovered pair;
2. discard a redundant pair obligation whose remaining separator set contains
   another still-uncovered pair's separator set;
3. force a query when some uncovered pair has exactly one remaining separator;
4. discard a dominated query q when another remaining query r covers every
   currently uncovered pair covered by q and cost(r) <= cost(q).

The reductions are exact for the bounded feasibility question; they are not
heuristic lower bounds. Equal signatures use declared order only to make the
kernel deterministic.
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
    dominated_pair_removals: int
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

    Query dominance removes q when another available r has a residual cover
    superset at weakly lower cost. Pair-obligation dominance is the dual rule:
    if the remaining separator set of pair p is contained in that of pair s,
    then satisfying p automatically satisfies s, so s is redundant.

    Forced unique separators, pair/query dominance, and inactive deletion are
    iterated to a fixed point before every genuine branch.
    """
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(max_states) is not int or max_states < 1:
        raise ValueError("max_states must be a positive integer")

    rows = _rows(task)
    if not rows:
        return KernelizedFixedBudgetDecision(budget, True, (), 0, 1, 0, 0, 0, 0, True)
    if any(separators == 0 for _, _, separators in rows):
        return KernelizedFixedBudgetDecision(budget, False, None, 0, 1, 0, 0, 0, 0, True)

    query_count = len(task.queries)
    costs = tuple(query.cost for query in task.queries)
    covers = _cover_masks(task, rows)
    full_uncovered = (1 << len(rows)) - 1
    full_available = (1 << query_count) - 1

    memo: dict[tuple[int, int, int], tuple[bool, tuple[str, ...] | None]] = {}
    canonical_states = 0
    kernel_calls = 0
    forced_count = 0
    dominated_query_count = 0
    dominated_pair_count = 0
    inactive_count = 0

    def reduce_state(uncovered: int, available: int, remaining: int):
        nonlocal kernel_calls, forced_count, dominated_query_count, dominated_pair_count, inactive_count
        kernel_calls += 1
        forced: list[str] = []
        while True:
            changed = False

            # Queries that cannot participate in any completion of the current
            # residual decision are removed exactly.
            remove_queries = []
            for q in range(query_count):
                bit = 1 << q
                if available & bit and (
                    costs[q] > remaining or not (covers[q] & uncovered)
                ):
                    remove_queries.append(q)
            if remove_queries:
                for q in remove_queries:
                    available &= ~(1 << q)
                inactive_count += len(remove_queries)
                changed = True

            if uncovered == 0:
                return "resolved", uncovered, available, remaining, tuple(forced)

            active_pairs = [p for p in range(len(rows)) if uncovered & (1 << p)]
            separator_sets = {p: rows[p][2] & available for p in active_pairs}
            if any(mask == 0 for mask in separator_sets.values()):
                return "infeasible", uncovered, available, remaining, tuple(forced)

            # Pair-obligation dominance: if Sep(hard) subseteq Sep(easy), every
            # completion covering hard also covers easy. Remove easy. Equal
            # separator sets keep the lower pair index deterministically.
            dominated_pairs: set[int] = set()
            for easy in active_pairs:
                easy_sep = separator_sets[easy]
                for hard in active_pairs:
                    if easy == hard:
                        continue
                    hard_sep = separator_sets[hard]
                    if hard_sep & ~easy_sep:
                        continue
                    if hard_sep != easy_sep or hard < easy:
                        dominated_pairs.add(easy)
                        break
            if dominated_pairs:
                for p in dominated_pairs:
                    uncovered &= ~(1 << p)
                dominated_pair_count += len(dominated_pairs)
                # Removing pair obligations can make queries inactive, so restart.
                continue

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
                forced.append(task.queries[q].name)
                forced_count += 1
                uncovered &= ~covers[q]
                available &= ~(1 << q)
                remaining -= costs[q]
                continue

            # Query dominance is evaluated on the remaining obligation antichain.
            available_queries = [q for q in range(query_count) if available & (1 << q)]
            dominated_queries: set[int] = set()
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
                    if costs[r] < costs[q] or r_cover != q_cover or r < q:
                        dominated_queries.add(q)
                        break
            if dominated_queries:
                for q in dominated_queries:
                    available &= ~(1 << q)
                dominated_query_count += len(dominated_queries)
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
        dominated_query_count,
        dominated_pair_count,
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
