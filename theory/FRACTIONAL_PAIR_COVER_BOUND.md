# Fractional pair-cover lower bounds and their limit

Status: exact finite deterministic LP-dual certificate for small tasks. This is an optimization aid inside `adaptive-gain`, not a new general LP method.

## 1. Fractional dual

For each cross-target pair `p`, assign a rational weight

\[
y_p\ge0.
\]

For every query `q`, impose

\[
\sum_{p:q\text{ separates }p} y_p\le c(q).
\]

Then every fixed resolving bundle satisfies

\[
C_F\ge\sum_p y_p.
\]

Because all acquisition costs are positive integers, `C_F` is integer, so the usable integer lower bound is

\[
\boxed{C_F\ge\left\lceil\sum_p y_p\right\rceil}.
\]

The exact small-task solver `exact_fractional_pair_packing()` maximizes this objective using rational vertex enumeration. It never converts a basis-search cap into an approximate optimum.

## 2. Why it is stronger than integral unit-pair packing

Integral pair packing restricts each selected pair to weight 1 and every unselected pair to weight 0. Fractional packing allows weights such as `1/2`.

A registered five-world control has

```text
C_A = 2
C_F = 3
```

while the maximum integral pair packing is only 2. The fractional optimum is

\[
\boxed{L_F=5/2}.
\]

Therefore

\[
C_F\ge\lceil5/2\rceil=3>C_A=2,
\]

certifying strict adaptive gain without solving the integer fixed cover.

One exact optimum weighting is supported on four cross-target pairs with weights

```text
1/2, 1/2, 1/2, 1
```

and satisfies every unit query-capacity constraint.

Thus the certificate hierarchy is genuinely strict on this control:

```text
private-pair certificate      fails
integral pair packing         fails to reach 3
fractional pair packing       certifies fixed cost >=3.
```

## 3. Fractional relaxation is still not complete

A second five-world control has

```text
C_A = 2
C_F = 3
```

but the exact fractional optimum is only

\[
\boxed{L_F=2}.
\]

Hence the relaxation gives only

\[
C_F\ge2,
\]

which does not separate fixed from adaptive cost even though the exact integer fixed optimum is 3.

This is an explicit pair-cover integrality-gap control:

```text
adaptive cost            = 2
fractional fixed bound   = 2
integer fixed optimum    = 3.
```

Therefore

```text
fractional certificate incomplete
!=
no adaptive gain.
```

The remaining proof burden is genuinely combinatorial.

## 4. Exact small-task solver

The dual has one variable per cross-target pair and one capacity inequality per query.

At a vertex with `k` positive pair weights, `k` linearly independent query-capacity inequalities can be chosen active. The solver therefore enumerates

```text
support of k positive pair variables
x
k active query constraints
```

for `k=0,...,min(number_of_pairs,number_of_queries)`.

Each small square system is solved by exact Gauss-Jordan elimination over `Fraction`. Candidate weights and all capacity inequalities are checked exactly.

Before enumeration, the implementation computes the total number of basis candidates. If this exceeds `max_basis_candidates`, it raises `FractionalPackingSearchLimitError`. It does not silently switch to floating-point or heuristic optimization.

## 5. Soundness chain

For any returned exact optimum `L_F`,

\[
L_F\le C_F.
\]

For integer fixed cost,

\[
\lceil L_F\rceil\le C_F.
\]

Therefore, if

\[
\lceil L_F\rceil>C_A,
\]

then

\[
\boxed{C_F>C_A}
\]

and strict adaptive gain is certified.

The implementation checks exactly this condition in

```text
selected_policy_fractional_pair_packing_gain_certificate().
```

## 6. Relation to established optimization

This is the standard LP-dual structure of a weighted covering relaxation specialized to the repository's cross-target pair hypergraph. Set Cover/Test Cover relaxations and integrality gaps are established optimization theory. `adaptive-gain` does not claim novelty for LP duality itself.

The repository-specific point is the **certificate ladder** linking those fixed-side lower bounds to an exact adaptive decision-tree cost:

```text
private pair
-> integral pair packing
-> fractional pair packing
-> exact integer fixed cover
```

and showing by explicit controls that every arrow can matter.

## 7. Next step

The integrality-gap control shows why a complete structural theorem cannot stop at fractional relaxation. The next candidate layer is an integer-cover lower bound stronger than the LP relaxation, for example:

- cover cuts over families of cross-target pairs;
- branch-and-bound lower-bound receipts;
- parameterized exact algorithms indexed by adaptive-tree union size or overhead;
- target-specific symmetry reduction before exact fixed optimization.

Any such extension must preserve a checkable certificate rather than only report an optimizer's answer.
