# Bounded-arity Pareto tradeoff for a required structural gap

## Purpose

The binary theorem gives a single exact corner for an integer structural gap `q`.
Allowing larger query arity changes the situation in a precise but non-monotone way.

Higher arity can reduce adaptive depth and therefore reduce the number of fixed-mandatory queries / productive-frontier obligations required for the same gap.  It **cannot**, however, reduce the minimum represented-world count.  For some `(q,b)` these two minima cannot be achieved by the same task, so the correct object is a Pareto frontier rather than one scalar information complexity.

Scope: finite deterministic unit-cost sensing, maximum query arity `b>=2`, and structural gap

\[
\Delta g=C_F-C_A\ge q\ge1.
\]

---

## 1. Minimum query/frontier burden at arity `b`

A depth-`h` rooted decision tree with at most `b` nonempty children per internal node has at most

\[
T_b(h)=1+b+\cdots+b^{h-1}
=\frac{b^h-1}{b-1}
\]

internal nodes.

If `C_A=h` and `C_F-C_A>=q`, then

\[
C_F\ge h+q.
\]

Flattening the adaptive tree gives

\[
C_F\le T_b(h),
\]

so necessarily

\[
T_b(h)-h\ge q.
\]

Define

\[
\boxed{
h_b^*(q)=\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\}.}
\]

Then every task with gap at least `q` satisfies

\[
C_A\ge h_b^*(q),
\qquad
C_F\ge h_b^*(q)+q.
\]

Since `C_F<=m` under unit costs and `C_F<=|H_min|`,

\[
\boxed{
m_{\min}(q,b)=E_{\min}(q,b)=q+h_b^*(q).}
\]

The private-pair tree construction attains this lower bound: choose a bounded-arity tree of height `h_b^*` with exactly `h_b^*+q` internal nodes and assign one physical query to every internal node. Every query becomes fixed-mandatory.

If the resulting task had adaptive cost below `h_b^*`, the bounded-arity flattening bound at that lower depth would contradict the minimality of `h_b^*`. Hence the adaptive cost is exact.

---

## 2. The minimum world count is arity-independent

The exact unrestricted-arity productive-tree bound at `n` represented worlds and adaptive depth `h` is

\[
M(n,h)
=
n+1-
\max\left(2,\left\lceil\frac{n}{2^{h-1}}\right\rceil\right).
\]

Therefore every deterministic task, regardless of allowed query arity, obeys

\[
\Delta g
\le
\max_h [M(n,h)-h].
\]

The maximum simplifies to

\[
\boxed{
\max_h[M(n,h)-h]
=
n-1-\lceil\log_2 n\rceil.
}
\]

A useful proof step is

\[
h+
\max\left(2,\left\lceil\frac{n}{2^{h-1}}\right\rceil\right)
\ge
\lceil\log_2 n\rceil+2.
\]

Thus the smallest world count capable of gap `q` is

\[
\boxed{
n_{\min}(q)=q+h_2^*(q)+1,}
\]

exactly the binary formula.  Binary private-pair witnesses attain it, so allowing more than two outcomes cannot improve this world-count lower bound.

Hence query arity has an asymmetric effect:

\[
\boxed{
\text{higher arity can lower query/frontier burden but not minimum world burden.}
}
\]

---

## 3. Exact Pareto frontier

For a fixed adaptive depth `h`, a gap `q` requires

\[
I=h+q
\]

fixed-mandatory internal queries.

Let

\[
\boxed{
n_b(q,h)=\min\{n:F_b(n,h)\ge h+q\},}
\]

where `F_b(n,h)` is the repository's exact bounded-arity internal-node recurrence.

Then

\[
\boxed{
(n_b(q,h),\ h+q,\ h+q)
}
\]

is the minimum `(worlds, queries, frontier edges)` coordinate at depth `h`.

Only depths

\[
h_b^*(q)\le h\le h_2^*(q)
\]

can be Pareto-relevant.  Beyond the binary minimum depth the world count cannot fall below `n_min(q)` while query/frontier count continues to increase.

Therefore the exact Pareto frontier is obtained by scanning this finite depth interval and retaining precisely those depths at which `n_b(q,h)` strictly decreases.

### Example: `q=3`, `b=4`

The query-optimal depth is `h=2`, giving

\[
(8\text{ worlds},5\text{ queries},5\text{ frontier edges}).
\]

The world-optimal depth is `h=3`, giving

\[
(7\text{ worlds},6\text{ queries},6\text{ frontier edges}).
\]

Neither dominates the other. Thus there is no single componentwise first corner.

By contrast, `q=2,b=3` has a single Pareto point `(6,4,4)` and simultaneously attains both minima.

---

## 4. Asymptotic contrast

Let

\[
k_b(q)=\left\lceil\log_b((b-1)q+1)\right\rceil.
\]

Then

\[
\boxed{h_b^*(q)\in\{k_b(q),k_b(q)+1\}.}
\]

Indeed `T_b(k_b)>=q`, while one further level gives more than enough capacity to pay the additive depth term.

Hence

\[
\boxed{
h_b^*(q)=\log_b q+O(1),}
\]

and therefore

\[
\boxed{
m_{\min}(q,b)=E_{\min}(q,b)=q+\log_b q+O(1).}
\]

But the world minimum remains

\[
\boxed{
n_{\min}(q)=q+\log_2 q+O(1).}
\]

So richer-outcome cues change the logarithmic routing overhead base from `2` to `b`, while the minimum represented-state burden remains governed by the binary world-count ceiling.

---

## 5. Relation to the eco-evolutionary theory

If a downstream dynamical regime requires gap `q`, then the information structure required to make that regime reachable is not described by one universal scalar once arity is allowed to vary.

Instead:

```text
required dynamical gain
    -> required structural gap q
    -> arity-dependent routing/query minimum
    -> arity-independent world minimum
    -> exact world-vs-query Pareto frontier
```

This qualifies the binary result without weakening it.  Binary sensing has a single exact corner; higher-arity sensing can trade represented-world complexity against query/frontier complexity.

No novelty is claimed for elementary bounded-arity tree counting.  The repository-specific contribution is the composition with the adaptive/fixed gap and the use of the resulting Pareto frontier as a dynamical reachability constraint.
