"""Sharp unit-cost adaptive/fixed ratio at fixed worlds, queries, and query arity.

Let F_b(n,h) be the exact maximum number of internal-node occurrences in a
productive rooted decision tree with at most n nonempty leaves, height at most h,
and every internal node having between two and b nonempty children.  It obeys the
exact recurrence

    F_b(1,h)=F_b(n,0)=0,

and for n>=2,h>=1

    F_b(n,h)
      = 1 + max_{2<=r<=min(b,n)}
          max_{n_1+...+n_r<=n, n_i>=1}
          sum_i F_b(n_i,h-1).

For a finite deterministic unit-cost task with n represented worlds, m declared
queries, maximum query arity b, and adaptive optimum C_A=h, flattening a selected
optimal adaptive tree gives

    C_F <= min(m, F_b(n,h)).

Therefore the sharp ratio is

    R_b(n,m) = max_{1<=h<=n-1} min(m,F_b(n,h))/h.

Sharpness is constructive.  Any bounded-arity tree can be turned into a task with
one physical query per internal node.  At node v, q_v reports the child index on
leaves below v and returns 0 outside v.  For each v, connect the leftmost leaf of
child 0 to the leftmost leaf of child 1.  These private-pair edges form a forest,
so they can be two-coloured as target labels.  The edge for v is separated by q_v
and by no other query, making every internal-node query fixed-mandatory.  The tree
itself is an adaptive resolving policy.

The theorem interpolates exactly between the registered endpoints:

* b=2: binary sharp world/query bound;
* b>=n: unrestricted-arity sharp world/query bound.

Scope: finite deterministic guaranteed target resolution, unit acquisition costs,
and a hard cap b on the number of distinct outcomes of every declared query.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class BoundedArityTree:
    children: tuple["BoundedArityTree", ...] = ()

    @property
    def is_leaf(self) -> bool:
        return not self.children


@dataclass(frozen=True)
class BoundedArityTreeBoundReceipt:
    world_count: int
    adaptive_depth: int
    max_arity: int
    maximum_internal_occurrences: int
    scope: str = "productive_tree_bounded_arity_internal_occurrence_bound"


@dataclass(frozen=True)
class BoundedArityRatioReceipt:
    world_count: int
    query_count: int
    max_arity: int
    sharp_ratio: Fraction
    maximizing_depths: tuple[int, ...]
    witness_adaptive_cost: int | None
    witness_fixed_cost: int | None
    witness_ratio: Fraction | None
    direct_check_performed: bool
    direct_check_agrees: bool
    private_pair_count: int
    theorem_holds: bool
    scope: str = "sharp_unit_cost_ratio_fixed_world_query_arity"


def _validate(world_count: int, depth: int, max_arity: int) -> None:
    if type(world_count) is not int or world_count < 1:
        raise ValueError("world_count must be a positive integer")
    if type(depth) is not int or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")


@lru_cache(None)
def maximum_bounded_arity_tree_internal_nodes(
    world_count: int,
    depth: int,
    max_arity: int,
) -> int:
    """Exact F_b(n,h) via a child-budget dynamic program."""
    _validate(world_count, depth, max_arity)
    if world_count <= 1 or depth == 0:
        return 0

    best = 0
    for child_count in range(2, min(max_arity, world_count) + 1):
        # dp[(used children, allocated leaf budget)] = best child-subtree total.
        dp = {(0, 0): 0}
        for used_children in range(child_count):
            nxt: dict[tuple[int, int], int] = {}
            remaining_children = child_count - used_children - 1
            for (_, used_budget), score in dp.items():
                max_budget = world_count - used_budget - remaining_children
                for child_budget in range(1, max_budget + 1):
                    key = (used_children + 1, used_budget + child_budget)
                    value = score + maximum_bounded_arity_tree_internal_nodes(
                        child_budget, depth - 1, max_arity
                    )
                    if value > nxt.get(key, -1):
                        nxt[key] = value
            dp = nxt
        child_best = max(
            score for (used, budget), score in dp.items()
            if used == child_count and budget <= world_count
        )
        best = max(best, 1 + child_best)
    return best


def bounded_arity_tree_bound_receipt(
    world_count: int,
    depth: int,
    max_arity: int,
) -> BoundedArityTreeBoundReceipt:
    return BoundedArityTreeBoundReceipt(
        world_count,
        depth,
        max_arity,
        maximum_bounded_arity_tree_internal_nodes(world_count, depth, max_arity),
    )


def bounded_arity_fixed_cost_bound(
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
) -> int:
    if type(query_count) is not int or query_count < 0:
        raise ValueError("query_count must be a nonnegative integer")
    if type(adaptive_cost) is not int or adaptive_cost < 0:
        raise ValueError("adaptive_cost must be a nonnegative integer")
    if adaptive_cost == 0:
        return 0
    return min(
        query_count,
        maximum_bounded_arity_tree_internal_nodes(
            world_count, adaptive_cost, max_arity
        ),
    )


def sharp_bounded_arity_unit_cost_ratio(
    world_count: int,
    query_count: int,
    max_arity: int,
) -> Fraction:
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    return max(
        Fraction(
            min(
                query_count,
                maximum_bounded_arity_tree_internal_nodes(
                    world_count, depth, max_arity
                ),
            ),
            depth,
        )
        for depth in range(1, world_count)
    )


def maximizing_bounded_arity_depths(
    world_count: int,
    query_count: int,
    max_arity: int,
) -> tuple[int, ...]:
    optimum = sharp_bounded_arity_unit_cost_ratio(
        world_count, query_count, max_arity
    )
    return tuple(
        depth
        for depth in range(1, world_count)
        if Fraction(
            min(
                query_count,
                maximum_bounded_arity_tree_internal_nodes(
                    world_count, depth, max_arity
                ),
            ),
            depth,
        ) == optimum
    )


@lru_cache(None)
def _maximum_tree(
    world_count: int,
    depth: int,
    max_arity: int,
) -> BoundedArityTree:
    target = maximum_bounded_arity_tree_internal_nodes(
        world_count, depth, max_arity
    )
    if target == 0:
        return BoundedArityTree()

    best_tree: BoundedArityTree | None = None
    best_score = -1
    for child_count in range(2, min(max_arity, world_count) + 1):
        # Store one maximizing child-tuple for every exact allocated budget.
        dp: dict[tuple[int, int], tuple[int, tuple[BoundedArityTree, ...]]] = {
            (0, 0): (0, ())
        }
        for used_children in range(child_count):
            nxt: dict[tuple[int, int], tuple[int, tuple[BoundedArityTree, ...]]] = {}
            remaining_children = child_count - used_children - 1
            for (_, used_budget), (score, trees) in dp.items():
                max_budget = world_count - used_budget - remaining_children
                for child_budget in range(1, max_budget + 1):
                    child = _maximum_tree(child_budget, depth - 1, max_arity)
                    value = score + _internal_count(child)
                    key = (used_children + 1, used_budget + child_budget)
                    old = nxt.get(key)
                    if old is None or value > old[0]:
                        nxt[key] = (value, trees + (child,))
            dp = nxt
        for (used, budget), (score, trees) in dp.items():
            if used != child_count or budget > world_count:
                continue
            value = 1 + score
            if value > best_score:
                best_score = value
                best_tree = BoundedArityTree(trees)
    if best_tree is None or best_score != target:
        raise ArithmeticError("bounded-arity maximizing-tree reconstruction failed")
    return best_tree


def _internal_count(tree: BoundedArityTree) -> int:
    return 0 if tree.is_leaf else 1 + sum(_internal_count(c) for c in tree.children)


def _leaf_count(tree: BoundedArityTree) -> int:
    return 1 if tree.is_leaf else sum(_leaf_count(c) for c in tree.children)


def _height(tree: BoundedArityTree) -> int:
    return 0 if tree.is_leaf else 1 + max(_height(c) for c in tree.children)


def _deepest_internal_depth(tree: BoundedArityTree) -> int:
    best = -1
    def walk(node: BoundedArityTree, depth: int) -> None:
        nonlocal best
        if node.is_leaf:
            return
        best = max(best, depth)
        for child in node.children:
            walk(child, depth + 1)
    walk(tree, 0)
    return best


def _prune_one_deepest(tree: BoundedArityTree) -> BoundedArityTree:
    target_depth = _deepest_internal_depth(tree)
    if target_depth < 0:
        return tree
    replaced = False
    def walk(node: BoundedArityTree, depth: int) -> BoundedArityTree:
        nonlocal replaced
        if replaced or node.is_leaf:
            return node
        if depth == target_depth:
            replaced = True
            return BoundedArityTree()
        return BoundedArityTree(tuple(walk(c, depth + 1) for c in node.children))
    result = walk(tree, 0)
    if not replaced:
        raise ArithmeticError("failed to prune deepest internal node")
    return result


def _prune_to_internal_count(
    tree: BoundedArityTree,
    target_internal_count: int,
) -> BoundedArityTree:
    if target_internal_count < 0 or target_internal_count > _internal_count(tree):
        raise ValueError("target_internal_count outside feasible range")
    result = tree
    while _internal_count(result) > target_internal_count:
        result = _prune_one_deepest(result)
    return result


def _tree_task(tree: BoundedArityTree, world_count: int, query_count: int) -> tuple[FiniteTask, int]:
    if tree.is_leaf:
        raise ValueError("tree task requires at least one internal node")
    node_rows: list[tuple[tuple[tuple[int, ...], ...], tuple[int, int]] | None] = []
    leaf_counter = 0

    def walk(node: BoundedArityTree) -> tuple[tuple[int, ...], int]:
        nonlocal leaf_counter
        if node.is_leaf:
            leaf = leaf_counter
            leaf_counter += 1
            return (leaf,), leaf
        node_index = len(node_rows)
        node_rows.append(None)
        child_rows = [walk(child) for child in node.children]
        child_leaf_sets = tuple(row[0] for row in child_rows)
        representatives = tuple(row[1] for row in child_rows)
        node_rows[node_index] = (
            child_leaf_sets,
            (representatives[0], representatives[1]),
        )
        leaves = tuple(leaf for child_leaves in child_leaf_sets for leaf in child_leaves)
        return leaves, representatives[0]

    all_leaves, _ = walk(tree)
    base_leaf_count = len(all_leaves)
    if base_leaf_count > world_count:
        raise ArithmeticError("constructed tree exceeded declared world budget")

    adjacency = [[] for _ in range(base_leaf_count)]
    private_pairs: list[tuple[int, int]] = []
    for row in node_rows:
        assert row is not None
        _, pair = row
        a, b = pair
        adjacency[a].append(b)
        adjacency[b].append(a)
        private_pairs.append(pair)

    targets: list[int | None] = [None] * base_leaf_count
    for start in range(base_leaf_count):
        if targets[start] is not None:
            continue
        targets[start] = 0
        stack = [start]
        while stack:
            current = stack.pop()
            for other in adjacency[current]:
                wanted = 1 - int(targets[current])
                if targets[other] is None:
                    targets[other] = wanted
                    stack.append(other)
                elif targets[other] != wanted:
                    raise ArithmeticError("private-pair graph was not bipartite")

    worlds = [World(f"leaf_{i}", int(targets[i])) for i in range(base_leaf_count)]
    query_outcomes: list[list[int]] = []
    for row in node_rows:
        assert row is not None
        child_leaf_sets, _ = row
        outcomes = [0] * base_leaf_count
        for child_index, leaves in enumerate(child_leaf_sets):
            for leaf in leaves:
                outcomes[leaf] = child_index
        query_outcomes.append(outcomes)

    # Duplicate an existing leaf exactly to reach the requested world count.
    while len(worlds) < world_count:
        source = 0
        worlds.append(World(f"pad_world_{len(worlds)}", worlds[source].target))
        for outcomes in query_outcomes:
            outcomes.append(outcomes[source])

    queries = [
        Query(f"tree_query_{i}", 1, tuple(outcomes))
        for i, outcomes in enumerate(query_outcomes)
    ]
    while len(queries) < query_count:
        queries.append(Query(f"pad_query_{len(queries)}", 1, tuple(0 for _ in worlds)))
    if len(queries) != query_count:
        raise ArithmeticError("tree witness exceeded declared query count")

    task = FiniteTask(tuple(worlds), tuple(queries))

    # Independent private-pair audit: internal query i must be the unique
    # separator of its registered opposite-target pair.
    for q_index, (a, b) in enumerate(private_pairs):
        if task.worlds[a].target == task.worlds[b].target:
            raise ArithmeticError("private pair did not cross target labels")
        separating = [
            j for j, query in enumerate(task.queries)
            if query.outcomes[a] != query.outcomes[b]
        ]
        if separating != [q_index]:
            raise ArithmeticError("tree query lost unique private-pair necessity")
    return task, len(private_pairs)


def sharp_bounded_arity_unit_cost_witness(
    world_count: int,
    query_count: int,
    max_arity: int,
) -> FiniteTask:
    if query_count > 20:
        raise ValueError("FiniteTask witness is limited by the exact solver's 20-query cap")
    depths = maximizing_bounded_arity_depths(world_count, query_count, max_arity)
    depth = depths[0]
    maximum = maximum_bounded_arity_tree_internal_nodes(world_count, depth, max_arity)
    internal_target = min(query_count, maximum)
    tree = _prune_to_internal_count(
        _maximum_tree(world_count, depth, max_arity),
        internal_target,
    )
    task, private_count = _tree_task(tree, world_count, query_count)
    if private_count != internal_target:
        raise ArithmeticError("bounded-arity witness private-pair count mismatch")
    if any(len(set(query.outcomes)) > max_arity for query in task.queries):
        raise ArithmeticError("bounded-arity witness exceeded declared query arity")
    return task


def sharp_bounded_arity_unit_cost_ratio_receipt(
    world_count: int,
    query_count: int,
    max_arity: int,
    *,
    direct_check: bool = True,
) -> BoundedArityRatioReceipt:
    ratio = sharp_bounded_arity_unit_cost_ratio(world_count, query_count, max_arity)
    depths = maximizing_bounded_arity_depths(world_count, query_count, max_arity)
    direct_ca = direct_cf = None
    private_count = min(
        query_count,
        maximum_bounded_arity_tree_internal_nodes(world_count, depths[0], max_arity),
    )
    agrees = True
    if direct_check:
        task = sharp_bounded_arity_unit_cost_witness(
            world_count, query_count, max_arity
        )
        direct_ca = adaptive_minimum_resolution(task).minimum_worst_path_cost
        direct_cf = fixed_minimum_resolution(task).minimum_cost
        if direct_ca in (None, 0) or direct_cf is None:
            agrees = False
        else:
            agrees = Fraction(direct_cf, direct_ca) == ratio
        if not agrees:
            raise ArithmeticError("bounded-arity sharp witness disagreed with theorem ratio")
    return BoundedArityRatioReceipt(
        world_count,
        query_count,
        max_arity,
        ratio,
        depths,
        direct_ca,
        direct_cf,
        Fraction(direct_cf, direct_ca) if direct_ca not in (None, 0) and direct_cf is not None else None,
        direct_check,
        agrees,
        private_count,
        agrees,
    )
