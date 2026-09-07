# Bipartite color refinement before exact residual canonicalization

Status: exact finite proof-engineering result for `adaptive-gain`. Color refinement is an isomorphism-preserving search reduction, not an isomorphism test and not a biological claim.

## 1. Residual incidence problem

A residual fixed-cover state is represented by

```text
remaining budget B,
query costs c(q),
obligation-query incidence M[p,q].
```

Rows are uncovered cross-target pair obligations and columns are still-available queries. Row names and query names are irrelevant to continuation feasibility; query costs are not.

The exact canonicalizer must minimize the weighted incidence representation over every cost-preserving query relabeling. In a large unresolved symmetry class this creates a factorial search.

## 2. Safe color refinement

`refine_residual_incidence_colors()` treats the residual incidence as a weighted bipartite graph.

Initial query colors preserve the invariant already used by the original canonicalizer:

```text
acquisition cost,
number of adjacent obligation rows,
multiset of adjacent row degrees.
```

Initial row color is row degree. Then repeatedly refine

\[
\operatorname{color}_{t+1}(p)
=
\bigl(
\operatorname{color}_{t}(p),
\operatorname{multiset}\{\operatorname{color}_{t}(q):q\sim p\}
\bigr)
\]

and

\[
\operatorname{color}_{t+1}(q)
=
\bigl(
\operatorname{color}_{t}(q),
c(q),
\operatorname{multiset}\{\operatorname{color}_{t+1}(p):p\sim q\}
\bigr)
\]

until the partition is stable.

Previous colors are included in each update, so color classes can only split.

## 3. Exactness theorem

Any cost-preserving incidence isomorphism preserves every refinement round by induction:

1. initial costs and degrees are preserved;
2. if colors at round `t` are preserved, neighbor-color multisets are preserved;
3. therefore colors at round `t+1` are preserved.

Hence two queries in different stable colors can never be mapped to one another by a valid weighted-incidence isomorphism.

Therefore restricting exact permutation enumeration to the stable color classes is safe.

If the stable query classes are

\[
C_1,\ldots,C_k,
\]

then the exact enumeration count becomes

\[
\boxed{N_{\rm refined}=\prod_i |C_i|!}.
\]

Because refinement only splits the original classes,

\[
\boxed{N_{\rm refined}\le N_{\rm initial}}.
\]

The final canonical signature is still the lexicographic minimum over **all** permutations inside those stable classes. No approximate graph-isomorphism answer is substituted.

Implementation: `adaptive_gain/color_refinement.py`.

## 4. Registered 60x reduction witness

An eight-query residual structural benchmark has

```text
query costs = (1,1,1,1,1,1,2,3)
```

and twelve degree-2 obligation rows. Under the original one-step invariant, queries `q0..q5` are indistinguishable:

```text
initial query color sizes = (6,1,1)
N_initial = 6! = 720.
```

The differently priced `q6` and `q7` split neighboring rows; subsequent bipartite refinement propagates those distinctions back to `q0..q5`:

```text
stable query color sizes = (2,3,1,1,1)
N_refined = 2! * 3! = 12.
```

Thus

\[
\boxed{720\to 12}
\]

or a factor-60 exact search reduction.

The original canonicalizer and the refined canonicalizer return the same canonical signature. Moreover, with `max_permutations=12` the original exact canonicalizer fails closed while the refined exact canonicalizer completes.

This is a synthetic proof-engineering benchmark, not an expected universal speedup.

## 5. Complete minimal-universe signature regression

For all

```text
4 worlds,
2+2 binary target,
3 labeled binary unit-cost queries
```

there are `16^3 = 4096` labeled tasks. For every one, the residual canonical signature returned after color refinement is checked against the original exact canonicalizer.

Result:

```text
signature mismatches = 0.
```

Thus the optimized canonicalization preserves the existing complete minimal-universe classification, including the 192 strict-gain tasks.

## 6. Refinement is not a complete isomorphism test

A necessary adverse control is included.

Take four unit-cost query vertices and four obligation vertices, all of degree two.

One incidence graph is a connected bipartite 8-cycle:

```text
0011, 0110, 1100, 1001
```

and another is two disconnected 4-cycles:

```text
0011, 0011, 1100, 1100.
```

Stable color refinement leaves all four queries in one color class in both cases:

```text
stable query class sizes = (4,)
remaining exact permutations = 4! = 24.
```

But the exact canonical signatures differ, correctly identifying the two weighted incidence structures as non-isomorphic.

Therefore

\[
\boxed{\text{same stable colors}\not\Rightarrow\text{isomorphic}.}
\]

Color refinement is only a sound partition-refinement front end to exact canonicalization.

## 7. Relation to the proof stack

The fixed-side compression stack is now

```text
safe pair/query kernelization
-> exact residual-state DAG sharing
-> weighted-incidence isomorphism quotient
-> bipartite color refinement before exact canonicalization.
```

The first step shrinks one residual problem. The next two share equivalent continuation problems. Color refinement reduces the cost of proving that two name-different residual problems are or are not in the same exact isomorphism class.

## 8. Remaining frontier

Stable color classes can still be large. Exact enumeration is factorial in those unresolved classes.

The next exact directions are:

- individualization-refinement with independently checkable canonical leaves;
- certified automorphism generators and orbit pruning;
- stronger graph invariants that are guaranteed isomorphism-invariant;
- proof-size bounds after kernelization plus symmetry quotienting.

Any resource cap must remain fail-closed: exceeding the exact canonicalization budget is `incomplete`, never `non-isomorphic`.
