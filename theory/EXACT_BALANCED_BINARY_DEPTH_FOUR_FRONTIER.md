# Exact-balanced binary depth-four constructive frontier

We now move one adaptive level beyond the closed depth-three envelope.  Queries
remain binary, unit cost, and **globally exact 50/50** on the represented worlds.

Define

\[
D_4(n)=\max\{C_F:\ C_A\le 4\}
\]

inside this exact-balanced subclass.  The universal binary flattening bound and
the sharp exact-balanced fixed-cost cap give

\[
D_4(n)\le \min\{15,n-3\}\qquad(n\ge6\text{ even}).
\]

This note records the first constructive points.  It does **not** yet claim the
sharp value of `D_4(n)`.

## 1. Twelve worlds: `(C_A,C_F)=(4,8)`

There are 12 represented worlds and 8 queries.  Writing each world as its
8-query binary signature gives

```text
w0   00010111
w1   00101000
w2   00101001
w3   00111000
w4   01010111
w5   01011111
w6   10101000
w7   10101010
w8   11000110
w9   11010001
w10  11010101
w11  11100110
```

Every column contains exactly six zeroes and six ones.

A depth-four policy is obtained from the complete depth-three routing

```text
q0
├─0: q1
│   ├─0: q3
│   └─1: q4
└─1: q2
    ├─0: q5
    └─1: q6
```

and then querying `q7` at the fourth level.  Assigning one target to each
terminal `(depth-three leaf, q7 outcome)` cell gives the target vector

```text
(3,0,1,2,4,5,9,10,7,6,8,10).
```

Hence `C_A<=4`.

For queries `q0,...,q7`, respectively, use the pairs

```text
(w1,w6), (w0,w4), (w8,w11), (w1,w3),
(w4,w5), (w9,w10), (w6,w7), (w1,w2).
```

Pair `i` differs in query `q_i` and in no other registered query, and its two
worlds have different targets.  Therefore every query is mandatory in every
fixed resolver and `C_F=8`.

Because a binary adaptive tree of depth at most three flattens to at most seven
distinct queries, `C_F=8` forces `C_A>=4`.  Thus

\[
\boxed{(C_A,C_F)=(4,8)}.
\]

## 2. Fourteen worlds: `(C_A,C_F)=(4,10)`

A stronger 14-world witness has ten exact-7/7 queries.  Its world signatures are

```text
w0   0001011101
w1   0010100010
w2   0010100110
w3   0011100010
w4   0101011101
w5   0101111101
w6   1010100010
w7   1010101010
w8   1100011001
w9   1101000100
w10  1101010100
w11  1110011001
w12  0101011111
w13  1010100011
```

Each of the ten columns has exactly seven zeroes and seven ones.

One explicit depth-four private-edge-separating policy is

```text
q0
├─0: q1
│   ├─0: q3
│   │   ├─0: q7
│   │   └─1: stop
│   └─1: q4
│       ├─0: q8
│       └─1: stop
└─1: q1
    ├─0: q6
    │   ├─0: q9
    │   └─1: stop
    └─1: q2
        ├─0: q5
        └─1: stop
```

The corresponding terminal target vector is

```text
(2,0,1,2,3,5,6,8,10,9,10,11,4,7).
```

The registered private pairs for `q0,...,q9` are

```text
(w1,w6), (w0,w4), (w8,w11), (w1,w3), (w4,w5),
(w9,w10), (w6,w7), (w1,w2), (w4,w12), (w6,w13).
```

Again, pair `i` differs only in `q_i` and is cross-target.  Thus all ten queries
are fixed-mandatory, while the displayed policy resolves the targets in depth
four.  Since ten is greater than the depth-three flattening cap seven,

\[
\boxed{(C_A,C_F)=(4,10)}.
\]

## 3. Current frontier

The certified constructive lower bounds are now

\[
\boxed{D_4(12)\ge8,\qquad D_4(14)\ge10.}
\]

The generic upper bounds at those sizes are 9 and 11, respectively.  Therefore
the remaining sharp questions are only one query wide:

```text
n=12:  D4(12) is 8 or 9
n=14:  D4(14) is 10 or 11
```

The next useful validation is to decide whether the `n-3` fixed-cost cap can be
made compatible with adaptive depth four at either size, allowing arbitrary
additional exact-balanced queries.  After that, continue with `n=16` and the
full-tree ceiling `C_F<=15`.
