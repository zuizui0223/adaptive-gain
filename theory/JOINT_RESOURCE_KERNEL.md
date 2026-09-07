# Joint resource kernel preserving both adaptive and fixed costs

The resource-labelled continuation quotient preserves both adaptive and fixed
resolution costs by retaining physical query identity across branches.  This
note asks which **global** reductions may be applied before building that joint
representation.

The answer implemented here uses two reductions only.

## 1. Same-target world twins

Let `u` and `v` have the same target.  They are global target-relevant twins when,
for every remaining query `q` and every remaining world `w` of a different
target,

\[
\mathbf 1[q(u)\ne q(w)]
=
\mathbf 1[q(v)\ne q(w)].
\]

Then the cross-target pair obligations involving `u` and `v` are duplicates for
fixed cover.  On the adaptive side, no unresolved target-mixed continuation can
distinguish `u` from `v` in a target-relevant way.  One representative world is
therefore sufficient.

Hence deleting duplicate twins preserves both costs:

\[
\boxed{C_A'=C_A,\qquad C_F'=C_F.}
\]

## 2. Global query refinement dominance

For query `q`, let `S(q)` be the set of all currently represented cross-target
world pairs separated by `q`.

If

\[
\boxed{S(q)\supseteq S(r),\qquad c(q)\le c(r),}
\]

then `q` globally dominates `r`.

### Fixed side

Any fixed bundle containing `r` can replace `r` by `q` without losing separation
of any cross-target pair and without increasing cost.  If `q` is already present,
`r` can simply be deleted.

Thus `r` is unnecessary for the fixed optimum.

### Adaptive side

On every future branch `A`, restriction preserves the inclusion

\[
S_A(q)\supseteq S_A(r).
\]

The state-local refinement theorem then applies.  If a policy would choose `r`
on a branch where `q` has not yet been used, choose `q` instead.  If `q` was used
earlier on that same realized path, `r` is constant on every unresolved
`q`-child and is unnecessary there.

Therefore global removal of `r` preserves the adaptive optimum as well.

So

\[
\boxed{
S(q)\supseteq S(r),\ c(q)\le c(r)
\Longrightarrow
(C_A,C_F)\text{ unchanged after removing }r.
}
\]

Equal-cost equal-effect queries are tie-broken by declared index only to make the
reduction deterministic.

## 3. Why the reductions are iterated

The reductions interact.

- Removing duplicate worlds may make two queries newly comparable by refinement.
- Removing a dominated query may make same-target worlds newly twin-equivalent.

Therefore `joint_resource_kernel()` alternates the two exact reductions until a
fixed point is reached.

A registered three-world control demonstrates the second direction.  A dominated
`noise` query distinguishes two target-0 worlds relative to one target-1 world.
A cheaper `direct` query separates both target-0 worlds from that target-1 world
and dominates `noise`.  After `noise` is removed, the two target-0 worlds become
twins and one can be collapsed on the next iteration.

## 4. Relation to the adaptive-only kernels

This joint kernel is deliberately weaker than the state-local adaptive kernels.

Adaptive-only search may remove a query because another query dominates it **at
one current Bellman state**.  That is sufficient for `C_A`, but need not preserve
the global physical-query reuse structure needed by `C_F`.

The joint kernel instead performs only root-global reductions whose validity
persists on every branch.  Thus the current hierarchy is

\[
\boxed{
\text{full task}
\to
\text{joint resource kernel}
\to
\begin{cases}
\text{resource-labelled joint quotient for }(C_A,C_F),\\
\text{stronger state-local adaptive kernels for }C_A\text{ only}.
\end{cases}
}
\]

## 5. Validation

The regression suite requires exact preservation of both costs on all

\[
15^3=3375
\]

three-query arbitrary deterministic partition tasks on four balanced worlds.
It also contains:

- explicit query-refinement dominance;
- a two-iteration query-removal -> world-twin cascade; and
- the earlier strict-vs-bypass collision, which must remain `(2,3)` versus `(2,2)`
  after kernelization.

These are finite synthetic structural checks, not empirical prevalence results.

## 6. Scope boundary

The kernel is exact for finite deterministic guaranteed target resolution with
positive additive query costs.  It is not claimed to be the coarsest joint-safe
kernel.  In particular, the next question is whether global query resources can
be quotient-ed under a certified renaming/automorphism while still preserving
cross-branch bundle reuse, and whether stronger joint reductions exist that are
not simple pairwise refinement or world-twin equivalence.
