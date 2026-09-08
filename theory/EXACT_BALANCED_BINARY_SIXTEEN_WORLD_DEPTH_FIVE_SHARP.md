# Exact-balanced binary depth-five value at sixteen worlds

Let

\[
D_5(16)=\max\{C_F:C_A\le5\}
\]

for unit-cost binary queries that are globally exact 8/8 on sixteen represented
worlds.

The existing 12-query construction has `(C_A,C_F)=(4,12)`, so

\[
D_5(16)\ge12.
\]

The universal exact-balanced fixed-cost cap is 13.  The question is whether one
extra adaptive level can recover that cap.

## Cap normalization and the only allowed external cuts

If `C_F=13`, a minimum fixed resolver has the sharp `n-3` normal form.  Up to
world relabelling and outcome complementation, its thirteen balanced queries
are the canonical star--edge--star cap bundle.

An outside balanced query must be identity-safe.  Otherwise that query plus 11
members of the cap bundle would resolve the sixteen identity targets with only
12 queries, and therefore also resolve every coarser target partition with at
most 12 queries, contradicting `C_F=13`.

At sixteen worlds there are exactly three identity-safe external balanced cuts.
Hence every hypothetical cap-13 task lies inside one of the eight query
universes obtained by adjoining a subset of those three cuts.

## Unique-witness obstruction

Fix one such query universe `Q`.  If the target fixed minimum is at least 13,
then every exactly-12-query subfamily must fail.  Whenever a 12-query subfamily
leaves exactly one world pair unresolved, that pair must be cross-target.
Therefore every adaptive policy must separate all world pairs that are unique
witnesses for at least one 12-query failure.

Across the eight safe-cut subsets, the query-universe sizes are

```text
13, 14, 14, 15, 14, 15, 15, 16
```

and the numbers of exactly-12-query subfamilies are

```text
13, 91, 91, 455, 91, 455, 455, 1820.
```

After deduplicating their unique unresolved pairs, the mandatory-pair counts are

```text
13, 13, 28, 28, 28, 28, 43, 43.
```

Exact Bellman DP on each query universe gives the same minimum worst-case depth
for separating those mandatory pairs:

```text
7, 7, 7, 7, 7, 7, 7, 7.
```

Thus any target partition retaining fixed cost 13 already requires adaptive
depth at least seven.  In particular it cannot have `C_A<=5`.

Therefore

\[
D_5(16)\le12.
\]

Together with the existing `(4,12)` witness,

\[
\boxed{D_5(16)=12}.
\]

So the first extra adaptive level beyond the closed depth-four frontier does
**not** improve the sixteen-world extremum.  The next informative point is
`n=18`, where depth four gives 13 and the fixed cap is 15.
