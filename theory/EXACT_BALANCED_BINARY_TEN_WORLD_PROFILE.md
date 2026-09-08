# Exact-balanced binary sharp profile at ten worlds

This note closes the fixed-query extremal ratio for exactly-balanced binary
unit-cost tasks on **ten represented worlds**.

Every declared query is required to have exactly five 0 outcomes and five 1
outcomes.

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
2, & m\ge6.
\end{cases}
}
\]

The maximum is over arbitrary target partitions and arbitrary exact-5/5 binary
query vocabularies.

The new point is that the two individually sharp upper bounds

\[
C_F\le7
\]

and

\[
C_F\le 2^3-1=7\qquad(C_A=3)
\]

cannot be saturated simultaneously under exact balance.

## 1. Why `C_A=3, C_F=7` would force one canonical tree

Assume for contradiction that a ten-world exact-balanced task has

\[
C_A=3,\qquad C_F=7.
\]

Take an optimal adaptive binary tree.  A depth-three binary tree has at most
seven internal occurrences.  Flattening the distinct query identities appearing
in the tree gives a fixed resolver.  Since the fixed optimum is seven, the tree
must therefore have

- exactly seven internal occurrences;
- exactly seven distinct query identities; and
- all eight terminal leaves nonempty.

After relabeling queries, write the complete tree as

```text
                 q0
             /        \
           q1          q2
         /   \        /   \
       q3     q4    q5     q6
```

Because `q0` is globally 5/5 balanced, exactly five represented worlds lie in
each root half.  Each half contains four nonempty leaves, so each side has leaf
multiplicities `(2,1,1,1)` in some order.

## 2. Fixed minimality forces private Hamming edges

The seven flattened queries form a minimum fixed resolver.  Therefore each
query owns a private opposite-target pair: a pair separated by that query and by
none of the other six.

In the canonical tree this implies, after deleting the fixed root bit from the
code vectors,

- the left five-world half contains a cross-leaf Hamming edge in each of
  `q1,q3,q4`;
- the right five-world half contains a cross-leaf Hamming edge in each of
  `q2,q5,q6`.

The `q3` and `q4` private edges already touch all four left leaves; similarly
`q5` and `q6` touch all four right leaves.  Choosing one required edge in each
of the three local dimensions therefore gives an endpoint union of size at
least four.  Since only five worlds exist on that side, the union has size only
four or five.

Thus the complete local state space can be enumerated without searching raw
five-world multisets:

1. choose one required local Hamming edge in each of the three dimensions;
2. reject endpoint unions larger than five;
3. if four distinct endpoint signatures remain, add one arbitrary extra world,
   allowing either a duplicate signature or a new signature;
4. record only the six non-root coordinate counts.

This finite reduction is exact.

## 3. Exhaustive half-state result

The left and right scans each produce exactly

\[
2944
\]

distinct six-coordinate count vectors.

Global exact balance of `q1,...,q6` would require a left vector

\[
(a_1,\ldots,a_6)
\]

and a right vector

\[
(5-a_1,\ldots,5-a_6).
\]

The exhaustive comparison finds

\[
\boxed{0}
\]

such complementary pairs.

Therefore `C_A=3, C_F=7` is impossible.  Notice that this contradiction occurs
**before** imposing the private-pair condition for the root query `q0`; the six
non-root balance equations already fail.

Hence every exact-balanced ten-world task with `C_A=3` satisfies

\[
\boxed{C_F\le6}.
\]

## 4. Sharp witnesses

The repository registers exact-5/5 witnesses with

\[
(C_A,C_F)=(2,3),\qquad(3,5),\qquad(3,6).
\]

The `(3,6)` witness proves that the new depth-three cap is sharp.

Duplicate physical query labels with identical balanced outcome maps may pad a
witness to larger declared `m` without changing either optimum.

## 5. Deriving the full `m` profile

### `m=1,2`

The ratio is at most one and is attained by a single target-separating balanced
query, with a duplicate label used for `m=2`.

### `m=3,4`

If `C_A=2`, a binary depth-two tree contains at most three internal query
occurrences, so flattening gives `C_F<=3`.  Larger adaptive depth only decreases
the ratio.  Therefore the maximum is `3/2`, attained by the registered `(2,3)`
witness.

### `m=5`

For `C_A<=2`, the ratio is at most `3/2`.  For `C_A>=3`, `C_F<=5`, hence

\[
C_F/C_A\le5/3.
\]

The registered `(3,5)` witness attains equality.

### `m>=6`

- `C_A<=2` gives ratio at most `3/2`;
- `C_A=3` gives `C_F<=6` by the obstruction above, hence ratio at most `2`;
- `C_A>=4` gives `C_F<=7` from the sharp exact-balanced fixed-cost theorem,
  hence ratio at most `7/4`.

Thus the global maximum is exactly `2`, attained by the registered `(3,6)`
witness and padded to arbitrary larger `m`.

## 6. Consequence

The first even world counts now have closed finite behavior:

- `n=4`: maximum ratio `1`;
- `n=6`: maximum ratio `3/2`;
- `n=8`: profile `1,1,3/2,3/2,5/3,5/3,...`;
- `n=10`: profile `1,1,3/2,3/2,5/3,2,2,...`.

The ten-world result shows that the balanced fixed-size theory is not obtained
merely by inserting the global cap `C_F<=n-3` into the ordinary binary tree
bound.  At depth three there is an additional compatibility constraint between
private-edge geometry and exact marginal balance.

## Reproducibility

Implementation:

- `adaptive_gain/balanced_binary_ten_world_profile.py`
- `tests/test_balanced_binary_ten_world_profile.py`
- `validation/balanced_binary_ten_world_profile.json`

The `2,944 + 2,944` half-state calculation is exhaustive, symmetry-normalized by
the canonical complete depth-three tree, and does not use random sampling.
