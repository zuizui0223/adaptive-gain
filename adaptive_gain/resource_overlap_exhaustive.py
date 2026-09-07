"""Exact registered classification of the first resource-role ambiguity.

Scope:

    four balanced target worlds
    four binary unit-cost queries
    all 16^4 = 65,536 labeled tasks

The first pass groups tasks by cost-only continuation root class plus the multiset
of per-resource abstract role profiles. Exactly one such class mixes fixed costs.
The second pass canonicalizes concrete state-resource co-location only inside that
ambiguous class. In this finite scope, co-location separates the two fixed-cost
families perfectly.

This is a scope-specific exhaustive theorem, not a general sufficiency theorem for
state-resource co-location.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import permutations, product


@dataclass(frozen=True)
class ResourceCoLocationRepairSummary:
    task_count: int
    resource_role_signature_count: int
    role_ambiguous_signature_count: int
    role_ambiguous_task_count: int
    colocation_signature_count_within_ambiguous_role_class: int
    colocation_ambiguous_signature_count: int
    colocation_cost_pair_counts: tuple[tuple[tuple[int | None, int | None], int], ...]
    scope: str = "balanced_four_world_four_binary_query_colocation_repair_exact_scan"


def _scan_role_records():
    targets = (0, 0, 1, 1)
    patterns = tuple(product((0, 1), repeat=4))
    intern: dict[tuple, int] = {}
    class_values: dict[int, int | None] = {0: 0}
    next_id = 1
    records = defaultdict(list)

    def pure(mask: int) -> bool:
        return len({targets[i] for i in range(4) if mask & (1 << i)}) <= 1

    for maps in product(patterns, repeat=4):
        memberships: dict[tuple[int, int], int] = {}
        profiles: list[set[tuple]] = [set() for _ in range(4)]

        def groups(world_mask: int, q: int) -> tuple[int, ...]:
            zero = one = 0
            for i in range(4):
                if not (world_mask & (1 << i)):
                    continue
                if maps[q][i]:
                    one |= 1 << i
                else:
                    zero |= 1 << i
            return tuple(mask for mask in (zero, one) if mask)

        def visit(world_mask: int, remaining: int) -> int:
            nonlocal next_id
            key = (world_mask, remaining)
            if key in memberships:
                return memberships[key]
            if pure(world_mask):
                memberships[key] = 0
                return 0
            actions = set()
            local = []
            for q in range(4):
                bit = 1 << q
                if not (remaining & bit):
                    continue
                cells = groups(world_mask, q)
                if len(cells) <= 1:
                    continue
                children = set()
                for child in cells:
                    if not pure(child):
                        children.add(visit(child, remaining & ~bit))
                action = (1, tuple(sorted(children)))
                actions.add(action)
                local.append((q, action))
            descriptor = tuple(sorted(actions))
            cid = intern.get(descriptor)
            if cid is None:
                cid = next_id
                next_id += 1
                intern[descriptor] = cid
                candidates = []
                for cost, children in descriptor:
                    values = [class_values[child] for child in children]
                    if any(value is None for value in values):
                        continue
                    candidates.append(cost + max(values, default=0))
                class_values[cid] = min(candidates) if candidates else None
            memberships[key] = cid
            for q, action in local:
                profiles[q].add((cid, action))
            return cid

        root = visit(0b1111, 0b1111)
        role_signature = (
            root,
            tuple(sorted((tuple(sorted(profile)) for profile in profiles), key=repr)),
        )
        fixed = None
        for bundle in range(16):
            cost = bundle.bit_count()
            if fixed is not None and cost >= fixed:
                continue
            if all(
                any(bundle & (1 << q) and maps[q][i] != maps[q][j] for q in range(4))
                for i, j in ((0, 2), (0, 3), (1, 2), (1, 3))
            ):
                fixed = cost
        records[role_signature].append((class_values[root], fixed, maps))
    return records, intern, class_values


def _colocation_signature(maps, intern: dict[tuple, int]):
    targets = (0, 0, 1, 1)
    memberships: dict[tuple[int, int], int] = {}

    def pure(mask: int) -> bool:
        return len({targets[i] for i in range(4) if mask & (1 << i)}) <= 1

    def groups(world_mask: int, q: int) -> tuple[int, ...]:
        zero = one = 0
        for i in range(4):
            if not (world_mask & (1 << i)):
                continue
            if maps[q][i]:
                one |= 1 << i
            else:
                zero |= 1 << i
        return tuple(mask for mask in (zero, one) if mask)

    def visit(world_mask: int, remaining: int) -> int:
        key = (world_mask, remaining)
        if key in memberships:
            return memberships[key]
        if pure(world_mask):
            memberships[key] = 0
            return 0
        actions = set()
        for q in range(4):
            bit = 1 << q
            if not (remaining & bit):
                continue
            cells = groups(world_mask, q)
            if len(cells) <= 1:
                continue
            children = set()
            for child in cells:
                if not pure(child):
                    children.add(visit(child, remaining & ~bit))
            actions.add((1, tuple(sorted(children))))
        cid = intern[tuple(sorted(actions))]
        memberships[key] = cid
        return cid

    visit(0b1111, 0b1111)
    rows = []
    for (world_mask, remaining), parent in memberships.items():
        if parent == 0:
            continue
        cells_by_query = []
        for q in range(4):
            bit = 1 << q
            if not (remaining & bit):
                cells_by_query.append(("U",))
                continue
            cells = groups(world_mask, q)
            if len(cells) <= 1:
                cells_by_query.append(("C",))
                continue
            children = set()
            for child in cells:
                if not pure(child):
                    children.add(memberships[(child, remaining & ~bit)])
            cells_by_query.append(("P", tuple(sorted(children))))
        rows.append((parent, tuple(cells_by_query)))

    best = None
    for order in permutations(range(4)):
        candidate = tuple(sorted(
            (parent, tuple(cells[q] for q in order))
            for parent, cells in rows
        ))
        if best is None or candidate < best:
            best = candidate
    return best


def enumerate_balanced_four_query_colocation_repair() -> ResourceCoLocationRepairSummary:
    records, intern, _ = _scan_role_records()
    ambiguous = [
        rows for rows in records.values()
        if len({(adaptive, fixed) for adaptive, fixed, _ in rows}) > 1
    ]
    colocation = defaultdict(Counter)
    for rows in ambiguous:
        for adaptive, fixed, maps in rows:
            colocation[_colocation_signature(maps, intern)][(adaptive, fixed)] += 1

    ambiguous_colocation = [counts for counts in colocation.values() if len(counts) > 1]
    merged = Counter()
    for counts in colocation.values():
        merged.update(counts)
    return ResourceCoLocationRepairSummary(
        16 ** 4,
        len(records),
        len(ambiguous),
        sum(len(rows) for rows in ambiguous),
        len(colocation),
        len(ambiguous_colocation),
        tuple(sorted(merged.items(), key=repr)),
    )
