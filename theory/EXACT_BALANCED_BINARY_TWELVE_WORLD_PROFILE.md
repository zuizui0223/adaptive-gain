# Exact-balanced binary sharp profile at twelve worlds

This note closes the fixed-query extremal ratio for exactly-balanced binary
unit-cost tasks on **twelve represented worlds** and identifies the first even
world count at which the full binary depth-three flattening bound is attainable
inside the exact-balanced subclass.

Every declared query has exactly six 0 outcomes and six 1 outcomes.

## Theorem

For every declared query count `m>=1`,

\[
\boxed{
\max \frac{C_F}{C_A}
=
\begin{cases}
1, & m=1,2,\\[4pt]
3/2, & m=3,4,\\[4pt]
5/3, & m=5,\\[4pt]
2, & m=6,\\[4pt]
7/3, & m\ge7.
\end{cases}
}
\]

The maximum is over arbitrary target partitions and exact-6/6 binary query
vocabularies.

## 1. The depth-three bound becomes sharp again

A binary adaptive tree of worst-path depth three has at most

\[
2^3-1=7
\]

internal query occurrences.  Flattening an optimal tree therefore always gives

\[
C_F\le7\qquad(C_A\le3).
\]

At ten worlds exact balance makes the endpoint `(C_A,C_F)=(3,7)` impossible.
At twelve worlds the repository contains an explicit seven-query task with

\[
\boxed{(C_A,C_F)=(3,7)}.
\]

All seven queries are exactly 6/6 balanced.  The general exact solvers verify
both optima directly.

Thus the ten-world obstruction is a genuine finite compatibility effect rather
than a permanent penalty imposed by exact marginal balance.

## 2. Sharpness for every declared query count

For `m=1,2`, the ratio is at most one.

For `m=3,4`, binary depth-two flattening gives `C_F<=3`, hence the ratio is at
most `3/2`; a registered exact-balanced `(2,3)` witness attains it.

For `m=5`, adaptive depth at most two again gives at most `3/2`, while adaptive
depth at least three gives `C_F/C_A<=5/3`; a registered `(3,5)` witness attains
`5/3`.

For `m=6`, the analogous argument gives the upper bound `2`, attained by a
registered `(3,6)` witness.

For `m>=7`, adaptive depth at most three gives

\[
C_F/C_A\le7/3.
\]

If `C_A>=4`, the sharp exact-balanced fixed-cost theorem at twelve worlds gives

\[
C_F\le12-3=9,
\]

so

\[
C_F/C_A\le9/4<7/3.
\]

The registered `(3,7)` witness therefore proves that the global maximum is
exactly `7/3`.  Duplicate physical labels with identical balanced outcome maps
pad the declared vocabulary to arbitrary larger `m` without changing either
optimum.

## 3. First world count for exact-balanced `(3,7)`

The minimum even represented-world count admitting an exact-balanced binary
task with

\[
(C_A,C_F)=(3,7)
\]

is exactly

\[
\boxed{12}.
\]

For smaller even counts:

- `n=4`: the sharp fixed-cost cap is 2;
- `n=6`: it is 3;
- `n=8`: it is 5;
- `n=10`: the fixed-cost cap is 7, but the complete depth-three balance/private-edge compatibility audit proves `C_A=3 => C_F<=6`.

At `n=12`, the explicit `(3,7)` witness closes the lower bound.

## 4. Persistence for every larger even world count

The twelve-world witness can be padded to every even `n>=12` while preserving
both exact balance and `(C_A,C_F)=(3,7)`.

Add represented worlds in pairs.  One new world returns zero on all seven
queries and receives the target of the all-zero adaptive leaf; the other returns
one on all seven queries and receives the target of the all-one leaf.

Each added pair contributes one zero and one one to every query, so global 50/50
balance is preserved.  The same depth-three policy still resolves, while the
original seven private cross-target pairs remain present and keep every fixed
query mandatory.  Hence

\[
\boxed{(C_A,C_F)=(3,7)\text{ is attainable for every even }n\ge12.}
\]

## 5. Finite picture through twelve worlds

The closed rows are now:

- `n=4`: maximum ratio `1`;
- `n=6`: maximum ratio `3/2`;
- `n=8`: `1,1,3/2,3/2,5/3,5/3,...`;
- `n=10`: `1,1,3/2,3/2,5/3,2,2,...`;
- `n=12`: `1,1,3/2,3/2,5/3,2,7/3,7/3,...`.

The next genuinely new compatibility question therefore moves to adaptive depth
four rather than depth three.

## Reproducibility

Implementation:

- `adaptive_gain/balanced_binary_twelve_world_profile.py`
- `tests/test_balanced_binary_twelve_world_profile.py`
- `validation/balanced_binary_twelve_world_profile.json`

The twelve-world witness is checked by the repository's general exact adaptive
and fixed solvers, and the larger-even-world family is checked by direct padding
regressions.
