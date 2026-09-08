# Exact-balanced binary depth-five value at eighteen worlds

Let

\[
D_5(18)=\max\{C_F:C_A\le5\}
\]

for unit-cost binary queries that are globally exact 9/9.

The sharp exact-balanced fixed-cost cap is 15.  A cap-15 minimum resolver has
the canonical star--edge--star normal form.  Any outside query must be one of
the three identity-safe balanced cuts; otherwise 14 queries would already
resolve identity and hence any coarser target partition.

For each of the eight subsets of those safe cuts, inspect every exactly-14-query
subfamily.  Whenever such a subfamily leaves exactly one world pair unresolved,
that pair must be cross-target in any task with `C_F=15`.  The numbers of unique
mandatory pairs are

```text
15, 15, 36, 36, 36, 36, 57, 57
```

for query universes of sizes 15 through 18.  Exact Bellman DP shows that
separating those pairs requires worst-case depth eight in every case.  Hence

\[
D_5(18)\le14.
\]

## A fourteen-query depth-five witness

There is an explicit 14-query exact-9/9 family whose private-pair forest has
component sizes

\[
(1,3,7,7).
\]

The registered private pairs for `q0,...,q13` are

```text
(2,1), (1,3),
(5,4), (5,6), (4,7), (4,9), (7,8), (9,10),
(12,11), (12,13), (11,14), (11,16), (14,15), (16,17).
```

Each pair differs in exactly its registered query, and the target assignment
puts every pair across target classes.  Therefore all fourteen queries are
fixed-mandatory and `C_F=14`.

An explicit adaptive policy has worst-case depth five.  Its terminal blocks are

```text
(0,2,4), (10), (9), (8), (7), (6), (5),
(3), (1,11), (17), (16), (15), (14), (13), (12).
```

Assigning one target to each displayed block gives exact adaptive cost five.
Thus

\[
(C_A,C_F)=(5,14).
\]

Combining construction and upper bound,

\[
\boxed{D_5(18)=14}.
\]

This is the first new recovery beyond the closed depth-four slice: at sixteen
worlds, `D5(16)=D4(16)=12`, while at eighteen worlds the additional adaptive
level raises the fixed-side extremum from 13 to 14.
