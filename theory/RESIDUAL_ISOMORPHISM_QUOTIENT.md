# Exact residual-state isomorphism quotient

Status: exact finite deterministic fixed-cover proof compression for `adaptive-gain`. This is a proof-engineering layer over the already-defined target-pair cover; it does not alter the scientific models in MROD, PAYOFF, or BALANCE.

## 1. Residual fixed-cover state

After any exact kernel reductions, a bounded fixed-cover continuation is determined by

```text
remaining budget B,
available query costs,
incidence between uncovered cross-target pair obligations and available queries.
```

The names of the worlds, the order of the pair obligations, and the names/order of equal-cost queries are not part of the continuation value.

Represent a residual state as a weighted binary incidence matrix:

\[
M\in\{0,1\}^{r\times m},
\]

where row `p` is one still-uncovered cross-target pair and column `q` is one available query. Entry `M[p,q]=1` means query `q` separates that pair. Let the column costs be

\[
c=(c_1,\ldots,c_m).
\]

The bounded question is whether some column subset of total cost at most `B` covers every row.

## 2. Isomorphism

Two residual instances `(M,c,B)` and `(M',c',B')` are isomorphic when

1. `B=B'`;
2. there is a bijection of query columns preserving acquisition cost; and
3. after applying that column bijection, the rows of `M` and `M'` agree as multisets.

Row identities are intentionally ignored: a row is only an obligation that must be covered. Query names are also ignored, but query costs are not.

### Feasibility invariance

Suppose `phi` is a cost-preserving query bijection from instance 1 to instance 2. Every fixed bundle `F` in instance 1 maps to `phi(F)` in instance 2 with exactly the same cost. Because the transformed row multiset is identical, `F` covers every row iff `phi(F)` covers every row.

Therefore

\[
\boxed{
F(M,c,B)=F(M',c',B')
}
\]

for isomorphic residual states, where `F` is the bounded fixed-cover feasibility indicator.

This licenses subproof sharing across label-different residual states.

## 3. Exact canonicalization

`canonical_residual_pair_cover_signature()` searches cost-preserving query permutations and sorts the obligation rows after each candidate permutation. The lexicographically minimum representation is the canonical signature.

To reduce factorial enumeration without changing the equivalence relation, query columns are first partitioned by invariants preserved under every weighted-incidence isomorphism:

```text
query cost,
number of covered rows,
multiset of degrees of the rows covered by that query.
```

Only permutations within equal invariant classes need enumeration. This is a safe restriction because a true isomorphism must preserve all three invariants.

The canonicalizer is exact for the enumerated finite state. It is not claimed to be an efficient general graph-canonicalization algorithm.

## 4. Fail-closed permutation cap

If the exact number of within-color-class permutations exceeds `max_permutations`, the implementation raises

```text
ResidualIsomorphismLimitError
```

rather than returning an approximate canonical label or silently treating the raw query labels as canonical.

Thus a resource limit means

```text
isomorphism quotient not completed
```

not

```text
states are non-isomorphic.
```

## 5. Explicit witness and independent verifier

When two residual instances receive the same canonical signature, `residual_pair_cover_isomorphism_witness()` constructs an explicit query bijection.

`verify_residual_pair_cover_isomorphism()` independently checks:

- equal remaining budget;
- a genuine permutation of query columns;
- cost preservation column by column; and
- equality of the transformed separator-row multisets.

The verifier does not trust the canonical code itself.

## 6. Exact quotient search

`isomorphic_fixed_budget_cover_decision()` applies the same exact pair/query kernel reductions used by the fixed-cover kernel, then canonicalizes every genuine branch state.

Only **infeasible** canonical classes are reused across label-different residual states. This choice keeps constructive feasible-bundle output simple: a feasible state is solved in its current query labels instead of transporting a cached bundle through an isomorphism.

For strict adaptive gain, the important case is infeasibility at

\[
B=C_A,
\]

so this asymmetric memoization captures the proof-compression target directly.

## 7. Seeded strict-gain compression witness

A registered six-world / six-query unit-cost synthetic task has

```text
C_A = 2
C_F = 3.
```

At fixed budget `B=2`, exact label-specific residual states number

```text
4,
```

but the weighted-incidence quotient contains only

```text
2
```

isomorphism classes. Two infeasible residual states are therefore reused through label-independent isomorphism.

The first merge exports an explicit query-bijection witness and that witness is independently verified.

This is a deliberately small proof-compression control, not an empirical prevalence claim or a universal compression ratio.

## 8. Complete minimal-universe regression

For all

```text
4 worlds,
binary target split 2+2,
3 labeled binary unit-cost queries
```

there are `16^3=4096` declared tasks. The exact adaptive/fixed classification has 192 strict-gain tasks.

The isomorphism-quotient fixed decision at `B=C_A` is checked on all 4096 tasks and must reproduce exactly

```text
strict gain = 192
false positive = 0
false negative = 0.
```

This validates the quotient implementation on the complete deliberately tiny universe.

## 9. Relation to exact-state DAG and kernelization

Three operations are now distinct:

1. **kernelization** removes logically redundant rows/columns and propagates forced queries;
2. **exact-state DAG sharing** merges histories reaching literally identical residual bitmask states;
3. **isomorphism quotienting** additionally merges residual states whose names/column identities differ but whose weighted incidence structures are isomorphic.

Thus

\[
\text{raw proof tree}
\to
\text{kernelized states}
\to
\text{exact-state DAG}
\to
\text{isomorphism classes}.
\]

Each arrow preserves the bounded fixed-cover decision exactly.

## 10. Scope boundary

The current canonicalizer uses exact small-state permutation enumeration with a hard cap. It does not claim polynomial-time graph isomorphism, canonical labeling of arbitrary hypergraphs, or a general-purpose symmetry solver.

The next question is whether larger residual states can be quotient more cheaply using certified color refinement, automorphism generators, or source-specific structure without weakening exactness.

## Reproduce

```bash
python -m pytest -q tests/test_isomorphism_quotient.py
```
