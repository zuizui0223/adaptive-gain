# Exact-balanced binary adaptive depth five: first constructive frontier

Let

\[
D_5(n)=\max\{C_F:C_A\le5\}
\]

for unit-cost binary queries that are globally exact 50/50 on the represented
worlds.  The universal bounds are

\[
D_5(n)\le \min\{31,n-3\}.
\]

The first registered depth-five construction starts from the certified
20-world depth-four ceiling witness `(C_A,C_F)=(4,15)`.

## 22 worlds: `(C_A,C_F)=(5,17)`

In the 20-world witness, worlds `w6` and `w13` have complementary signatures on
all fifteen registered queries.  Add two worlds `w20,w21` duplicating those two
signatures.  Every old query therefore receives one additional zero and one
additional one, so all fifteen become exact 11/11 on 22 worlds.

Two new balanced queries are then added.  Query `q15` makes `(w6,w20)` a
query-unique private pair, while `q16` makes `(w13,w21)` a query-unique private
pair.  Both new queries are constant across every old registered private edge,
so all seventeen private certificates survive.  Each new query is also exact
11/11.

The old depth-four decision tree is unchanged except at two leaves.  At the old
`w6` leaf ask `q15`; at the old `(w3,w13)` leaf ask `q16`.  Hence worst-case
adaptive depth is five.  Since all seventeen queries have cross-target private
pairs,

\[
\boxed{(C_A,C_F)=(5,17)}.
\]

## Padding family

Appending an all-zero/all-one complementary world pair to all seventeen queries
preserves exact balance, the registered private pairs, and the same adaptive
policy after assigning each padding world the target of the leaf it reaches.
Therefore

\[
\boxed{D_5(n)\ge17\quad\text{for every even }n\ge22.}
\]

This is only the first lower frontier.  The remaining question is how quickly
`D_5(n)` rises from 17 toward the flattening ceiling 31, and whether finite-size
defects analogous to the depth-three `n=10` and depth-four `n=18` defects occur.
