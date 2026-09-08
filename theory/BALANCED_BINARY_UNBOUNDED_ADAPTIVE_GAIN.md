# Balanced binary queries do not bound adaptive advantage

The binary unit-cost theory already has an unbounded family, but its branch-terminal queries are highly unbalanced. This note shows that **global balance of every binary query still does not bound** the fixed/adaptive ratio.

The result is an existence lower bound, not a sharp fixed-`(n,m)` theorem under balancedness.

## Construction

Fix routing depth

\[
d\ge1,
\qquad
k=2^d.
\]

Create `k` target-mixed pairs

\[
(a_i,b_i),\qquad i=0,\ldots,k-1,
\]

with

\[
T(a_i)=0,
\qquad
T(b_i)=1,
\]

and add one extra dummy world `z` with target 0. Thus

\[
n=2k+1.
\]

All query costs are one and all query outcomes are binary.

## Routing queries

Use `d` routing-bit queries. On both `a_i` and `b_i`, routing bit `r` reports bit `r` of branch index `i`. The dummy world reports zero on every routing query.

On the original `2k` worlds each routing query has exactly `k` zeros and `k` ones. Adding the dummy gives counts

\[
k+1\quad\text{and}\quad k,
\]

so every routing query is balanced to within one observation.

## Terminal queries

For each branch `j`, terminal `t_j` has

\[
t_j(a_j)=0,
\qquad
t_j(b_j)=1.
\]

Choose exactly `k/2` other branch indices and assign outcome one to **both** worlds in each of those pairs. Assign zero to both worlds in every remaining pair and zero to the dummy.

The implementation chooses the next `k/2` cyclic branch indices, which never includes `j`.

Therefore the number of ones is

\[
1+2(k/2)=k+1,
\]

and the number of zeros is `k`. Every terminal query is globally balanced as well.

Hence every declared query satisfies

\[
\boxed{
|\#0-\#1|\le1.
}
\]

## Fixed lower bound

For the target-mixed pair `(a_j,b_j)`:

- every routing query is equal on the two worlds;
- every terminal `t_i`, `i\ne j`, assigns the same value to both worlds of branch `j`;
- only `t_j` separates the pair.

Thus `t_j` is fixed-mandatory. This holds for every `j`, so

\[
\boxed{C_F\ge k=2^d}.
\]

The theorem only needs this lower bound. Some constructions may require additional routing resources in an optimal fixed resolver; that can only increase the ratio.

## Adaptive upper bound

Measure the `d` routing bits. They identify branch `i`. Then measure `t_i`.

For every nonzero branch the compatible state is exactly `{a_i,b_i}`. For branch zero the dummy also remains, but it shares target 0 and terminal outcome zero with `a_0`, while `b_0` has outcome one. Thus `t_0` resolves that branch as well.

Therefore

\[
\boxed{C_A\le d+1}.
\]

Combining bounds,

\[
\boxed{
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\longrightarrow\infty.
}
\]

So the adaptive advantage remains unbounded under all of the simultaneous restrictions

```text
finite represented worlds
binary deterministic queries
unit acquisition costs
globally balanced query outcomes: |#0-#1| <= 1
guaranteed exact target resolution
```

## Interpretation

Global marginal balance is not the structural quantity controlling adaptive gain.

The terminal queries are perfectly ordinary balanced binary measurements at the whole-task level, yet each contains a **private target-mixed pair obligation**. Fixed resolution must buy all those branch-specific resources simultaneously. Adaptivity first learns which branch is relevant and then buys only that branch's terminal resource.

Thus balancing a query's marginal outcome counts does not remove branch-exclusive resource geometry.

A constraint capable of bounding worst-case adaptive advantage must control something stronger, such as branch/resource incidence, productive-frontier geometry, or the way target-mixed pairs are distributed across queries.

## Validation

Implementation:

- `adaptive_gain/balanced_binary_extremal_family.py`
- `tests/test_balanced_binary_extremal_family.py`

For depths `d=1,2,3`, the general exact solvers verify the adaptive upper bound and fixed lower bound directly, while separate checks verify every query is binary/balanced and every terminal is the unique separator of its branch pair. Larger depths use only the closed-form construction/counting argument and do not pretend to be exhaustively solved beyond the repository's 20-query cap.

## Claim boundary

This does **not** give the sharp maximum ratio at fixed `(n,m)` when every binary query is balanced. It only proves that balancedness by itself does not make the ratio uniformly bounded as problem size grows.
