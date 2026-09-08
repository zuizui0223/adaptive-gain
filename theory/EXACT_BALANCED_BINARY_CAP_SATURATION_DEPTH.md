# Exact-balanced cap saturation forces a star--edge--star spine

Let `n=2h>=8` be even.  Consider an exact-50/50 binary task whose **entire
declared query family** has `n-3` queries and whose fixed optimum is

\[
C_F=n-3.
\]

Thus every declared query is fixed-mandatory.

## 1. Private-pair forest

Choose one private cross-target pair for every query.  As in the fixed-cost cap
proof, the selected pairs form a forest `G`: query `q` crosses its own selected
edge and no other selected edge.  Since `G` has `n` vertices and `n-3` edges,
it has exactly three connected components.

Write their sizes as `a<=b<=c`.

For a leaf edge in any nontrivial component of size `s`, deleting that edge
leaves a singleton, a connected block of size `s-1`, and the other two intact
components.  A query crossing only this forest edge must still make an exact
`h/h` cut.  Equivalently, some subset of the **other two component sizes** must
sum to `h-1`.

Applying that condition to every nontrivial component rules out isolated
components for `h>=4` and forces

\[
\{a,b,c\}=\{2,h-1,h-1\}.
\]

Now consider an arbitrary edge inside an `(h-1)` component.  If it splits that
component into sizes `r` and `h-1-r`, the other intact component sizes are
`2` and `h-1`.  Exact balance is possible only for `r=1` or `r=h-2`.
Therefore **every edge is a leaf edge**, so each `(h-1)` component is a star.

Hence the saturated private-pair forest has the unique normal form

```text
(h-1)-vertex star  --  2-vertex edge  --  (h-1)-vertex star
```

(up to relabeling; the three components are disconnected in the forest).

## 2. Adaptive lower bound inside the saturated bundle

Each star has `h-2` private leaf edges.  Let `l` left-star queries and `r`
right-star queries be asked before the middle-edge query along the branch that
still contains both middle endpoints.  After the middle query, one branch must
still separate the remaining `h-2-l` left-star private edges and the other must
separate the remaining `h-2-r` right-star private edges.

Thus the worst depth is at least

\[
l+r+1+\max\{h-2-l,h-2-r\}
\ge h-1.
\]

The bound is attained by asking the middle-edge query first, then processing the
left-star leaf queries sequentially on one branch and the right-star leaf
queries sequentially on the other.  Therefore

\[
\boxed{C_A\ge h-1=n/2-1}
\]

for every task whose declared family is exactly such a saturated `n-3` bundle.
The repository includes a target assignment attaining equality, so

\[
\boxed{(C_A,C_F)=(n/2-1,n-3)}.
\]

Concrete instances are

```text
n=8   -> (3,5)
n=10  -> (4,7)
n=12  -> (5,9)
n=14  -> (6,11)
```

## 3. Why this does not yet close `D_4(n)`

The theorem is deliberately bundle-local.  If the declared family contains
additional exact-balanced queries outside a chosen minimum fixed resolver, an
adaptive policy may use those extra queries.  A private pair relative to the
minimum bundle need not remain private relative to the whole declared family.

Therefore the remaining depth-four question is genuinely stronger:

> can extra exact-balanced queries lower the adaptive cost to four while the
> global fixed optimum remains `n-3`?

The new constructive frontier proves `D_4(12)>=8` and `D_4(14)>=10`; the generic
cap gives `D_4(12)<=9` and `D_4(14)<=11`.  Closing those one-query gaps is the
next target.
