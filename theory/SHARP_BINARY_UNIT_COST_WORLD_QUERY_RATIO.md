# Sharp fixed-`(n,m)` ratio for binary unit-cost observations

This note closes the fixed-world/fixed-query extremal problem when every query has
binary deterministic outcomes and unit acquisition cost.

Let

- `n >= 2` be the represented-world count;
- `m >= 1` be the declared-query count; and
- `K = min(m,n-1)`.

Define

\[
d=\left\lfloor\log_2(K+1)\right\rfloor.
\]

Then

\[
\boxed{
\max\frac{C_F}{C_A}
=
\max\!\left(
1,
\frac{2^d-1}{d},
\frac{K}{d+1}
\right).
}
\]

The maximum is attained by explicit alternating-target threshold tasks.

## 1. Binary tree upper bound

A binary adaptive decision tree of worst-path depth `h` has at most

\[
2^h-1
\]

internal-node occurrences.  Since its nonempty leaves partition represented
worlds, it also has at most `n-1` internal nodes.  Finally its distinct query union
cannot exceed the `m` declared resources.

Therefore flattening an optimal adaptive tree gives

\[
\boxed{
C_F
\le
\min\{m,n-1,2^{C_A}-1\}.
}
\]

For a nontrivial task with `C_A=h`,

\[
\frac{C_F}{C_A}
\le
\frac{\min\{K,2^h-1\}}{h}.
\]

If `C_A=1`, the same query is fixed-resolving and the ratio is one.

## 2. Optimize over adaptive depth

Consider

\[
f(h)=\frac{\min\{K,2^h-1\}}{h}.
\]

For depths satisfying `2^h-1 <= K`,

\[
f(h)=\frac{2^h-1}{h}.
\]

This sequence is nondecreasing because

\[
\frac{2^{h+1}-1}{h+1}
\ge
\frac{2^h-1}{h}
\]

is equivalent to

\[
(h-1)2^h+1\ge0.
\]

Once `2^h-1 >= K`, the numerator is fixed at `K`, so `K/h` decreases with `h`.
Hence only the two depths straddling the saturation point can be optimal:

\[
h=d
\quad\text{or}\quad
h=d+1.
\]

This proves the upper bound

\[
\boxed{
\frac{C_F}{C_A}
\le
\max\!\left(
1,
\frac{2^d-1}{d},
\frac{K}{d+1}
\right).
}
\]

## 3. Threshold-path construction

For an integer `N>=2`, create ordered worlds

\[
w_0,w_1,\ldots,w_{N-1}
\]

with alternating targets

\[
T(w_i)=i\bmod2.
\]

For every boundary `j=0,...,N-2`, declare one binary threshold query

\[
q_j(w_i)=\mathbf 1[i>j].
\]

There are `N-1` unit-cost queries.

### Fixed optimum

Adjacent worlds `w_j,w_{j+1}` have opposite targets.  Their outcomes differ under
`q_j`, while every other threshold gives the same outcome on that adjacent pair.
Thus `q_j` is the unique separator of that pair and is mandatory in every fixed
resolver.

Hence

\[
\boxed{C_F=N-1}.
\]

### Adaptive optimum

After any sequence of threshold outcomes, the compatible world set is an interval
of the ordered path.  Every interval containing at least two worlds contains both
target labels because targets alternate.  Therefore exact target resolution
requires isolating one world.

A binary tree with `N` singleton leaves needs depth at least

\[
\lceil\log_2N\rceil.
\]

Balanced binary search with the threshold queries attains that depth, so

\[
\boxed{C_A=\lceil\log_2N\rceil}.
\]

Thus the threshold path has ratio

\[
\frac{N-1}{\lceil\log_2N\rceil}.
\]

## 4. Attain both candidate depths

Let `K=min(m,n-1)` and `d=floor(log2(K+1))`.

### Candidate 1

Choose

\[
N=2^d.
\]

Then the threshold path uses `2^d-1 <= K` resources and has

\[
\frac{C_F}{C_A}=\frac{2^d-1}{d}.
\]

### Candidate 2

Choose

\[
N=K+1.
\]

If `K+1` is not already a power of two, then

\[
\lceil\log_2(K+1)\rceil=d+1
\]

and

\[
\frac{C_F}{C_A}=\frac{K}{d+1}.
\]

If `K+1` is a power of two, candidate 1 already equals `K/d` and dominates the
second expression.

In either construction, `N<=n` and the number of threshold resources is at most
`m`.  Duplicate an existing world with identical target/outcomes until exactly
`n` worlds are present, and add constant unused unit-cost queries until exactly
`m` resources are declared.  These padding operations preserve both optima.

Therefore the upper bound is attained exactly.

## 5. Consequences

### First binary-only scope above `3/2`

For `n<=5`, `K<=4`; for `m<=4`, again `K<=4`.  The sharp formula is then at most
`3/2`.

At

```text
n = 6 worlds
m = 5 binary unit-cost queries
```

one has `K=5`, `d=2`, and

\[
\boxed{
\max C_F/C_A=5/3.
}
\]

The six-world alternating threshold path attains

\[
(C_A,C_F)=(3,5).
\]

So binary observations need one more declared query than the unrestricted-arity
six-world/four-query ratio-2 witness before the ratio can exceed `3/2`.

### The earlier binary unbounded family is not extremal at fixed `(n,m)`

The branch-index-bit construction proves unbounded growth but is optimized for a
transparent routing interpretation, not for fixed `(n,m)` efficiency.  Threshold
paths provide the sharp finite extremum.

### Dependence only on `K=min(m,n-1)`

Under binary unit costs, the exact maximum ratio depends on world/query counts only
through the effective resource cap

\[
K=\min(m,n-1).
\]

Extra worlds beyond `m+1`, or extra queries beyond `n-1`, cannot improve the
extremal ratio.

## Implementation

- `adaptive_gain/binary_unit_cost_extremal_bounds.py`
- `tests/test_binary_unit_cost_extremal_bounds.py`

The threshold-path formula and sharp witnesses are checked by the general exact
adaptive and fixed solvers on a grid of small world/query counts.
