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



def _orient_deepest_first(tree: BoundedArityTree) -> BoundedArityTree:
    """Recursively place one deepest child first at every internal node.

    This exposes a child-0 spine whose length equals the tree height.  The
    private-pair construction then makes the leftmost leaf an endpoint of one
    unique opposite-target pair for every query on that spine, certifying the
    adaptive lower bound by a single realized world.
    """
    if tree.is_leaf:
        return tree
    oriented_children = tuple(_orient_deepest_first(c) for c in tree.children)
    ordered = tuple(
        sorted(
            oriented_children,
            key=lambda child: (-_height(child), repr(child)),
        )
    )
    return BoundedArityTree(ordered)


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



def _prune_one_deepest_off_spine(tree: BoundedArityTree) -> BoundedArityTree:
    """Prune one deepest internal node while protecting a child-0 deepest spine."""
    oriented = _orient_deepest_first(tree)
    target_depth = -1
    target_path: tuple[int, ...] | None = None

    def scan(
        node: BoundedArityTree,
        depth: int,
        path: tuple[int, ...],
        on_spine: bool,
    ) -> None:
        nonlocal target_depth, target_path
        if node.is_leaf:
            return
        if not on_spine and depth > target_depth:
            target_depth = depth
            target_path = path
        for index, child in enumerate(node.children):
            scan(
                child,
                depth + 1,
                path + (index,),
                on_spine and index == 0,
            )

    scan(oriented, 0, (), True)
    if target_path is None:
        return oriented

    def replace(
        node: BoundedArityTree,
        path: tuple[int, ...],
    ) -> BoundedArityTree:
        if not path:
            return BoundedArityTree()
        index = path[0]
        children = list(node.children)
        children[index] = replace(children[index], path[1:])
        return BoundedArityTree(tuple(children))

    return _orient_deepest_first(replace(oriented, target_path))


def _prune_to_internal_count_preserving_height(
    tree: BoundedArityTree,
    target_internal_count: int,
    target_height: int,
) -> BoundedArityTree:
    """Reduce internal-node count without shortening one deepest spine."""
    if target_internal_count < target_height:
        raise ValueError("target_internal_count cannot be below target_height")
    result = _orient_deepest_first(tree)
    if _height(result) != target_height:
        raise ValueError("input tree does not have the declared target height")

    while _internal_count(result) > target_internal_count:
        before = _internal_count(result)
        result = _prune_one_deepest_off_spine(result)
        after = _internal_count(result)
        if after >= before:
            raise ArithmeticError("no off-spine internal node remained to prune")
        if _height(result) != target_height:
            raise ArithmeticError("protected-spine pruning shortened the tree")

    if _internal_count(result) != target_internal_count:
        raise ArithmeticError("protected-spine pruning missed target internal count")
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



def bounded_arity_unit_cost_witness_at_depth(
    world_count: int,
    query_count: int,
    max_arity: int,
    adaptive_depth: int,
) -> FiniteTask:
    """Construct the private-pair witness at one declared feasible depth.

    The declared depth must be no larger than both the world and query budgets.
    The construction uses I=min(m,F_b(n,h)) internal queries and pads any
    remaining declared queries with constants.
    """
    if query_count > 20:
        raise ValueError("FiniteTask witness is limited by the exact solver's 20-query cap")
    if type(adaptive_depth) is not int or adaptive_depth < 1:
        raise ValueError("adaptive_depth must be a positive integer")
    if adaptive_depth > world_count - 1:
        raise ValueError("adaptive_depth exceeds the nontrivial world-depth bound")
    if adaptive_depth > query_count:
        raise ValueError("adaptive_depth exceeds the declared query budget")

    maximum = maximum_bounded_arity_tree_internal_nodes(
        world_count, adaptive_depth, max_arity
    )
    internal_target = min(query_count, maximum)
    if internal_target < adaptive_depth:
        raise ValueError("declared depth cannot be preserved by the available queries")

    tree = _prune_to_internal_count_preserving_height(
        _maximum_tree(world_count, adaptive_depth, max_arity),
        internal_target,
        adaptive_depth,
    )
    if _height(tree) != adaptive_depth:
        raise ArithmeticError("depth-preserving bounded-arity pruning failed")

    task, private_count = _tree_task(tree, world_count, query_count)
    if private_count != internal_target:
        raise ArithmeticError("bounded-arity depth witness private-pair count mismatch")
    if any(len(set(query.outcomes)) > max_arity for query in task.queries):
        raise ArithmeticError("bounded-arity depth witness exceeded declared query arity")
    return task



