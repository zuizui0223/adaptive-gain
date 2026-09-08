# Exact-balanced binary depth four on eighteen worlds

Let

\[
D_4(n)=\max\{C_F: C_A\le4\}
\]

inside the unit-cost binary subclass in which every declared query is globally
exact 50/50 on the represented worlds.

The previous sharp values are

\[
D_4(12)=8,\qquad D_4(14)=10,\qquad D_4(16)=12.
\]

At eighteen worlds the generic bounds give

\[
D_4(18)\le \min\{15,18-3\}=15.
\]

The saturated value 15 is impossible at adaptive depth four: a 15-query
minimum fixed resolver is an `n-3` cap-saturating bundle, whose exact-balanced
star--edge--star normal form requires adaptive depth `18/2-1=8` when those 15
queries themselves are the declared family.  Thus the live question is 13
versus 14.

## Explicit `(C_A,C_F)=(4,13)` witness

A thirteen-query witness has private-pair forest component sizes

```text
(3,3,4,4,4)
```

with edges

```text
(0,2), (1,2),
(3,4), (4,5),
(7,6), (6,9), (8,9),
(10,12), (12,11), (11,13),
(15,16), (16,14), (14,17).
```

The one-sides of queries `q0,...,q12` are

```text
0:  0 6 7 8 9 10 11 12 13
1:  0 2 3 4 5 6 7 8 9
2:  0 1 2 4 5 6 7 8 9
3:  0 1 2 3 4 6 7 8 9
4:  0 1 2 3 4 5 6 8 9
5:  0 1 2 6 7 10 11 12 13
6:  0 1 2 3 4 5 6 7 9
7:  0 1 2 3 4 5 11 12 13
8:  0 1 2 6 7 8 9 10 12
9:  0 1 2 3 4 5 10 11 12
10: 0 1 2 3 4 5 14 16 17
11: 0 1 2 6 7 8 9 15 16
12: 0 1 2 3 4 5 14 15 16
```

Every row has exactly nine worlds.  Private pair `i` differs only in `q_i`, so
all thirteen queries are fixed-mandatory.  The target vector is

```text
(0,1,2,3,2,4,0,5,6,7,8,9,10,11,12,13,1,14).
```

One depth-four policy is

```text
q0
├─1: q1
│   ├─1: q5
│   │   ├─1: q4
│   │   └─0: q6
│   └─0: q8
│       ├─1: q7
│       └─0: q9
└─0: q1
    ├─1: q2
    │   ├─1: q3
    │   └─0: stop
    └─0: q11
        ├─1: q10
        └─0: q12
```

Hence `C_A<=4`.  Since a binary depth-three tree has at most seven internal
query occurrences, `C_F=13` rules out `C_A<=3`.  Therefore the cost pair is
exactly

\[
\boxed{(C_A,C_F)=(4,13)}.
\]

Consequently

\[
\boxed{13\le D_4(18)\le14}.
\]

## What has already been excluded for `C_F=14`

If a minimum fourteen-query fixed resolver `B` is certified by one Hamming-1
private pair per query, the private-pair graph has four components.  Exact
balance leaves only seven possible component-size types and 35 non-isomorphic
forest shapes.  Optimizing the balanced cut choice on every one of those 35
forests gives minimum private-edge separation depth at least five.

Allowing one additional exact-balanced query that crosses zero or one of the
registered private edges still gives no depth-four construction after complete
enumeration of the corresponding cut choices.  A second attempted normal form,
with eleven singleton obstructions plus a four-query `K4` of distance-two
obstructions, also bottoms out at depth five.

These exclusions are strong but do not yet constitute a universal proof that
`D_4(18)=13`: a genuine fourteen-cost task could use a minimum resolver whose
private pairs are helped by several external queries in a more complicated
replacement pattern.  The remaining validation therefore searches directly
at the target-partition / fixed-hitting-set level rather than assuming global
private edges in the full declared query family.
