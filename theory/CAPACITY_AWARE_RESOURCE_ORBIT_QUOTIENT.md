# Capacity-aware resource orbit quotient

The resource-labelled continuation quotient preserves branch-crossing physical
query identity, but can still contain many states related only by a symmetry of
the entire declared task.  This note quotients those **states**, while retaining
how many distinct query resources remain.

## 1. Two different symmetry notions

They must not be conflated.

### Pair-cover automorphism

A fixed residual pair-cover instance may admit a permutation of query columns and
obligation rows that preserves its weighted incidence.  This is sufficient for
fixed-proof canonicalization and proof-branch transport.

The unique minimal four-world strict-gain core has pair-cover query automorphism

\[
\operatorname{Aut}_{cover}\cong S_3.
\]

That symmetry is **not** induced by an automorphism of the full deterministic
world/query task.  It is a symmetry of the reduced fixed comparator.

### Full task automorphism

A full task automorphism consists of

- a target-preserving permutation of represented worlds; and
- a cost-preserving permutation of physical query tokens,

such that every query partition is carried to the mapped query partition, up to
irrelevant relabeling of that query's outcome symbols.

Only this stronger symmetry is used to quotient adaptive/fixed resource states.

The deletion-minimal five-world core has a genuine nontrivial full-task
automorphism: two target-1 worlds are exchanged simultaneously with two query
resources.

## 2. Why orbit cardinality alone is not enough

Even when several resources are symmetry-related, a fixed bundle may need more
than one member of that orbit.  Therefore the quotient does **not** replace an
orbit by one reusable token.

A state retains explicit bitmasks for

\[
(W, R)
\]

where `W` is the current world subset and `R` is the remaining physical-query
subset.  During fixed-bundle replay it retains

\[
(W,R,B)
\]

where `B` is the still-selected fixed bundle.

A full task automorphism transports all masks simultaneously:

\[
(W,R,B)\mapsto(g_WW,g_QR,g_QB).
\]

The canonical state is the lexicographically least transported tuple.

Because `R` and `B` remain subsets of physical tokens, their bit counts and
orbit capacities are preserved automatically.  Consuming one resource changes
the remaining subset, so the subsequent canonicalization automatically uses the
appropriate stabilizer/orbit structure of the new state rather than assuming the
original orbit remains intact.

This is the exact small-task meaning of

\[
\boxed{\text{resource orbit + capacity}.}
\]

## 3. Adaptive and fixed recursions

Adaptive evaluation memoizes canonical `(W,R)` states.  It still chooses an
actual available query token and removes exactly that token on the realized path.

Fixed evaluation chooses one original bundle `B` and recursively replays it while
memoizing canonical `(W,R,B)` states.  The same bundle subset is transported with
the state, so branch-crossing resource reuse and resource multiplicity remain
explicit.

Therefore exact full-task automorphism quotienting changes only labels, not the
underlying decision/resource problem:

\[
\boxed{
C_A^{orbit}=C_A,\qquad C_F^{orbit}=C_F.
}
\]

## 4. Five-world capacity control

For the five-world deletion-minimal standard core,

\[
C_A=2,\qquad C_F=3.
\]

Its full task has a two-element automorphism group that exchanges two queries and
two target-1 worlds.  The canonical fixed replay of the root still contains all
three physical query tokens:

```text
remaining-query capacity = 3
selected-bundle capacity = 3
```

so symmetry does not turn the fixed cost three into one or two.

This differs from the four-world `S3` pair-cover symmetry: the latter is a valid
fixed-incidence automorphism but not a full-task automorphism and is therefore not
used by the joint state quotient.

## 5. Exact small-task automorphism enumeration

`resource_orbit_quotient.py` enumerates:

- permutations within target-equal world classes; and
- permutations within equal-cost query classes,

then keeps exactly the pairs that preserve every query's outcome partition up to
outcome-symbol relabeling.

The enumeration is factorial and guarded by `max_candidates`.  Exceeding the cap
raises `ResourceOrbitLimitError`; it is never interpreted as asymmetry.

## 6. Validation

Regression tests require:

- the five-world genuine task symmetry to preserve `(C_A,C_F)=(2,3)` and all
  three root resource tokens;
- the previous strict-vs-bypass collision to remain `(2,3)` versus `(2,2)`; and
- exact joint-cost agreement over all `16^3=4,096` balanced four-world binary
  tasks.

The earlier `RESOURCE_ORBIT_CAPACITY.md` control remains complementary: it shows
that even a large pair-cover resource orbit does not license physical-token
collapse.

## 7. Scope boundary

This is exact only for the declared finite deterministic task.  It does not claim
that orbit cardinality is a sufficient summary by itself, that full-task
automorphisms can be found cheaply in general, or that the construction extends
unchanged to noisy likelihoods, calibration-changing actions, or continuous
uncertainty sets.

The next question is whether the explicit query subsets can be replaced by a
smaller **capacity/stabilizer signature** without losing `C_F` or `C_A`.
