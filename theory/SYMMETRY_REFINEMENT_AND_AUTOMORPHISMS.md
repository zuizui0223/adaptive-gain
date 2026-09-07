# Refinement, individualization, and residual automorphisms

Status: exact finite proof-engineering results for weighted residual target-pair cover. These results concern representation/canonicalization cost, not biological effect sizes.

## 1. Three different sources of apparent symmetry

After pair/query kernelization, an exact residual fixed-cover state is a weighted bipartite incidence structure between

- uncovered cross-target pair obligations; and
- available queries with integer acquisition costs.

Three different phenomena can make several query columns look interchangeable.

### A. Local indistinguishability removed by color refinement

Queries can share the same cost and first-order degree summary but acquire different stable colors after neighboring row/query colors are propagated.

### B. Higher-order indistinguishability removed by individualization

Stable color refinement can still leave a non-singleton class even when choosing one query as a temporary distinguished vertex reveals different downstream structures.

### C. Genuine automorphism

Several queries can remain interchangeable because a real cost-preserving incidence automorphism maps them into one another. No sound canonicalizer may declare such query identities intrinsically different.

The repository now audits all three layers separately.

## 2. Stable color-refinement search count

If stable query color classes are

\[
C_1,\ldots,C_k,
\]

then exact permutation enumeration restricted to those classes requires

\[
N_{\rm color}=\prod_i |C_i|!
\]

candidate relabelings.

A registered eight-query benchmark reduces

\[
720\to 12
\]

at this stage.

See `BIPARTITE_COLOR_REFINEMENT.md`.

## 3. Exact individualization-refinement

`individualization_refined_canonical_signature()` chooses a canonical non-singleton stable color class, temporarily individualizes one query in that class, refines again, and recursively continues until all query colors are singleton.

Every member of the selected cell is branched, so the resulting canonical form remains exact. Search caps raise `IndividualizationRefinementLimitError`; no approximate signature is returned.

The IR canonical encoding is not required to be byte-for-byte identical to the earlier brute-force lexicographic encoding. Exactness means that it induces the same weighted-incidence isomorphism classes.

That condition is checked over all `4096` tasks in the complete four-world / three-query minimal universe: the old exact canonicalizer and IR canonicalizer induce a one-to-one correspondence between equivalence classes.

### Regular adverse controls

For the bipartite 8-cycle and the disjoint union of two 4-cycles,

```text
stable color permutation count = 24
IR canonical leaves            = 8.
```

The two structures are still assigned different canonical signatures.

Thus individualization improves on stable color refinement while preserving exact discrimination.

## 4. Exact query automorphism group

Let `G` be the group of cost-preserving query permutations that leave the obligation-row multiset unchanged.

`residual_automorphism_group()` enumerates `G` exactly for small residual instances, returns a generator set, and reports the query orbits.

If stable color refinement leaves

\[
N_{\rm color}=\prod_i |C_i|!
\]

allowed query relabelings, then `G` acts freely on those relabelings by composition. Therefore the exact number of distinct labeled incidence forms is

\[
\boxed{
N_{\rm distinct}=\frac{N_{\rm color}}{|G|}
}.
\]

The division is checked exactly in the implementation.

## 5. Registered symmetry table

| Residual structure | `N_color` | IR leaves | `|Aut|` | `N_distinct` |
|---|---:|---:|---:|---:|
| Minimal strict-gain normal form | 6 | 6 | 6 | **1** |
| Connected bipartite 8-cycle | 24 | 8 | 8 | 3 |
| Two disjoint 4-cycles | 24 | 8 | 8 | 3 |
| 720->12 refinement benchmark | 12 | 12 | 12 | **1** |

These are synthetic structural controls, not runtime guarantees for arbitrary tasks.

## 6. Minimal strict-gain normal form has genuine `S3` query symmetry

The unique minimal strict-gain normal form has canonical cross-target separator structure equivalent to

```text
{001, 010, 100, 111}.
```

Any permutation of the three query columns preserves this row multiset. Therefore

\[
G\cong S_3,
\qquad
|G|=6.
\]

Stable color refinement leaves one three-query class and IR necessarily visits six canonical leaves in the current unpruned implementation. This is not a failure to notice a structural difference: there is no structural difference among the three query identities in the residual fixed-cover incidence.

The automorphism audit gives

\[
N_{\rm distinct}=6/6=1.
\]

This explains why the same minimal strict-gain decision structure appears under every query relabeling.

## 7. Important implementation boundary

The current automorphism module is an **exact audit**, not yet an asymptotically cheaper canonicalizer. It enumerates every stable-color-preserving permutation up to a hard cap and then extracts the subgroup that is a true automorphism group.

Therefore the current pipeline can diagnose how much remaining factorial work is pure automorphism redundancy, but it does not yet obtain the full speedup without doing the enumeration that proves the group complete.

This distinction is deliberate.

## 8. Next exact step: orbit pruning with a stabilizer chain

The natural next improvement is to use independently verified automorphism generators during individualization.

At a search node, let the automorphism subgroup that fixes the already individualized queries act on the selected target cell. Only one representative from each orbit needs to be individualized; other choices lead to isomorphic subproblems.

A safe implementation needs:

1. an exact or certified subgroup of the current stabilizer;
2. explicit proof that skipped queries lie in the same orbit;
3. a canonical representative rule;
4. fail-closed behavior when group certification exceeds its resource cap.

This would turn the automorphism audit from an explanatory receipt into an active search reduction.
