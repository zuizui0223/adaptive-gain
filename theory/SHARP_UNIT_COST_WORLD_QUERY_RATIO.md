# Sharp unit-cost ratio at fixed world and query counts

This note gives an exact extremal result for the finite deterministic guaranteed-
resolution model when every declared query has unit acquisition cost and query
arity is otherwise unrestricted.

Let

- `n >= 2` be the number of represented worlds;
- `m >= 1` be the number of declared query resources;
- `C_A > 0` be the optimal adaptive worst-path cost; and
- `C_F` be the optimal fixed resolving-bundle cost.

The exact maximum ratio at fixed `(n,m)` is

\[
\boxed{
\sup \frac{C_F}{C_A}
=
\max\!\left(
1,
\frac{\min\{m,\,1+\lfloor n/2\rfloor\}}{2}
\right).
}
\]

The supremum is attained by an explicit finite task, so it is a maximum.

## 1. Exact productive-tree union bound

Consider any productive rooted decision tree with at most `n` nonempty leaves and
worst-path depth at most `h`.  Every internal node has at least two nonempty
children.  Let `I` be the number of internal-node occurrences.

Then

\[
\boxed{
I\le M(n,h)
:=
n+1-
\max\!\left(
2,
\left\lceil\frac{n}{2^{h-1}}\right\rceil
\right)
}
\]

for `h >= 1`, with `M(n,0)=0`.

This bound is sharp as a statement about productive rooted trees.

### Proof by induction

Write

\[
D_h(n):=n-M(n,h)
=
\max\!\left(
1,
\left\lceil\frac{n}{2^{h-1}}\right\rceil-1
\right).
\]

For `h=1`, any productive tree is one root with at least two leaves, so `I=1`
and the formula is immediate.

For `h>=2`, partition the root's leaves among its child subtrees.  If a child
contains `x` leaves, induction gives at most `x-D_{h-1}(x)` internal nodes below
that child.  Hence maximizing total internal nodes is equivalent to minimizing

\[
\sum_j D_{h-1}(x_j)
\]

over partitions of `n` into at least two positive child leaf counts.

Set `B=2^{h-2}`.  From

\[
D_{h-1}(x)=\max\{1,\lceil x/B\rceil-1\}
\]

one has

\[
x\le 2B\,D_{h-1}(x)=2^{h-1}D_{h-1}(x).
\]

Therefore every such partition obeys

\[
\sum_jD_{h-1}(x_j)
\ge
\left\lceil\frac{n}{2^{h-1}}\right\rceil.
\]

There are at least two children and every `D` is at least one, so the sum is at
least

\[
A:=\max\!\left(2,\left\lceil\frac{n}{2^{h-1}}\right\rceil\right).
\]

Conversely, split `n` into exactly `A` positive parts, each at most `2^{h-1}`.
That is possible by the definition of `A`.  Every part then has
`D_{h-1}(x_j)=1`, so the lower bound `A` is attained.  Substituting back gives

\[
I=n+1-A=M(n,h).
\]

QED.

## 2. Consequence for a unit-cost adaptive policy

Take a selected optimal adaptive tree.  Under unit costs its worst-path depth is
exactly `h=C_A`.

The distinct query union `S` used anywhere in the tree has

\[
|S|\le I\le M(n,C_A).
\]

Flattening `S` is a valid fixed resolver, while no fixed bundle uses more than the
`m` declared resources.  Thus

\[
\boxed{
C_F\le \min\{m,M(n,C_A)\}.
}
\]

This strengthens the coarse `C_F<=n-1` tree-union bound whenever the adaptive
depth is small relative to `n`.

## 3. Sharp world-count ratio bound

For `C_A=1`, the selected single query is itself a fixed resolver, so `C_F=1`.

Assume `C_A=h>=2`.

### Depth two

The tree formula gives

\[
M(n,2)=1+\lfloor n/2\rfloor,
\]

hence

\[
\frac{C_F}{C_A}
\le
\frac{1+\lfloor n/2\rfloor}{2}.
\]

### Depth three

Here

\[
M(n,3)=n+1-\max(2,\lceil n/4\rceil).
\]

A direct check of `n mod 4` gives

\[
2M(n,3)\le 3(1+\lfloor n/2\rfloor),
\]

so the same ratio bound holds.

### Depth at least four

Since every productive tree has at most `n-1` internal nodes,

\[
\frac{C_F}{C_A}
\le
\frac{n-1}{4}
\le
\frac{1+\lfloor n/2\rfloor}{2}.
\]

Therefore every nontrivial unit-cost task satisfies

\[
\boxed{
\frac{C_F}{C_A}
\le
\frac{1+\lfloor n/2\rfloor}{2}.
}
\]

## 4. Add the declared-query bound

Trivially `C_F<=m`.  For every strict task `C_A>=2`, so

\[
\frac{C_F}{C_A}\le\frac{m}{2}.
\]

Combining this with the world-count theorem, and retaining the ratio-one direct-
query case, yields

\[
\boxed{
\frac{C_F}{C_A}
\le
\max\!\left(
1,
\frac{\min\{m,1+\lfloor n/2\rfloor\}}{2}
\right).
}
\]

## 5. Attainment

Let

\[
s:=\min\{m,1+\lfloor n/2\rfloor\}.
\]

If `s<=2`, one direct unit-cost target query attains ratio one.

If `s>=3`, set `k=s-1`.  The registered depth-two `k`-branch extremal routing
family uses `2k<=n` worlds and `k+1=s<=m` queries and has

\[
C_A=2,\qquad C_F=s.
\]

Duplicate one existing represented world, with the same target and all the same
query outcomes, until exactly `n` worlds are present.  Add constant unused
unit-cost queries until exactly `m` resources are declared.  Neither operation
changes either optimum.

Thus the bound is attained exactly:

\[
\boxed{
\max_{|W|=n,|Q|=m}\frac{C_F}{C_A}
=
\max\!\left(
1,
\frac{\min\{m,1+\lfloor n/2\rfloor\}}{2}
\right).
}
\]

## 6. Consequences

- The earlier six-world / four-query `(C_A,C_F)=(2,4)` witness is now an immediate
  corollary: it is the first `(n,m)` with sharp ratio greater than `3/2`.
- At fixed `n`, increasing query vocabulary beyond `1+floor(n/2)` cannot increase
  the unit-cost extremal ratio.
- At fixed `m>=3`, the maximum ratio saturates at `m/2` once
  `n>=2(m-1)`.
- Depth two is globally extremal for the unrestricted-arity fixed-world-count
  problem.
- This theorem does **not** solve the binary-outcome extremum.  The binary-only
  family in `UNBOUNDED_UNIT_COST_ADAPTIVE_GAIN.md` proves unbounded growth when
  `n,m` grow, but fixed `(n,m)` sharpness under binary arity remains separate.

## Implementation

- `adaptive_gain/unit_cost_extremal_bounds.py`
- `tests/test_unit_cost_extremal_bounds.py`

The tree formula is checked against an independent dynamic recurrence for small
`n,h`.  The attainment construction is checked by the general exact adaptive and
fixed solvers on a grid of small `(n,m)` values.
