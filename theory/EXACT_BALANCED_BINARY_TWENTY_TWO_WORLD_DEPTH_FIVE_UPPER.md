# Exact-balanced binary depth-five sharp value at 22 worlds

Define

\[
D_5(22)=\max\{C_F:C_A\le5\}
\]

for unit-cost binary queries that are globally exact 11/11 on the represented worlds.  The explicit construction already gives

\[
D_5(22)\ge17.
\]

This note closes the upper side.

## 1. `C_F=19` is impossible

The exact-balanced fixed-cost cap is `n-3=19`.  Let `U` be the distinct labels in a resolving depth-five tree.  Flattening makes `U` a fixed resolver.  If the original task had `C_F=19`, the restricted task on `U` also has fixed minimum exactly 19 and therefore contains a cap-saturating minimum resolver `B19`.

Up to world relabelling and outcome complementation, `B19` is the star--edge--star normal form.  It identifies all 22 worlds.  Any extra tree query must therefore be identity-safe: otherwise `B19+r` would contain an 18-query identity resolver and hence an 18-query resolver for the original targets.

There are

\[
\binom{21}{10}=352716
\]

exact 11/11 cut classes modulo outcome complementation.  Exhaustion leaves exactly **three** identity-safe external cuts.  All eight subsets of those three were checked by exact depth-five mandatory-pair DP.  None is feasible.  Hence `C_F=19` is impossible when `C_A<=5`.

## 2. Classifying every minimum `B18`

Suppose instead `C_F=18`.  The query set of a depth-five tree has restricted fixed minimum 18: it cannot be 19 by the preceding result.  Therefore it contains a minimum 18-query resolver `B18`.

Choose one private cross-target pair for each query of `B18`.  Their graph is a forest on 22 vertices with 18 edges and hence four components.  Exact 11/11 balance leaves eight component-size types:

```text
(1,1,10,10)
(1,2,9,10)
(1,3,9,9)
(2,2,8,10)
(2,3,7,10)
(2,4,6,10)
(2,5,5,10)
(5,5,5,7)
```

There are **60** compatible non-isomorphic forest forms.  Exhausting every balanced private cut gives exactly **4,742** normalized `B18` matrices.  None can separate its 18 registered private edges in depth five using only `B18`; thus every hypothetical `(5,18)` task must use external queries essentially.

The 4,742 matrices split into

```text
4,725 identifying B18 matrices
   17 one-collision B18 matrices.
```

## 3. Identifying `B18`: basis exchange is impossible

For an identifying `B18`, an external query is individually safe only if `B18+r` still has fixed minimum at least 18.  Allowing **all** individually safe external cuts is a relaxation of the real problem.

Across all 4,725 identifying matrices, only **96** relaxed supersets admit any depth-five identity tree.  For each survivor, two external queries that together allow a 17-query identity resolver are declared a forbidden pair.  Root-level pairwise-safety leaves only **22** matrices.

For each of those 22 matrices, the forbidden graph on safe external queries was completed and all maximal pairwise-safe external sets were enumerated.  A truly fixed-18 query family must use an external set contained in one of those maximal pairwise-safe sets.  Yet even when every query in a maximal set is made available, exact depth-five identity resolution is impossible.

Therefore all 4,725 identifying `B18` cases are excluded.

## 4. The 17 collision matrices

The remaining 17 matrices have exactly one pair of worlds with the same `B18` signature.  Because `B18` is a resolver, those two worlds are forced to share target.

They form only two isomorphism classes.

The first class contains a single `(1,1,10,10)` matrix.  It has only **12** external cuts that are individually fixed-safe after the same-target collision is taken into account.  Even the full 12-query relaxation is depth-five infeasible.

The other **16** matrices are mutually isomorphic under world relabelling together with query permutation/outcome complementation, so one representative suffices.  In that representative there are **87,519** individually target-safe external cuts.

The automorphism group of the representative partitions those cuts into only **37 orbits**.  Five orbit representatives are universal: each is pairwise compatible with every safe external cut.  `B18` plus all five universal cuts is still depth-five infeasible.

For each of the remaining **32 orbit representatives** `r`, restrict the external universe to queries pairwise fixed-safe with `r`.  There are at most 149 such queries.  Complete the compatibility graph, enumerate every maximal pairwise-safe clique, and give the adaptive policy the entire clique.  This is again a relaxation: any genuine fixed-18 external family containing `r` is a subset of one of these cliques.

Across the 32 representatives the audit checked

```text
25,512 maximal pairwise-safe cliques
0 depth-five target-resolution survivors.
```

Hence the collision cases are also impossible.

## 5. Sharp conclusion

Both `C_F=19` and `C_F=18` are impossible for adaptive depth at most five.  The explicit 22-world witness has `(C_A,C_F)=(5,17)`.  Therefore

\[
\boxed{D_5(22)=17}.
\]

The next finite-size problem is `D_5(24)`, with generic upper bound `21` from `C_F<=n-3` and current constructive lower bound at least 17 by complementary-pair padding.
