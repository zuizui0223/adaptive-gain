# Integral pair packing as a fixed-cost lower-bound certificate

Status: exact finite deterministic lower-bound theorem for the `adaptive-gain` abstraction. It is a sufficient certificate, not a complete solver for every weighted fixed-resolution problem.

## 1. Cross-target separator sets

Let

\[
P_T=\{p=\{w_i,w_j\}:T(w_i)\ne T(w_j)\}
\]

be the cross-target pairs. For each pair define its separator-query set

\[
S(p)=\{q:o_q(w_i)\ne o_q(w_j)\}.
\]

A fixed resolving bundle `F` must contain at least one query from `S(p)` for every `p`.

Each query has positive integer cost `c(q)`.

## 2. Integral pair-packing theorem

Choose a subset of cross-target pairs

\[
P^*\subseteq P_T
\]

such that every declared query separates at most its cost many selected pairs:

\[
\boxed{
|\{p\in P^*:q\in S(p)\}|\le c(q)
\quad\forall q.
}
\]

Then every fixed resolving bundle has cost at least

\[
\boxed{C_F\ge |P^*|}.
\]

### Proof

Any fixed resolver `F` must cover every selected pair, so the total number of incidences between selected pairs and queries in `F` is at least `|P*|`:

\[
|P^*|
\le
\sum_{q\in F}|\{p\in P^*:q\in S(p)\}|.
\]

Packing feasibility gives

\[
\sum_{q\in F}|\{p\in P^*:q\in S(p)\}|
\le
\sum_{q\in F}c(q).
\]

Therefore

\[
|P^*|\le\sum_{q\in F}c(q).
\]

Since this holds for every fixed resolving bundle,

\[
C_F\ge|P^*|.
\]

No probability model is used.

## 3. Strict adaptive-gain certificate

Let the exact adaptive optimum be integer cost `C_A`. If the pair-packing search constructs

\[
|P^*|\ge C_A+1,
\]

then

\[
\boxed{C_F\ge C_A+1>C_A}
\]

and strict adaptive gain is certified **without solving the global fixed optimization**.

Implementation:

```text
pair_packing_lower_bound(...)
selected_policy_pair_packing_gain_certificate(...)
```

The search can stop as soon as it reaches the required lower bound `C_A+1`. If a configured search-state limit is reached first, the implementation raises; it does not convert incomplete search into a negative scientific conclusion.

## 4. Relation to private-pair certificate

The private-pair certificate is a special, especially transparent packing construction.

If each query `q` in a selected adaptive union has a pair `p_q` that no other declared query separates, select all those private pairs and assign unit pair weight. Distinct private-pair witnesses cannot be separated by the wrong essential query, so query capacities are respected in the unit-cost case. More generally, repeated capacity can support integer-cost extensions.

But pair packing can work even when no single pair proves one query mandatory.

Therefore

```text
private-pair certificate
subset of
integral pair-packing lower-bound certificates
subset of
all possible fixed-cost lower bounds.
```

The last inclusion can be strict because fractional/stronger combinatorial lower bounds may outperform integral unit-pair packing.

## 5. Five-world witness where private pairs are insufficient

A registered five-world strict-gain control has

```text
C_A=2
C_F=3
U=3
```

but one selected-union query has no globally private cross-target pair. The private-pair certificate therefore remains incomplete.

The pair-packing certificate instead finds three compatible cross-target pairs whose separator loads satisfy every unit query capacity. Hence

\[
C_F\ge3>C_A=2.
\]

This recovers strict gain without enumerating all fixed bundles.

## 6. Partial-bypass strict-gain controls

The two six-world controls introduced in `FIXED_BYPASS_PAIR_COVER.md` have

```text
C_A=3
C_F=4
```

while one contains internal redundancy and the other an external shortcut discount.

In both cases the packing search constructs four selected cross-target pairs, proving

\[
C_F\ge4>C_A=3.
\]

Thus pair packing certifies the **residual** adaptive gain even when some branch-exclusive overhead is consumed by bypass.

## 7. No-gain adverse control

For the four-world routing-bypass control,

```text
C_A=C_F=2.
```

The exact integral packing maximum is 2. A request for lower bound 3 completes without finding such a packing, so no strict-gain certificate is emitted.

This is a negative control on false certification.

## 8. Optimization boundary and prior art

The fixed side is a weighted target-pair-cover problem. The packing above is an integral feasible dual-style lower bound. Set Cover/Test Cover dual bounds, fractional relaxations, branch-and-bound, and related covering methods are established optimization ideas; this repository does not claim invention of those general methods.

The contribution here is narrower: connect a verifiable fixed-cost lower bound to the exact adaptive-tree optimum and the cross-repository routing/no-routing problem.

Relevant established Test Cover references are listed in `FIXED_BYPASS_PAIR_COVER.md`.

## 9. Next mathematical step

The natural next extension is a **fractional pair packing**

\[
y_p\ge0,
\qquad
\sum_{p:q\in S(p)}y_p\le c(q),
\]

which yields

\[
C_F\ge\sum_p y_p.
\]

That linear-programming relaxation can be stronger than integral unit-pair packing. It is deliberately not imported until its numerical/solver contract and exact-certification boundary are specified.
