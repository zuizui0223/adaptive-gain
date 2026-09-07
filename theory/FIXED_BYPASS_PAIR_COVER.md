# Fixed bypass as a target-pair cover problem

Status: exact finite deterministic theorem for the `adaptive-gain` abstraction. It does not replace source-repository scientific models.

## 1. Fixed resolution is a cross-target pair cover

For represented worlds `W` and target map `T`, define

\[
P_T=\{\{w_i,w_j\}:T(w_i)\ne T(w_j)\}.
\]

Each query `q` covers the pair when it separates the two declared outcomes:

\[
S_q=\{\{w_i,w_j\}\in P_T:o_q(w_i)\ne o_q(w_j)\}.
\]

A fixed query bundle resolves the target iff its separator sets cover every pair in `P_T`.

This is a target-specific pair-cover formulation related to classical Test Cover. `adaptive-gain` uses only cross-**target** pairs, not necessarily every pair of distinct represented worlds.

Prior-art boundary: Test Cover, Set Cover, LP relaxations, and branch-and-bound are established optimization topics. The repository's narrower role is to connect those fixed-side structures to the adaptive worst-path cost comparison exposed by MROD/PAYOFF/BALANCE.

## 2. Refined bypass decomposition

Let

```text
C_A = minimum adaptive worst-path resolution cost
C_F = global minimum fixed resolving cost
U   = total cost of all distinct query identities used anywhere in the selected optimal adaptive tree
C_U = minimum fixed resolving cost using only queries in that selected tree union
```

Then

\[
\boxed{C_A\le C_F\le C_U\le U}
\]

and

\[
\boxed{
U-C_A
=(C_F-C_A)+(C_U-C_F)+(U-C_U)
}.
\]

The terms are

```text
branch-exclusive overhead = U - C_A
realized adaptive gain     = C_F - C_A
external shortcut discount = C_U - C_F
internal union redundancy  = U - C_U
```

so

\[
\boxed{
\text{gain}
=
\text{overhead}
-
\text{internal redundancy}
-
\text{external shortcut}
}.
\]

Bypass is therefore a discount rather than a yes/no veto.

## 3. Private-pair no-bypass theorem

A query has a globally private cross-target pair when it is the only declared separator of that pair. Every fixed resolver must then contain that query.

If every query in the selected adaptive union has a globally private pair, the full union is mandatory for every fixed resolver. Since the union itself resolves,

\[
\boxed{C_F=U}.
\]

If also `U>C_A`, strict adaptive gain follows without globally optimizing the fixed class.

This strong certificate proves the registered MROD-style and PAYOFF-style source-derived witnesses.

Its failure does **not** imply a bypass exists: fixed optimality can arise from a combinatorial cover lower bound with no single query owning a private pair.

## 4. Bypass controls

### Internal redundancy

A four-world branch-dependent control has

```text
C_A=2, C_F=2, C_U=2, U=3.
```

The selected adaptive union contains a cheaper fixed subset, so internal redundancy is one and gain is zero.

### External shortcut

A separate four-query control has

```text
C_A=2, C_F=2, C_U=3, U=3.
```

The selected union is internally irreducible, but a query outside the union creates a cheaper fixed route.

### Partial bypass with residual gain

Two six-world controls verify that bypass can consume only part of the overhead:

```text
partial internal:
C_A=3, C_F=4, C_U=4, U=5

partial external:
C_A=3, C_F=4, C_U=5, U=5.
```

Both retain one unit of realized adaptive gain.

## 5. Lower-bound certificate ladder

Private pairs are only the first fixed-side lower bound.

### Integral pair packing

Choose cross-target pairs so that each query separates at most `cost(q)` selected pairs. Then the number of selected pairs is a valid lower bound on `C_F`.

### Fractional pair-cover dual

Assign rational nonnegative weights `y_p` to cross-target pairs with

\[
\sum_{p:q\text{ separates }p}y_p\le c(q).
\]

Then

\[
C_F\ge\sum_p y_p,
\qquad
C_F\ge\left\lceil\sum_p y_p\right\rceil
\]

for integer acquisition costs.

A registered five-world control needs the fractional layer: integral packing gives only 2, while the exact fractional optimum is `5/2`, proving integer fixed cost at least 3 against `C_A=2`.

### LP integrality gap

Another five-world control has

```text
C_A=2
fractional lower bound=2
C_F=3.
```

Thus fractional packing is not complete for strict gain.

## 6. Exact integer budget-infeasibility proof

Strict gain does not require the exact numerical optimum `C_F`. Once `C_A` is known, it is sufficient to prove that **no fixed resolver has cost <= C_A**.

`fixed_budget_cover_decision()` does this exactly:

1. choose a still-uncovered cross-target pair;
2. list every remaining separator whose cost fits the residual budget;
3. branch over every such query;
4. update uncovered pairs, available queries, and budget;
5. declare a leaf infeasible only when the selected pair has no affordable separator.

If all branches fail at root budget `B=C_A`, then

\[
\boxed{C_F>C_A}.
\]

The generated proof tree is independently checked by `verify_fixed_budget_decision_certificate()`. The verifier reconstructs the pair system, checks that every affordable separator branch is present, and recomputes each child state. Tampered proofs fail regression tests.

This closes the registered LP-integrality-gap strict-gain example without computing the full fixed optimum.

The search remains exponential in the worst case. A state cap raises `IntegerCoverProofLimitError`; it is never converted into an infeasibility claim.

## 7. Exact fixed optimum

If the actual value of `C_F` is scientifically or computationally needed, the repository can still solve the stronger optimization problem. For strict gain alone, the integer budget proof is enough.

The resulting hierarchy is

```text
private-pair necessity
  -> integral pair packing
  -> fractional pair-cover dual
  -> exact integer infeasibility proof at B=C_A
  -> exact fixed optimum when its value is required
```

Each layer is useful on explicit controls, and failure of any lower layer means only `certificate_incomplete`.

## 8. Minimal-universe validation

For the complete balanced universe

```text
4 worlds
binary target split 2+2
3 labeled binary unit-cost queries
```

there are 4096 labeled tasks and exactly 192 strict-gain tasks. The private-pair certificate already catches all 192 in this deliberately tiny universe.

A separate exhaustive regression now also compares the integer budget proof with the exact fixed/adaptive classification on all 4096 tasks; the strict-gain classifications must agree exactly.

That finite completeness is not a prevalence claim and does not extend automatically to larger vocabularies.

## 9. What remains open

The exact strict-gain decision gap is now closed for finite deterministic tasks, but proof complexity remains open.

Useful next directions are:

- compressing large integer proof trees into stronger cover inequalities;
- symmetry reduction of equivalent pair/query states;
- parameterized bounds using branch-exclusive overhead or selected-union size;
- continuous analogues where cross-target pairs form an uncountable parameter set;
- stochastic and information-valued analogues where fixed-side utility is not binary pair coverage.

See also `INTEGER_FIXED_COVER_PROOF.md` and `OPEN_PROBLEMS.md`.
