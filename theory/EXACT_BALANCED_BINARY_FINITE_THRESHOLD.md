# Exact-balanced binary finite threshold

The asymptotic exactly-balanced family proves that global 50/50 marginal query balance does **not** uniformly bound adaptive advantage.  The finite-size question is subtler: exact balance can still lower the sharp ratio at small `(n,m)`.

This note records the first complete finite threshold.

## Result

For deterministic unit-cost binary observations in which every declared query has exactly half 0 outcomes and half 1 outcomes over the represented worlds:

\[
\boxed{
 n<8 \Longrightarrow C_F/C_A\le 3/2,
}
\]

while there is an 8-world, 5-query task with

\[
\boxed{(C_A,C_F)=(3,5),\qquad C_F/C_A=5/3.}
\]

Thus the smallest world count at which exact global 50/50 balance permits a ratio strictly above `3/2` is **8**, and the smallest query count is **5**.

This differs from the unrestricted binary class, where the first fixed-`(n,m)` scope above `3/2` already occurs at six worlds and five queries.

## Complete n=4 and n=6 scans

Outcome complementation of one binary query does not change deterministic exact-resolution costs, so each balanced bipartition is represented once by fixing world 0 to outcome 0.

For `n=4` this leaves 3 balanced partition classes.  Across all 4 nontrivial target multiplicity profiles and all nonempty query-family subsets, there are 28 symmetry-reduced representatives.  Their maximum ratio is

\[
\boxed{1}.
\]

For `n=6` there are

\[
\frac12\binom{6}{3}=10
\]

balanced partition classes and 10 nontrivial target multiplicity profiles.  Enumerating every nonempty subset gives

\[
10(2^{10}-1)=10{,}230
\]

symmetry-reduced representatives.  Of these, 9,184 are resolvable by their declared vocabulary.  The exact maximum is

\[
\boxed{3/2},
\]

attained, among other cases, at `(C_A,C_F)=(2,3)`.

Duplicate physical query labels with identical deterministic outcomes cannot improve either optimum; they only pad the declared query count.  Therefore the complete subset scan covers arbitrary query multiplicity for the extremal ratio.

## Eight-world witness

Take target labels

```text
world:   w0 w1 w2 w3 w4 w5 w6 w7
target:   0  0  0  0  1  1  1  1
```

and five unit-cost queries

```text
q0: 0 1 1 0 0 0 1 1
q1: 0 1 0 0 0 1 1 1
q2: 0 1 0 1 0 1 1 0
q3: 0 1 1 0 0 1 0 1
q4: 0 0 1 1 1 0 0 1
```

Every row has exactly four 0s and four 1s.

The general exact solver gives

\[
C_A=3,
\qquad
C_F=5.
\]

The fixed lower bound also has a direct private-pair certificate: each query is the unique separator of one cross-target pair,

```text
q0 : (w1,w5)
q1 : (w2,w7)
q2 : (w3,w4)
q3 : (w1,w6)
q4 : (w0,w4)
```

so every fixed resolver must contain all five queries.  A depth-three adaptive tree exists, hence `C_A<=3`; the universal flattening bound rules out `C_A<=2` because a binary depth-two tree contains at most three internal query occurrences while `C_F=5`.  Therefore `C_A=3` exactly.

## Why five queries are minimal

For any binary deterministic task with at most four declared queries:

- if `C_A=1`, flattening gives `C_F<=1`;
- if `C_A=2`, a binary depth-two tree has at most three internal nodes, so `C_F<=3`;
- if `C_A>=3`, then `C_F<=4`, so `C_F/C_A<=4/3`.

Hence no binary task with `m<=4` can exceed `3/2`, balanced or otherwise.

## Interpretation

Exact marginal balance is therefore neither completely irrelevant nor a uniform regularizer.  It has a genuine **finite-size penalty**—the six-world binary extremum `5/3` is suppressed to `3/2`—but that penalty disappears already by eight worlds for the five-query threshold.

The remaining open problem is still the full sharp fixed-`(n,m)` formula inside the exact-balanced binary subclass.  The present result closes only the first nontrivial threshold and supplies a complete small-world audit.

## Reproducibility

Implementation:

- `adaptive_gain/balanced_binary_small_scope.py`
- `tests/test_balanced_binary_small_scope.py`
- `validation/balanced_binary_small_scope.json`
