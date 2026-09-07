# LYM bound for the state-resource failure-row kernel

The exact fixed-resolution theorem stores reduced failure rows `(U,P)`, where
`U` is the set of already-consumed queries and `P` is the set of still-productive
queries at one reachable mixed state.

The reduction order is

\[
(U_1,P_1)\le(U_2,P_2)
\iff
U_1\subseteq U_2,\quad P_1\subseteq P_2.
\]

After deleting dominated rows, the retained rows form an antichain.

## Rank structure

For `q` queries, every coordinate is in exactly one of three statuses:

```text
0  = neither consumed nor productive in the row
U  = consumed
P  = productive
```

A rank-`k` row has `k=|U|+|P|` nonzero coordinates. Choose the `k` coordinates,
then choose `U` or `P` independently on each one, so the rank size is

\[
\boxed{N_{q,k}=\binom qk 2^k}.
\]

## LYM inequality

Choose a maximal chain uniformly by:

1. taking a uniformly random ordering of the `q` coordinates;
2. independently assigning each coordinate its final `U/P` label;
3. activating coordinates in that order.

There are `q! 2^q` such chains.

A fixed rank-`k` row lies on

\[
k!(q-k)!2^{q-k}
\]

chains, so its inclusion probability is

\[
\frac{1}{\binom qk 2^k}.
\]

An antichain meets any maximal chain at most once. Therefore

\[
\boxed{
\sum_{r\in A}
\frac{1}{\binom q{k_r}2^{k_r}}
\le1,
\qquad k_r=|U_r|+|P_r|.
}
\]

Consequently

\[
\boxed{
|A|\le\max_{0\le k\le q}\binom qk2^k.
}
\]

This is an exact combinatorial upper bound on the dominance-reduced
state-resource row kernel.

Examples:

```text
q=1: bound 2
q=2: bound 4
q=3: bound 12
q=4: bound 32
q=5: bound 80
q=6: bound 240
```

For the complete `15^3=3,375` arbitrary-partition four-world/three-query
regression, the largest observed reduced kernel has six rows, below the general
bound 12. That observed finite maximum is not claimed as a general theorem.

Implementation: `adaptive_gain/state_resource_bounds.py`.

The result concerns only the deterministic finite fixed-resolution row poset. It
does not imply a comparable bound for stochastic continuation states or
continuous compatible sets.
