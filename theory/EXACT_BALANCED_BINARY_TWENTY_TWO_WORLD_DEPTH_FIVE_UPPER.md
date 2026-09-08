# Exact-balanced binary depth-five upper reduction at 22 worlds

Define

\[
D_5(22)=\max\{C_F:C_A\le5\}
\]

for unit-cost binary queries that are globally exact 11/11 on the represented worlds.
The registered construction already gives `D5(22) >= 17`.

## 1. Ruling out 19

The universal fixed-cost cap is `C_F <= n-3 = 19`.  Suppose a depth-five task had `C_F=19` and let `U` be the distinct query labels used by one resolving depth-five tree.  Flattening the tree makes `U` a fixed resolver.  Therefore the restricted task on `U` has fixed minimum at least 19; the universal cap makes it exactly 19.  Hence `U` contains a minimum 19-query resolver `B`.

Every cap-saturating exact-balanced minimum resolver has the star--edge--star private-pair normal form with component sizes `(10,2,10)`, up to relabelling and outcome complementation.  Its query signatures distinguish all 22 worlds.

Consequently every additional tree query must be identity-safe: if `B+r` admitted an 18-query identity resolver, the same 18 queries would resolve the original targets, contradicting `C_F=19`.

There are `C(21,10)=352716` exact 11/11 cut classes modulo outcome complementation.  Exhaustion leaves only **three** identity-safe external cuts.  All `2^3=8` subsets were checked by exact depth-five DP.  For each subset the mandatory pair set contains the 19 registered private pairs and all singleton two-query-omission witnesses forced by retaining fixed cost 19.  Every subset is depth-five infeasible.

Therefore

\[
D_5(22)\le18.
\]

## 2. Why the old private-edge construction cannot attain 18

If an 18-query minimum resolver certifies all 18 queries by query-unique private pairs, its private-pair graph has 22 vertices, 18 edges and four components.  Exact 11/11 balance at every leaf edge leaves eight component-size types:

```text
(1,1,10,10)
(1,2,9,10)
(1,3,9,9)
(2,2,8,10)
(2,3,7,10)
(2,4,6,10)
(2,5,5,10)
(5,5,5,7)
```

Enumerating all compatible non-isomorphic component trees yields **60 forest forms**.  Exhausting every admissible exact-balanced private cut gives **4,742 query matrices**.  Exact DP finds **zero** matrices whose private edges can all be separated in depth five.

Thus a hypothetical `(C_A,C_F)=(5,18)` task cannot be another member of the global-private-edge family used for the sharp depth-four constructions.  It must use queries outside its minimum 18-query resolver in an essential adaptive role, and likely needs higher-order obstruction pairs rather than 18 globally private edges.

## 3. Current certified interval

\[
\boxed{17\le D_5(22)\le18}.
\]

The remaining one-query gap is now the next target.
