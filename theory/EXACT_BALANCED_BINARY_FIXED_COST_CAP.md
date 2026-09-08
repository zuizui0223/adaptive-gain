# Sharp fixed-cost cap for exact-balanced binary queries

Global exact 50/50 balance does not keep adaptive advantage bounded as the
problem grows, but it imposes a strong finite restriction on the fixed side.
This note gives the exact maximum possible fixed resolution cost at a fixed
even number of represented worlds.

## Theorem

Let `n` be even, all query costs be one, and every declared query be binary with
exactly `n/2` worlds on each outcome.  Then

\[
\boxed{
\max C_F=
\begin{cases}
1,&n=2,\\
2,&n=4,\\
n-3,&n\ge6.
\end{cases}
}
\]

The maximum is over arbitrary target partitions, arbitrary query counts, and
arbitrary exactly-balanced deterministic query vocabularies.

For comparison, without the exact-balance restriction the binary fixed side can
require `n-1` essential queries.  Thus exact 50/50 balance removes two units of
worst-case fixed essentiality for every even `n>=6`.

## 1. A minimum fixed bundle supplies private pairs

Let `B` be a minimum-cardinality fixed resolver and write `|B|=C_F`.
For every `q in B`, the bundle `B\{q}` is not resolving.  Therefore there is a
pair of worlds `(x_q,y_q)` with different targets such that every query in
`B\{q}` gives the same outcome on the pair.  Since `B` itself resolves, `q`
separates that pair.

So every member of a minimum fixed bundle owns a **private cross-target pair**:

\[
q(x_q)\ne q(y_q),
\qquad
r(x_q)=r(y_q)\quad\forall r\in B\setminus\{q\}.
\]

Private pairs belonging to different queries are necessarily distinct.

## 2. The private-pair graph is a forest

Create a graph `G` on the represented worlds, with one selected private-pair
edge `e_q={x_q,y_q}` for every `q in B`.

Query `q` separates its own edge `e_q`.  It separates no other selected edge,
because every other edge is private to its own query.  Hence there is a vertex
bipartition whose cut in `G` consists of exactly `e_q`.

An edge is the unique edge of some graph cut only if it is a bridge.  Every edge
of `G` is therefore a bridge, so

\[
\boxed{G\text{ is a forest}.}
\]

In particular `C_F=|E(G)|<=n-1` even before balance is used.

## 3. Exact balance rules out one- and two-component extremizers

Write `n=2h`.

### `C_F=n-1` is impossible

Then `G` would be a tree.  Choose a leaf edge.  Because the corresponding query
crosses no other graph edge, every connected component after deleting that edge
must lie wholly on one side of the query cut.  The two components have sizes
`1` and `n-1`, which cannot form an `h/h` partition for `n>=4`.

Thus `C_F<=n-2`.

### `C_F=n-2` is impossible for `n>=6`

Then `G` has exactly two connected components.

If both components have at least two vertices, take an edge in the smaller
component.  The larger component has at least `h` vertices and must remain
whole under the corresponding query.  If it has more than `h` vertices, an
exactly-balanced side is immediately impossible.  If both components have
exactly `h` vertices, placing the larger component on one side already fills
that side and leaves no room to split the chosen edge of the other component.
So the smaller component cannot contain an edge.

The only remaining possibility is therefore an isolated vertex plus a tree on
`n-1` vertices.  Take a leaf edge of the large tree.  After deleting it, the
large-tree remainder has size `n-2`.  For `n>=6`,

\[
n-2>n/2=h,
\]

and that connected remainder must remain wholly on one side of the query cut,
again contradicting exact balance.

Hence

\[
\boxed{C_F\le n-3\qquad(n\ge6).}
\]

For `n=4`, the isolated-vertex plus three-vertex-tree configuration is feasible,
which is why the sharp small exception is `C_F=2` rather than `n-3=1`.

## 4. Sharp construction for every even `n>=6`

Let `n=2h` and split the worlds into three private-pair components of sizes

\[
(h-1,\ 2,\ h-1).
\]

Use a star on the first `h-1` worlds, one edge on the middle two worlds, and a
star on the last `h-1` worlds.  The forest has

\[
(h-2)+1+(h-2)=n-3
\]

edges.

For a leaf edge in the left star, make the query's 1-side consist of the left
star with that leaf deleted, plus both middle worlds.  Its size is

\[
(h-2)+2=h.
\]

This query crosses exactly that star edge.  Do the symmetric construction for
every right-star edge.  For the middle edge, take the whole left star plus one
middle endpoint, again giving `h` worlds.  Thus every query is exactly 50/50 and
every forest edge is private to one query.

The resulting query signatures are distinct across all worlds.  Assigning a
distinct target to every world makes the whole `n-3` query family resolving,
while every query is individually mandatory by its private pair.  Therefore

\[
C_F=n-3.
\]

The `n=2` and `n=4` sharp witnesses are handled separately by one and two
balanced cuts respectively.

## 5. Consequence for adaptive-gain extremal bounds

For every exactly-balanced binary task with even `n>=6`, unit costs, `m`
declared queries, and adaptive optimum `C_A=h_A`, the ordinary binary productive
tree bound and the new fixed cap combine to give

\[
\boxed{
C_F\le
\min\{m,\ n-3,\ F_2(n,h_A)\}.
}
\]

Hence

\[
\boxed{
\frac{C_F}{C_A}
\le
\max_{1\le h\le n-1}
\frac{\min\{m,n-3,F_2(n,h)\}}{h}.
}
\]

This upper bound is sharp at the already-closed `n=8` row, but it is **not yet
claimed sharp for all larger `(n,m)`**.  In particular `n=10` becomes the next
natural test: the fixed side is now known to satisfy `C_F<=7`, so the remaining
question is whether adaptive depth and exact balance can jointly attain the
resulting candidate envelope.

## Reproducibility

Implementation and finite witness audits:

- `adaptive_gain/balanced_binary_fixed_cost_cap.py`
- `tests/test_balanced_binary_fixed_cost_cap.py`

The upper theorem is analytic; the tests verify the sharp constructions against
the repository's independent exact fixed solver for representative even world
counts.
