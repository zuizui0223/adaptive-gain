# Exact-balanced binary depth-four sharp value at eighteen worlds

Define

\[
D_4(n)=\max\{C_F:C_A\le4\}
\]

for unit-cost binary queries that are globally exact 50/50 on the represented
worlds.  The explicit 18-world lower witness gives

\[
D_4(18)\ge13.
\]

This note closes the remaining one-query gap.

## 1. Why a hypothetical `C_F=14` reduces to `B14 + r`

Let `T` be a resolving adaptive tree of depth at most four.  Let `U` be the
set of distinct query labels occurring in `T`.  Flattening the tree gives a
fixed resolver, so

\[
14=C_F\le |U|\le15.
\]

If `|U|=14`, set `B=U`.  Suppose instead `|U|=15`.  The fixed minimum inside
`U` is at least the global minimum 14.  It cannot equal 15.  If it did, all 15
queries in `U` would be fixed-mandatory.  Since 15=`18-3`, the exact-balanced
cap-saturation theorem applies and forces adaptive depth

\[
18/2-1=8
\]

when only those 15 queries are available.  But `T` itself uses only `U` and has
depth at most four, a contradiction.  Therefore the restricted fixed minimum
inside `U` is 14.  Hence `U` contains a minimum 14-query resolver `B`, and
there is at most one additional tree query `r`.

So every hypothetical `(C_A,C_F)=(4,14)` task is represented by a `B14+r`
case.  This is the step that makes the finite exhaustive audit universal.

## 2. Exhaust all possible minimum bundles `B`

Choose one private cross-target pair for each query of the minimum resolver
`B`.  The private-pair graph is a forest: a cycle would make one private edge
separable by the other queries.  With 18 vertices and 14 edges it therefore has
four connected components.

There are 47 unordered positive four-part partitions of 18.  Exact 9/9 balance
eliminates all but the following seven component-size types:

```text
(1,1,8,8)
(1,2,7,8)
(1,3,7,7)
(2,2,6,8)
(2,3,5,8)
(2,4,4,8)
(4,4,4,6)
```

For an edge `e`, its query must be constant across every other private edge and
flip across `e`.  Removing `e` gives five forest components; an exact-balanced
query is therefore precisely a union of those components of total size nine
that puts the endpoints of `e` on opposite sides.  Enumerating all admissible
tree forms and all such edge-cut choices gives:

```text
admissible private-forest forms: 35
balanced minimum-bundle configurations B: 1,246
```

After quotienting outcome complementation, 1,231 of these `B` matrices identify
all 18 worlds.  The remaining 15 have exactly one pair of worlds with the same
`B` signature; because `B` is a resolver, that pair is forced to share target.

## 3. Add the only possible extra tree query `r`

There are

\[
\frac12\binom{18}{9}=24,310
\]

exact-balanced cut classes, where a cut and its complement represent the same
binary query.

For each `B`, every candidate `r` is first tested against the fixed lower bound.
For a 15-query family `B+r`, a fixed resolver of size at most 13 can be padded
to size 13.  Equivalently, among the 105 ways to omit two of the 15 queries,
none may resolve the target.  A world pair with query-difference set of size one
or two witnesses exactly the omission pairs containing that difference set.

### Identifying `B`

For the 1,231 identifying bundles:

```text
B+r candidates retaining the fixed-14 omission condition: 49,590
candidates able to separate all 14 registered private edges in depth 4: 134
```

For the remaining 134 candidates an exact decision-tree DP tracks 119 required
conditions simultaneously:

```text
105 two-query omission conditions
+14 registered private-edge separation conditions
=119 conditions.
```

No candidate reaches all 119.  The best reaches 118.

```text
full 119/119 hits: 0
maximum coverage: 118/119
```

### The 15 collision bundles

For a collision bundle, the unique equal-signature world pair is forced to have
the same target and therefore cannot serve as an omission witness.  Recomputing
the omission condition with that pair excluded gives:

```text
fixed-14-safe B+r candidates: 84,116
private-edge depth-four candidates: 21,448
```

For each of those candidates, every omission condition having a unique
cross-target witness contributes a mandatory world pair that the adaptive tree
must separate.  Adding the 14 registered private edges yields between 22 and 41
mandatory pairs, depending on the candidate.  Exact depth-four feasibility for
these mandatory pairs leaves

```text
survivors: 0.
```

Thus the collision cases also contain no `(4,14)` task.

## 4. Sharp conclusion

Both exhaustive branches are empty, so

\[
D_4(18)\le13.
\]

The explicit 13-query construction already has `(C_A,C_F)=(4,13)`.  Therefore

\[
\boxed{D_4(18)=13}.
\]

Together with the previously closed finite sizes and the 20-world ceiling
witness, the certified depth-four frontier is now

```text
n=12: D4=8
n=14: D4=10
n=16: D4=12
n=18: D4=13
n>=20 even: D4=15
```

The balanced-binary fixed-`(n,m)` problem remains open in general, but the
adaptive-depth-four slice is now closed through the transition to the universal
15-query flattening ceiling.
