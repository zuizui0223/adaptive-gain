# Unique normal form of minimal strict adaptive gain

Status: exact finite classification for the deliberately minimal deterministic universe

```text
4 represented worlds
binary target split 2+2
3 binary unit-cost queries.
```

It is not a general characterization of adaptive experimental design.

## 1. Standard representative

Choose target worlds

```text
T(w0)=T(w1)=0
T(w2)=T(w3)=1
```

and three binary unit-cost queries

```text
q_left  = (0,0,1,0)
q_route = (0,1,1,0)
q_right = (0,1,1,1).
```

The exact costs are

\[
\boxed{C_A=2,\qquad C_F=3}.
\]

## 2. Adaptive tree

`q_route` partitions the represented worlds into

```text
outcome 0: {w0,w3}
outcome 1: {w1,w2}.
```

Both branches remain target-ambiguous, but they need different one-query continuations:

```text
{w0,w3} -> q_right resolves
{w1,w2} -> q_left resolves.
```

Thus the worst adaptive path costs two unit queries.

## 3. Why fixed needs all three queries

There are four cross-target pairs:

```text
p0=(w0,w2)
p1=(w0,w3)
p2=(w1,w2)
p3=(w1,w3).
```

Using bit order `(p0,p1,p2,p3)`, the three query separator masks are

```text
q_right -> 0011 = 3
q_left  -> 0101 = 5
q_route -> 1001 = 9
```

up to query ordering.

Equivalently, the separator sets are

```text
q_right = {p0,p1}
q_left  = {p0,p2}
q_route = {p0,p3}.
```

So one pair `p0` is separated by all three queries, while each of the other three pairs is a globally private pair for exactly one query:

```text
p1 forces q_right
p2 forces q_left
p3 forces q_route.
```

Every fixed resolver must therefore buy all three queries, giving `C_F=3`.

The minimal gain is precisely the ability to avoid buying both branch-specific continuations on one realized path.

## 4. Symmetry quotient

The finite target-resolution problem is unchanged by:

1. permuting the two worlds inside either target class;
2. swapping the two target classes;
3. permuting query identities;
4. flipping the two outcome labels independently for each binary query.

`canonical_minimal_separator_signature()` quotients those symmetries by using only cross-target pair-separation masks and selecting the lexicographically smallest world-symmetry representative.

The canonical strict-gain signature is

\[
\boxed{(3,5,9)}.
\]

## 5. Exact 4096-task iff classification

There are

\[
16^3=4096
\]

labeled triples of binary outcome maps on four worlds.

Exhaustive regression against the exact adaptive and fixed solvers shows:

```text
strict adaptive gain tasks = 192
tasks with canonical signature (3,5,9) = 192
false positives = 0
false negatives = 0.
```

Hence, **within this minimal scope only**,

\[
\boxed{
C_A<C_F
\iff
\text{canonical separator signature}=(3,5,9).
}
\]

All 192 labeled strict-gain tasks are therefore one symmetry orbit.

## 6. Why the orbit contains 192 labeled tasks

For the standard representative:

- target-equivalence-preserving world relabeling produces 4 distinct separator-signature placements;
- query identity permutations contribute `3! = 6` labeled orderings;
- independent binary outcome flips contribute `2^3 = 8` raw outcome labelings.

Thus

\[
4\times6\times8=192.
\]

`standard_raw_symmetry_orbit_size()` independently constructs this orbit and returns exactly 192.

## 7. Relation to PAYOFF and MROD source-derived witnesses

The PAYOFF source-derived four-world routing abstraction lies in this same minimal normal-form class: one first contrast routes the second measurement and each fixed query has a private cross-target obligation.

The MROD nuisance-expanded witness has more represented hidden worlds because inactive-assay randomness is made explicit, so it is not literally a four-world member of this minimal universe. Its decision structure nevertheless realizes the same routing pattern:

```text
one routing observation
-> two unresolved branches
-> different branch-specific one-query continuations.
```

The normal-form theorem therefore explains the smallest deterministic skeleton shared by the positive source-derived examples without claiming their scientific models are identical.

## 8. Claim boundary

The iff theorem depends on all declared restrictions:

```text
4 worlds
2+2 target multiplicity
3 queries
binary outcomes
unit query costs.
```

It does not extend automatically to unequal costs, multi-outcome queries, more worlds, more target labels, noisy likelihoods, continuous parameter sets, or expected-information objectives.

The repository already contains larger strict-gain controls that have positive root target information, partial fixed bypass, fractional-only fixed-cost certificates, and LP integrality gaps. Those are intentionally outside this minimal normal form.

## Reproduce

```bash
python -m pytest -q tests/test_minimal_normal_form.py
```
