# Exact-balanced binary sharp profile at eight worlds

The exact-50/50 balanced-binary subclass is asymptotically unbounded, but its
finite fixed-size extremum differs from the unrestricted binary class.  The
first threshold result showed that eight worlds and five queries admit

\[
(C_A,C_F)=(3,5),\qquad C_F/C_A=5/3.
\]

This note closes the stronger question for **every declared query count `m` at
`n=8`**.

## Theorem

For finite deterministic unit-cost tasks on exactly eight represented worlds,
where every declared query is binary and has exactly four 0 outcomes and four 1
outcomes,

\[
\boxed{
\max \frac{C_F}{C_A}
=
\begin{cases}
1, & m=1,2,\\[4pt]
3/2, & m=3,4,\\[4pt]
5/3, & m\ge5.
\end{cases}
}
\]

The maximum is over arbitrary target partitions and arbitrary exactly-balanced
query vocabularies with the declared number of physical query labels.

## 1. Minimum fixed resolvers are irredundant cut families

A binary query is a bipartition of the represented worlds.  Let `B` be a
minimum-cardinality fixed resolver.  For every `q in B`, the bundle `B\{q}` is
not resolving.  Hence there is an opposite-target world pair that every query
in `B\{q}` treats identically.  Since `B` itself resolves, `q` separates that
pair.

Therefore every query in a minimum fixed resolver owns a **private
cross-target pair** relative to the other queries in the bundle.  Forgetting
target labels can only weaken this requirement: the underlying balanced cuts
must form an irredundant family, meaning every cut separates at least one world
pair separated by no other cut in the family.

Thus

\[
C_F \le \text{maximum size of an irredundant family of balanced cuts}.
\]

## 2. Exact eight-world cut classification

At eight worlds there are

\[
\frac12\binom84=35
\]

distinct exactly-balanced bipartitions modulo swapping binary outcome names.

The validator enumerates every six-cut subset,

\[
\binom{35}{6}=1{,}623{,}160,
\]

and tests whether every member owns a private world pair.  The result is

\[
\boxed{\text{no irredundant six-cut family exists}.}
\]

The registered five-query `(3,5)` witness is itself an irredundant five-cut
family, so the maximum irredundant size is exactly five.

No larger irredundant family can exist either: every subfamily of an
irredundant family is irredundant, because a private pair remains private after
other cuts are deleted.  Consequently,

\[
\boxed{C_F\le5}
\]

for every exactly-balanced eight-world task, regardless of how many physical
query resources are declared.

This is a stronger finite restriction than the unrestricted binary bound
`C_F<=7` at eight worlds.

## 3. Upper bounds by declared query count

### `m=1,2`

If `C_A=1`, flattening the one-step adaptive policy gives `C_F<=1`.  Otherwise
`C_A>=2` and `C_F<=m<=2`.  Hence

\[
C_F/C_A\le1.
\]

### `m=3,4`

If `C_A=1`, again the ratio is one.  If `C_A=2`, a binary depth-two adaptive
tree has at most three internal query occurrences, so flattening gives
`C_F<=3`.  If `C_A>=3`, then `C_F<=m<=4`, giving at most `4/3`.  Therefore

\[
C_F/C_A\le3/2.
\]

### `m>=5`

The balanced-cut theorem gives `C_F<=5`.  For `C_A<=2`, binary flattening gives
ratio at most `3/2`.  For `C_A>=3`,

\[
C_F/C_A\le5/3.
\]

Thus the global upper bound is `5/3`.

## 4. Sharp witnesses

### `m=1,2`: ratio 1

Use four target-0 worlds and four target-1 worlds, and one exactly-balanced
query equal to the target partition.  Then `(C_A,C_F)=(1,1)`.  A duplicate
physical label with identical outcomes pads the construction to `m=2` without
changing either optimum.

### `m=3,4`: ratio 3/2

Take

```text
world:   w0 w1 w2 w3 w4 w5 w6 w7
target:   0  0  1  1  1  0  0  0

q0:       0  0  0  0  1  1  1  1
q1:       1  1  1  0  1  0  0  0
q2:       1  1  0  1  0  1  0  0
```

Every query is exactly 4/4 balanced.  The exact solver gives

\[
(C_A,C_F)=(2,3).
\]

One optimal adaptive policy asks `q1` first.  On one branch `q2` completes
resolution; on the other branch `q0` completes resolution.  All three queries
are fixed-mandatory.  Duplicating any balanced query pads the witness to `m=4`.

### `m>=5`: ratio 5/3

Use the registered eight-world five-query witness from the finite-threshold
classification.  It has

\[
(C_A,C_F)=(3,5)
\]

and all five queries are exactly balanced.  Duplicate physical query labels
pad the declared vocabulary to any `m>5`; duplicates add no new deterministic
information and therefore leave both optima unchanged.

Hence all three upper bounds are attained.

## 5. Consequence for the balanced fixed-size open problem

The full sharp fixed-`(n,m)` formula for exactly-balanced binary queries remains
open, but the first three nontrivial even world counts now have a much sharper
finite picture:

- `n=4`: complete classification gives maximum ratio 1;
- `n=6`: complete classification gives maximum ratio `3/2`;
- `n=8`: the present theorem gives the complete `m`-profile
  `1,1,3/2,3/2,5/3,5/3,...`.

So exact marginal balance has a genuine finite combinatorial effect.  It does
not merely delay the unrestricted extremum by one arbitrary example: at eight
worlds it globally caps every fixed resolver at five essential balanced cuts.

## Reproducibility

Implementation:

- `adaptive_gain/balanced_binary_eight_world_profile.py`
- `tests/test_balanced_binary_eight_world_profile.py`
- `validation/balanced_binary_eight_world_profile.json`

The six-cut cap is a finite exhaustive classification receipt, not a sampling
claim.
