# Unbounded unit-cost adaptive gain from branch-exclusive terminal resources

The finite deterministic theory admits an explicit unit-cost family with
arbitrarily large fixed/adaptive cost ratio.

## Construction

Fix an integer `k >= 2`.  Create `2k` represented worlds

\[
a_0,b_0,\ldots,a_{k-1},b_{k-1}
\]

with

\[
T(a_i)=0,\qquad T(b_i)=1.
\]

There are `k+1` unit-cost queries.

### Router

One `k`-ary router returns branch index `i` on both `a_i` and `b_i`.  Thus the
router is target-blind inside each branch.

### Terminal queries

For each branch `i`, terminal query `q_i` has binary outcomes

\[
q_i(a_j)=\mathbf 1[i<j],\qquad
q_i(b_j)=\mathbf 1[i\le j].
\]

So `q_i` differs on the target-mixed pair `(a_i,b_i)` and is constant on every
other branch pair.

The terminal code vectors form a chain:

\[
\operatorname{code}(a_{i+1})=\operatorname{code}(b_i).
\]

Therefore adjacent cross-target worlds `a_{i+1}` and `b_i` agree under every
terminal query and are separated only by the router.

## Adaptive optimum

Measure the router first.  Outcome `i` leaves exactly the mixed pair
`{a_i,b_i}`.  Then measure `q_i`.

Hence

\[
C_A\le2.
\]

No single query resolves every branch: the router never separates `(a_i,b_i)`,
and each terminal query is constant on some other mixed branch.  Therefore

\[
\boxed{C_A=2}.
\]

## Fixed optimum

For every `i`, pair `(a_i,b_i)` is separated by `q_i` and by no other declared
query, so every fixed resolving bundle must contain all `k` terminal queries.

For every `i<k-1`, pair `(a_{i+1},b_i)` has identical outcomes under every
terminal query and different router outcomes, so the router is also mandatory.

Thus

\[
\boxed{C_F=k+1}.
\]

All queries together obviously resolve, so the lower bound is attained.

The productive-frontier hypergraph makes the same fact especially transparent:
its inclusion-minimal edges are exactly the `k+1` singletons

\[
\{\text{router}\},\{q_0\},\ldots,\{q_{k-1}\}.
\]

## Consequences

Therefore

\[
\boxed{C_F-C_A=k-1}
\]

and

\[
\boxed{\frac{C_F}{C_A}=\frac{k+1}{2}}.
\]

Both additive gain and multiplicative ratio are unbounded as `k -> infinity`.
The selected router-first policy has union cost `k+1`, equal to `C_F`, so this
family has no internal or external fixed bypass: all branch-exclusive overhead is
realized as adaptive gain.

The `k=2` member has `(C_A,C_F)=(2,3)` and is the same structural mechanism as the
registered four-world minimal strict-gain core, up to labels.

## First unit-cost scope above 3/2

The `k=3` member uses

```text
6 worlds
4 unit-cost queries
```

and has

\[
(C_A,C_F)=(2,4),\qquad C_F/C_A=2.
\]

This is componentwise minimal in represented worlds and query count for a
**unit-cost** finite deterministic task with ratio strictly above `3/2`.

### Why five worlds cannot exceed 3/2

If `C_A=1`, the same single query is a fixed resolver and the ratio is 1.

If `C_A=2`, an optimal policy consists of one root query plus at most one second
query for each target-mixed root outcome.  Mixed root outcomes are disjoint and
each contains at least two represented worlds, so with `n` worlds there are at
most `floor(n/2)` such branches.  Flattening the tree therefore gives

\[
C_F\le1+\lfloor n/2\rfloor.
\]

For `n<=5`, this gives `C_F/C_A <= 3/2`.

If `C_A>=3`, a productive decision tree on `n` represented worlds has at most
`n-1` internal nodes, hence its query union has cost at most `n-1` under unit
costs.  Therefore for `n<=5`,

\[
\frac{C_F}{C_A}\le\frac{n-1}{3}\le\frac43.
\]

So at least six represented worlds are necessary.

Also any ratio above `3/2` has integer `C_A>=2` and therefore integer `C_F>=4`;
a unit-cost fixed bundle of cost at least four requires at least four declared
queries.  The `k=3` construction attains both lower bounds simultaneously.

This minimality statement is deliberately restricted to unit-cost queries.
Unequal positive integer costs can change the smallest world/query scope.

## Implementation

- `adaptive_gain/extremal_routing_family.py`
- `tests/test_extremal_routing_family.py`

The executable audit checks the exact formula for `k=2,...,8`, the first
`>3/2` scope, singleton productive-frontier edges, and loss of the `>3/2` ratio
after any one-world deletion of the six-world witness.