def shallow_leaf_expected_value_witness(
    rare_depth: int,
    max_arity: int = 2,
) -> FiniteTask:
    """Construct one depth-1 leaf plus a full rare-state routing subtree.

    The root has two nonempty children: one single shallow leaf and one full
    max_arity-ary subtree of height rare_depth. Applying the private-pair
    target construction makes every internal query fixed-mandatory.

    Thus the common leaf completes in one query, rare leaves complete in
    rare_depth + 1 queries, and the fixed resolver costs

        1 + (max_arity**rare_depth - 1)/(max_arity - 1).

    This family witnesses expected-value capacity above the robust ceiling.
    """
    if type(rare_depth) is not int or rare_depth < 1:
        raise ValueError("rare_depth must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")

    def full(depth: int) -> BoundedArityTree:
        if depth == 0:
            return BoundedArityTree()
        return BoundedArityTree(
            tuple(full(depth - 1) for _ in range(max_arity))
        )

    tree = BoundedArityTree(
        (
            BoundedArityTree(),
            full(rare_depth),
        )
    )
    world_count = _leaf_count(tree)
    query_count = _internal_count(tree)
    task, private_count = _tree_task(tree, world_count, query_count)
    if private_count != query_count:
        raise ArithmeticError("shallow-leaf witness lost private-pair necessity")
    return task


def two_shallow_leaf_expected_value_witness(
    rare_depth: int,
    max_arity: int = 2,
) -> FiniteTask:
    """Construct depth-1 and depth-2 pure leaves plus a rare deep subtree.

    The root child 0 is a one-query leaf. Root child 1 is an internal node
    whose child 0 is a two-query leaf and whose child 1 contains a full
    max_arity-ary subtree of height rare_depth. The private-pair target
    construction makes all internal queries fixed-mandatory.

    This family witnesses the conditional one-step-mass bound in RF6.
    """
    if type(rare_depth) is not int or rare_depth < 1:
        raise ValueError("rare_depth must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")

    def full(depth: int) -> BoundedArityTree:
        if depth == 0:
            return BoundedArityTree()
        return BoundedArityTree(
            tuple(full(depth - 1) for _ in range(max_arity))
        )

    second = BoundedArityTree(
        (
            BoundedArityTree(),
            full(rare_depth),
        )
    )
    tree = BoundedArityTree(
        (
            BoundedArityTree(),
            second,
        )
    )
    world_count = _leaf_count(tree)
    query_count = _internal_count(tree)
    task, private_count = _tree_task(tree, world_count, query_count)
    if private_count != query_count:
        raise ArithmeticError("two-shallow-leaf witness lost private-pair necessity")
    return task



