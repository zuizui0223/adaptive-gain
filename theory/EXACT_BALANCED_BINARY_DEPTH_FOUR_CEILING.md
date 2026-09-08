# Exact-balanced binary depth-four ceiling

Let

\[
D_4(n)=\max\{C_F:\ C_A\le4\}
\]

for unit-cost binary queries that are globally exact 50/50 on an even number
`n` of represented worlds.

A binary tree of worst-case depth four has at most fifteen internal query
occurrences. Flattening an adaptive tree therefore gives the universal upper
bound

\[
D_4(n)\le15.
\]

## Twenty worlds attain the ceiling

There is an explicit exact-10/10 task on 20 worlds with fifteen queries and

\[
\boxed{(C_A,C_F)=(4,15)}.
\]

The world signatures are

```text
w0   111111111111111
w1   111110001000101
w2   011110001000101
w3   000110001001010
w4   010110001001010
w5   001110001001010
w6   011110000110100
w7   011010000110100
w8   011010100110100
w9   011100000110100
w10  011100010110100
w11  011111000110100
w12  100001110001011
w13  100001111001011
w14  100001111011011
w15  100001111010011
w16  100001111010111
w17  100001110101011
w18  100001110101001
w19  100001110101000
```

Every column has ten zeroes and ten ones. For `q0,...,q14`, respectively, the
registered private pairs are

```text
(1,2), (3,4), (3,5), (6,7), (6,9),
(6,11), (7,8), (9,10), (12,13), (12,17),
(13,14), (14,15), (15,16), (17,18), (18,19).
```

Pair `i` differs only in `q_i` and is cross-target, so all fifteen queries are
mandatory in every fixed resolver. The private-pair forest has component sizes

\[
(1,2,3,6,8).
\]

A complete depth-four adaptive policy uses all fifteen labels exactly once:

```text
q10
├─1: q3
│   ├─1: q4
│   │   ├─1: q5      -> (w0,w11) / w6
│   │   └─0: q7      -> w10 / w9
│   └─0: q12
│       ├─1: q6      -> (w8,w16) / w7
│       └─0: q11     -> w14 / w15
└─0: q8
    ├─1: q1
    │   ├─1: q0      -> w1 / (w2,w4)
    │   └─0: q2      -> w5 / (w3,w13)
    └─0: q13
        ├─1: q9      -> w17 / w12
        └─0: q14     -> w18 / w19
```

The terminal target vector is

```text
(0,8,9,11,9,10,1,5,4,3,2,0,13,11,6,7,4,12,14,15).
```

Thus `C_A<=4`, while private pairs give `C_F>=15`; flattening gives the
opposite inequalities, hence equality.

## Every even n >= 20 also attains 15

Append one all-zero and one all-one world. Each existing query gains one zero
and one one, so exact balance is preserved. Assign the all-zero world to the
terminal target of `w19` and the all-one world to the terminal target of
`(w0,w11)`. The same complete depth-four policy still resolves the task and all
original private pairs remain present. Repeating the operation yields

\[
\boxed{D_4(n)=15\quad\text{for every even }n\ge20.}
\]

## Eighteen worlds: the last finite gap is closed

The 18-world lower witness gives `(C_A,C_F)=(4,13)`.  A separate exhaustive
classification now rules out `C_F=14` at adaptive depth four, so

\[
\boxed{D_4(18)=13}.
\]

The key reduction is internal to the adaptive tree, not an assumption about an
arbitrary global minimum bundle.  If a hypothetical depth-four task had
`C_F=14`, let `U` be the distinct query labels used by a resolving depth-four
tree.  Then `14<=|U|<=15`.  If `|U|=15` and the restricted fixed minimum inside
`U` were 15, those fifteen exact-balanced queries would form an `n-3`
cap-saturating family and the cap-saturation theorem would force adaptive depth
8 inside `U`, contradicting the displayed depth-four tree.  Hence `U` itself
contains a minimum 14-query resolver `B`, with at most one extra tree query
`r`.  Exhausting all such `B+r` cases gives no survivor; see
`EXACT_BALANCED_BINARY_EIGHTEEN_WORLD_DEPTH_FOUR_SHARP.md`.

## Certified depth-four frontier near the ceiling

```text
n=12: D4=8
n=14: D4=10
n=16: D4=12
n=18: D4=13
n>=20 even: D4=15
```

Thus the finite transition into the universal 15-query flattening ceiling is
closed through eighteen worlds.
