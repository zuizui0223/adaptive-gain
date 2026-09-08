# Exactly balanced binary queries do not bound adaptive advantage

The binary unit-cost theory already has an unbounded family, but its branch-terminal queries are highly unbalanced. This note shows that even **exact 50/50 balance of every binary query** does not bound the fixed/adaptive ratio.

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

and add two dummy worlds `z_0,z_1`, both with target 0. Thus

\[
\boxed{n=2k+2}.
\]

All query costs are one and all query outcomes are binary.

## Routing queries

Use `d` routing-bit queries. On both `a_i` and `b_i`, routing bit `r` reports bit `r` of branch index `i`.

On the original `2k` worlds each routing query has exactly `k` zeros and `k` ones. Give `z_0` outcome zero and `z_1` outcome one on every routing query. Therefore every routing query has exactly

\[
\boxed{k+1\text{ zeros and }k+1\text{ ones}.}
\]

The two dummy routing vectors place `z_0` in branch 0 and `z_1` in branch `k-1`.

## Terminal queries

For each branch `j`, terminal `t_j` has

\[
t_j(a_j)=0,
\qquad
t_j(b_j)=1.
\]

Choose exactly `k/2` other branch indices and assign outcome one to **both** worlds in each of those pairs. Assign zero to both worlds in every remaining pair and zero to both dummy worlds.

The implementation chooses the next `k/2` cyclic branch indices, which never includes `j`.

On the original `2k` worlds, `t_j` therefore has

\[
k+1\text{ ones},
\qquad
k-1\text{ zeros}.
\]

The two zero-valued dummies raise the zero count to `k+1`, so every terminal also has exactly

\[
\boxed{k+1\text{ zeros and }k+1\text{ ones}.}
\]

Hence every declared query satisfies the stronger exact balance condition

\[
\boxed{\#0=\#1.}
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

The theorem only needs this lower bound. If a particular finite member also requires routing resources in an optimal fixed resolver, that only strengthens the ratio lower bound.

## Adaptive upper bound

Measure the `d` routing bits. They identify branch `i`. Then measure `t_i`.

For ordinary branches the compatible state is exactly `{a_i,b_i}`. Branch 0 additionally contains `z_0`, and branch `k-1` additionally contains `z_1`. Both dummies have target 0 and terminal outcome zero, exactly like `a_i`, while `b_i` has terminal outcome one. Thus the branch terminal still resolves the target.

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
every query exactly 50/50 balanced on represented worlds
guaranteed exact target resolution
```

## Interpretation

Global marginal balance is not the structural quantity controlling adaptive gain.

The terminal queries are exactly balanced binary measurements at the whole-task level, yet each contains a **private target-mixed pair obligation**. Fixed resolution must buy all those branch-specific resources simultaneously. Adaptivity first learns which branch is relevant and then buys only that branch's terminal resource.

Thus even perfect global balance does not remove branch-exclusive resource geometry.

A constraint capable of bounding worst-case adaptive advantage must control something stronger, such as branch/resource incidence, productive-frontier geometry, or the way target-mixed pairs are distributed across queries.

## Validation

Implementation:

- `adaptive_gain/balanced_binary_extremal_family.py`
- `tests/test_balanced_binary_extremal_family.py`

For depths `d=1,2,3`, the general exact solvers verify the adaptive upper bound and fixed lower bound directly. Separate checks verify that every query is binary and has exactly equal zero/one counts, and that every terminal is the unique separator of its branch pair. Larger depths use only the closed-form construction/counting argument and do not pretend to be exhaustively solved beyond the repository's 20-query cap.

## Claim boundary

This does **not** give the sharp maximum ratio at fixed `(n,m)` when every binary query is balanced. It proves only that exact global balance by itself does not make the ratio uniformly bounded as problem size grows.