def ternary_target_balance_expected_witness(
    rare_depth: int,
) -> FiniteTask:
    """A three-outcome root with pure targets 0/1 and a rare mixed branch.

    The first two root outcomes are single-leaf pure targets of opposite type;
    a third root outcome enters a complete binary rare-state subtree.
    Every internal query has its own opposite-target private pair, so the
    fixed resolver acquires exactly 2**rare_depth query resources.

    The two common target types can each finish in one query, while positive
    low-probability rare worlds from both targets preserve fixed necessity.
    """
    if type(rare_depth) is not int or rare_depth < 1:
        raise ValueError("rare_depth must be a positive integer")

    def binary_subtree(depth: int) -> BoundedArityTree:
        if depth == 0:
            return BoundedArityTree()
        return BoundedArityTree((
            binary_subtree(depth - 1),
            binary_subtree(depth - 1),
        ))

    tree = BoundedArityTree((
        BoundedArityTree(),
        BoundedArityTree(),
        binary_subtree(rare_depth),
    ))
    world_count = _leaf_count(tree)
    query_count = _internal_count(tree)
    task, private_count = _tree_task(tree, world_count, query_count)
    if private_count != query_count:
        raise ArithmeticError("target-balance witness lost fixed mandatory queries")
    if task.worlds[0].target == task.worlds[1].target:
        raise ArithmeticError("one-step root outcomes must represent both targets")
    if len({w.target for w in task.worlds[2:]}) != 2:
        raise ArithmeticError("rare subtree must contain both target classes")
    if len(set(task.queries[0].outcomes)) != 3:
        raise ArithmeticError("root did not produce exactly three outcomes")
    if any(len(set(q.outcomes)) > 3 for q in task.queries):
        raise ArithmeticError("witness exceeded ternary cue arity")
    return task


def finite_expected_ceiling_witness(
    world_count: int,
    query_count: int,
) -> FiniteTask:
    """Binary witness for the exact finite-scope expected-value ceiling.

    Let M=min(query_count, world_count-1). For M>=2, construct a binary tree
    with exactly M internal nodes and one target-pure leaf directly below the
    root. Private-pair targets make all M internal queries fixed-mandatory.
    Extra worlds are exact duplicates and extra declared queries are constants.

    The distinguished first leaf is therefore resolvable after one query,
    while C_F=M. This witnesses the supremum U(1)-U(M) as its encounter
    probability tends to one.
    """
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if query_count > 20:
        raise ValueError("FiniteTask witness is limited by the exact solver's 20-query cap")

    internal_target = min(query_count, world_count - 1)
    if internal_target < 2:
        raise ValueError("strict expected adaptive advantage requires at least two fixed queries")

    def chain(internal_count: int) -> BoundedArityTree:
        if internal_count == 0:
            return BoundedArityTree()
        return BoundedArityTree(
            (
                BoundedArityTree(),
                chain(internal_count - 1),
            )
        )

    tree = BoundedArityTree(
        (
            BoundedArityTree(),
            chain(internal_target - 1),
        )
    )
    task, private_count = _tree_task(tree, world_count, query_count)
    if private_count != internal_target:
        raise ArithmeticError("finite expected ceiling witness lost fixed necessity")
    return task


def finite_expected_one_step_mass_witness(
    world_count: int,
    query_count: int,
) -> FiniteTask:
    """Binary witness with one depth-1 leaf, one depth-2 leaf, and rare tail."""
    if type(world_count) is not int or world_count < 3:
        raise ValueError("world_count must be an integer at least 3")
    if type(query_count) is not int or query_count < 2:
        raise ValueError("query_count must be an integer at least 2")
    if query_count > 20:
        raise ValueError("FiniteTask witness is limited by the exact solver's 20-query cap")

    internal_target = min(query_count, world_count - 1)

    def chain(internal_count: int) -> BoundedArityTree:
        if internal_count == 0:
            return BoundedArityTree()
        return BoundedArityTree(
            (
                BoundedArityTree(),
                chain(internal_count - 1),
            )
        )

    second = BoundedArityTree(
        (
            BoundedArityTree(),
            chain(internal_target - 2),
        )
    )
    tree = BoundedArityTree(
        (
            BoundedArityTree(),
            second,
        )
    )
    task, private_count = _tree_task(tree, world_count, query_count)
    if private_count != internal_target:
        raise ArithmeticError("finite one-step-mass witness lost fixed necessity")
    return task

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
