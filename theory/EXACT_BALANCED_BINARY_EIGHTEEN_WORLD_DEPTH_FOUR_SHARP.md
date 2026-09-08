# Exact-balanced binary depth-four sharp value at eighteen worlds

Define

\[
D_4(n)=\max\{C_F:C_A\le4\}
\]

for unit-cost binary queries that are globally exact 50/50 on the represented
worlds. The explicit 18-world lower witness gives

\[
D_4(18)\ge13.
\]

This note closes the remaining one-query gap with the corrected exhaustive
classification.

## 1. Why a hypothetical `C_F=14` reduces to `B14 + r`

Let `T` be a resolving adaptive tree of depth at most four and let `U` be the
set of distinct query labels occurring in `T`. Flattening gives a fixed
resolver, hence

\[
14=C_F\le |U|\le15.
\]

If `|U|=14`, set `B=U`. Suppose `|U|=15`. The fixed minimum of the task
restricted to `U` cannot be 15: if all 15 exact-balanced queries in `U` were
fixed-mandatory, then 15=`18-3` saturates the exact-balanced fixed-cost cap, and
the cap-saturation theorem forces adaptive depth

\[
18/2-1=8,
\]

contradicting the depth-four tree `T`, which uses only `U`. Therefore the
restricted fixed minimum inside `U` is 14. Thus `U` contains a minimum
14-query resolver `B`, with at most one extra query `r`.

So every hypothetical `(C_A,C_F)=(4,14)` task reduces universally to a
`B14+r` case.

## 2. Exhaust all possible minimum bundles `B`

Choose one private cross-target pair for each query of the minimum resolver
`B`. The private-pair graph is a forest. With 18 vertices and 14 edges it has
four components.

There are 47 unordered positive four-part partitions of 18. For every tree
component, consider a leaf edge. Its private query must place either the single
leaf side or the complementary `s-1` side together with whole other forest
components to total exactly nine worlds. This leaf-edge 9/9 condition alone
reduces the 47 partitions to exactly six possibilities:

```text
(1,1,8,8)
(1,2,7,8)
(2,2,6,8)
(2,3,5,8)
(2,4,4,8)
(4,4,4,6)
```

Hence every component has size at most eight. All non-isomorphic component
trees can therefore be generated exhaustively with a small finite tree
catalog. For each private edge, removing that edge gives five components; an
exact-balanced private query is a union of these pieces of total size nine,
with the two edge endpoints on opposite sides.

Enumerating all non-isomorphic forests and every admissible balanced private
cut choice gives the corrected count

```text
balanced minimum-bundle configurations B: 1,222
```

After quotienting outcome complementation:

```text
B identifying all 18 worlds: 1,207
B with exactly one two-world signature collision: 15
```

The earlier intermediate count `1,246` was an overcount and is superseded by
this corrected enumeration.

## 3. Add the only possible extra tree query `r`

There are

\[
\frac12\binom{18}{9}=24,310
\]

exact-balanced cut classes modulo outcome complementation.

For a 15-query family `B+r`, `C_F\ge14` requires every 13-query subfamily to
fail. In particular, for each pair of omitted B queries, there must exist a
cross-target world pair not separated by the remaining twelve B queries plus
`r`. When such an omission condition has only one possible witness pair, that
pair is mandatory for every adaptive policy, in addition to the fourteen
registered private edges.

### Identifying `B`

Across all 1,207 identifying bundles:

```text
(B,r) pairs retaining the fixed-14 omission condition: 65,864
pairs also able to separate all 14 registered private edges in depth 4: 134
pairs still depth-4 feasible after adding all singleton omission witnesses: 0
```

Thus no identifying bundle supports `(C_A,C_F)=(4,14)`.

### The 15 collision bundles

In each collision bundle the unique equal-B-signature world pair is forced to
share target and therefore cannot serve as a cross-target omission witness.
Recomputing the same necessary conditions with that pair excluded gives

```text
fixed-14-safe (B,r) pairs: 84,326
private-edge depth-four pairs: 21,448
pairs surviving singleton-witness depth-four feasibility: 0
```

Thus the collision branch is also empty.

## 4. Sharp conclusion

No normalized `B14+r` case survives, so

\[
D_4(18)\le13.
\]

The explicit 13-query construction has `(C_A,C_F)=(4,13)`, hence

\[
\boxed{D_4(18)=13}.
\]

Together with the previously closed values and the complete 20-world tree,

```text
n=12: D4=8
n=14: D4=10
n=16: D4=12
n=18: D4=13
n>=20 even: D4=15
```

so the exact-balanced adaptive-depth-four slice is closed through the
transition to the universal 15-query flattening ceiling.
