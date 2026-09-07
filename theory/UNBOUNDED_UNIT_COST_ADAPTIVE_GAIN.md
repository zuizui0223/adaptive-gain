# Unbounded unit-cost adaptive gain from branch-exclusive terminal resources

The finite deterministic theory admits explicit unit-cost families with
arbitrarily large fixed/adaptive cost ratio.  This is true even when **every query
has binary outcomes**.

## 1. Constant-depth family with one multi-valued router

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

So `q_i` differs on `(a_i,b_i)` and is constant on every other branch pair.  The
terminal code vectors form a chain

\[
\operatorname{code}(a_{i+1})=\operatorname{code}(b_i),
\]

so adjacent cross-target worlds `a_{i+1}` and `b_i` agree under every terminal
query and are separated only by the router.

### Exact costs

Measure the router and then the branch-specific terminal:

\[
\boxed{C_A=2}.
\]

Every terminal `q_i` is fixed-mandatory because `(a_i,b_i)` has no other
separator, and the router is fixed-mandatory because `(a_{i+1},b_i)` has no
terminal separator.  Therefore

\[
\boxed{C_F=k+1}.
\]

The productive frontier is exactly the singleton antichain

\[
\{\text{router}\},\{q_0\},\ldots,\{q_{k-1}\}.
\]

Hence

\[
\boxed{C_F-C_A=k-1},
\qquad
\boxed{\frac{C_F}{C_A}=\frac{k+1}{2}}.
\]

Both additive gain and ratio are unbounded.  There is no internal or external
fixed bypass: the selected adaptive policy union has cost `k+1=C_F`.

The `k=2` member is the same structural mechanism as the registered four-world
minimal strict-gain core, up to labels.

## 2. Binary-outcome family

The unbounded ratio does not rely on a growing-arity router.

Fix routing depth `d >= 1` and set

\[
k=2^d.
\]

Again create mixed pairs `(a_i,b_i)`, `i=0,...,k-1`, with targets 0 and 1.
There are

- `d` unit-cost **binary routing queries**, each returning one bit of branch index
  `i` on both `a_i` and `b_i`; and
- `k` unit-cost **binary terminal queries** `t_i`, where `t_i=1` only on `b_i`.

All observations are binary.

### Fixed optimum

For pair `(a_i,b_i)`, every routing bit is equal and every terminal except `t_i`
is zero on both worlds.  Thus `t_i` is the unique separator of that pair.
Every fixed resolver must therefore contain all `k` terminals.  The complete
terminal set resolves all cross-target pairs, so

\[
\boxed{C_F=2^d}.
\]

### Adaptive optimum

The obvious policy reads all `d` routing bits, identifies branch `i`, and then
measures `t_i`, giving

\[
C_A\le d+1.
\]

For the matching lower bound, consider the path realized by any target-0 world
`a_i`.  Every terminal outcome on that path is zero.  If only `r` independent
routing bits have been measured, then at least

\[
2^{d-r}
\]

branch indices remain compatible.  Their target-1 worlds cannot be removed by
other terminals: each compatible `b_j` requires its own `t_j`.  Therefore every
such target-0 path has cost at least

\[
r+2^{d-r}.
\]

For integers `0<=r<=d`,

\[
\min_r\{r+2^{d-r}\}=d+1.
\]

Hence

\[
\boxed{C_A=d+1}.
\]

Therefore

\[
\boxed{
\frac{C_F}{C_A}
=
\frac{2^d}{d+1}
\longrightarrow\infty.
}
\]

So the multiplicative adaptive advantage is unbounded even under the joint
restrictions

```text
finite represented worlds
binary deterministic observations
unit acquisition costs
exact guaranteed target resolution
```

Small depths are checked directly by the exact solvers.  Larger depths use the
closed-form lower bound rather than pretending that exhaustive optimization of
an exponentially growing instance is cheap.

## 3. First unit-cost scope above 3/2

The multi-valued `k=3` member uses

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

If `C_A=1`, the same query is a fixed resolver and the ratio is 1.

If `C_A=2`, an optimal policy has one root plus at most one second query for each
target-mixed root outcome.  Mixed root outcomes are disjoint and contain at least
two worlds, so with `n` worlds there are at most `floor(n/2)` such branches.
Flattening the policy gives

\[
C_F\le1+\lfloor n/2\rfloor.
\]

For `n<=5`, this implies `C_F/C_A<=3/2`.

If `C_A>=3`, a productive resolution tree on `n` represented worlds has at most
`n-1` internal nodes, hence its query union has unit cost at most `n-1`.  Thus for
`n<=5`,

\[
\frac{C_F}{C_A}\le\frac{n-1}{3}\le\frac43.
\]

So at least six represented worlds are necessary.  Any ratio above `3/2` also
requires integer `C_F>=4`, hence at least four declared unit-cost queries.  The
six-world construction attains both lower bounds.

This minimality result is explicitly unit-cost.  Unequal positive integer costs
can change the smallest finite scope.

## Implementation

- `adaptive_gain/extremal_routing_family.py`
- `tests/test_extremal_routing_family.py`

Executable regression checks:

- the exact k-ary formula for `k=2,...,8`;
- singleton productive-frontier edges of that family;
- the first unit-cost ratio above `3/2`;
- one-world deletion of the six-world witness;
- direct exact-solver agreement for binary depths `d=1,2,3`; and
- analytic binary-family ratios at larger depths without claiming exhaustive
  solver validation there.
