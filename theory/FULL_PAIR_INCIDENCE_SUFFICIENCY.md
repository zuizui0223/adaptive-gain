# Full target-pair incidence suffices for deterministic target-resolution cost

The five-world irreducible classification exposes an important representation
boundary.  The **inclusion-minimal fixed-cover kernel** is not enough to classify
adaptive routing geometry, but the **full identity-indexed cross-target pair
incidence** is stronger.  In the deterministic guaranteed-resolution problem it
is sufficient for both the exact fixed cost and the exact adaptive worst-path
cost.

This note states and proves that distinction.

## Setup

Let

- `W` be a finite represented world set;
- `T(w)` be the declared target label;
- each query `q` have positive cost `c(q)` and deterministic outcome `q(w)`.

For every pair of worlds with different targets define the separation bit

\[
S_q(u,v)=\mathbf 1[q(u)\ne q(v)],
\qquad T(u)\ne T(v).
\]

The **full target-pair incidence** retains

1. the identity of every represented world;
2. every target label;
3. every query identity and cost; and
4. every bit `S_q(u,v)` for every cross-target pair.

It is not the same as sorting pair rows, deleting dominated obligations, or
keeping only a minimal cover certificate.

## Fixed sufficiency

A fixed bundle `F` resolves the target exactly when every cross-target pair is
separated by at least one chosen query:

\[
\forall u,v:T(u)\ne T(v),\qquad
\exists q\in F:S_q(u,v)=1.
\]

Therefore the full incidence immediately determines every fixed bundle's
feasibility and hence the exact optimum `C_F`.

## Mixed-outcome reconstruction lemma

Fix a current represented-world subset `A` and one query `q`.  Build a graph
`G_q(A)` with vertex set `A`.  Put an edge between `u` and `v` exactly when

\[
T(u)\ne T(v)
\quad\text{and}\quad
S_q(u,v)=0.
\]

Thus an edge means **different targets but equal query outcome**.

### Lemma

Every query-outcome cell containing at least two target values is exactly one
connected component of `G_q(A)` containing at least two target values.

### Proof

An edge can join only equal-outcome worlds, so every graph component lies inside
one outcome cell.

Conversely let `C` be an outcome cell containing at least two target labels.  If
two worlds in `C` have different targets they are directly adjacent.  If two
worlds in `C` share one target, choose a world in `C` with a different target;
both original worlds are adjacent to it.  Hence all worlds in `C` are connected.
Therefore every target-mixed outcome cell is exactly one graph component. ∎

Outcome cells containing only one target can be split or merged internally
without affecting guaranteed target resolution: every such branch stops with
continuation cost zero.

## Adaptive sufficiency theorem

Let `V(A,R)` denote the minimum future worst-path cost when the admissible worlds
are `A` and the remaining query set is `R`.

For a candidate query `q`, the mixed-outcome reconstruction lemma recovers from
full pair incidence exactly the target-unresolved children

\[
A_{q,1},\ldots,A_{q,k}.
\]

All omitted outcome cells are target-pure and therefore have value zero.  Hence

\[
V(A,R)
=
\min_{q\in R}
\left[
 c(q)+
 \max_j V(A_{q,j},R\setminus\{q\})
\right],
\]

with the usual convention that the maximum over no mixed children is zero.
Queries whose only mixed child is the whole current set make no target-relevant
progress and can be ignored.

Every object on the right-hand side is determined by

- target labels;
- query costs; and
- full cross-target separation incidence.

By induction on the number of remaining queries, the exact adaptive value is
therefore determined by the full incidence.

Thus

\[
\boxed{
\text{full target-pair incidence determines both }C_A\text{ and }C_F
}
\]

for the finite deterministic guaranteed-target-resolution problem.

## Why the minimal fixed kernel is different

Pair-obligation dominance is safe for fixed cover: if separator set `H` is a
subset of separator set `E`, every fixed bundle covering `H` automatically covers
`E`, so `E` may be deleted from the fixed-cover instance.

That deletion need not preserve adaptive branch geometry.

The four-world minimal strict-gain core has raw cross-target separator rows

\[
(1,2,4,7),
\]

while the new deletion-minimal five-world core has

\[
(1,2,3,4,5,6).
\]

Both reduce under pair dominance to

\[
\boxed{(1,2,4)}.
\]

Yet their adaptive world structures are different.

An even sharper same-scope control uses five worlds and three queries.  The
irreducible strict-gain standard task has

\[
(C_A,C_F)=(2,3),
\]

while another task with the same inclusion-minimal kernel `(1,2,4)` has

\[
(C_A,C_F)=(3,3).
\]

So

\[
\boxed{
\text{minimal fixed kernel equality}
\not\Rightarrow
\text{adaptive cost equality}.
}
\]

The full incidence matrices of those tasks are different, as required by the
sufficiency theorem.

## What information may be discarded safely?

For deterministic **guaranteed target resolution**, full cross-target incidence
may forget distinctions among worlds that occur only inside target-pure outcome
cells, because those branches have continuation value zero.

This does **not** establish sufficiency for other objectives.  In particular it
does not automatically preserve

- transcript probabilities;
- mutual information;
- calibration likelihoods;
- stochastic error distributions;
- utilities that care about within-target state; or
- report licensing.

Those problems can require information beyond binary cross-target separation.

## Implementation

`adaptive_gain/target_pair_incidence.py` provides

- `target_pair_incidence_task()`;
- an exact fixed solver using the full incidence;
- an exact adaptive Bellman solver reconstructing target-mixed outcome cells; and
- `pair_incidence_sufficiency_audit()` against the direct world/outcome solver.

Regression tests include all `15^3 = 3,375` triples of arbitrary set partitions
on four worlds, not only binary outcomes.  They also include the five-world
irreducible core and the same-minimal-kernel/no-gain control.

## Scope boundary

This theorem is a representation theorem for finite deterministic guaranteed
resolution.  It does not say the full pair incidence is a minimal representation,
that the same compression works for information-valued objectives, or that a
pair-dominance kernel can replace the full incidence in adaptive optimization.
