# Productive-frontier rank caps do not reduce the sharp unit-cost ratio

Let the productive frontier of a finite deterministic task be the inclusion-minimal hypergraph

\[
\mathcal H_{\min}=\min_{\subseteq}\{P_s:s\text{ reachable target-mixed}\},
\]

where `P_s` is the set of physical queries productive on state `s`.
Define its hypergraph rank by

\[
\operatorname{rank}(\mathcal H_{\min})
=
\max_{E\in\mathcal H_{\min}}|E|.
\]

Fix

- `n >= 2` represented worlds,
- `m >= 1` unit-cost query resources,
- maximum query outcome arity `b >= 2`, and
- a positive productive-frontier rank cap `r >= 1`.

Let `R_b(n,m)` be the already established sharp fixed/adaptive ratio with no frontier-rank restriction.

## Theorem

For every positive rank cap,

\[
\boxed{
R_{b,\,\operatorname{rank}\le r}(n,m)
=
R_b(n,m).
}
\]

So an upper bound on productive-frontier edge size alone gives **no improvement at all** in the worst-case adaptive/fixed ratio.

## Upper bound

The rank-capped task class is a subclass of the unrestricted bounded-arity class. Therefore

\[
R_{b,\,\operatorname{rank}\le r}(n,m)
\le R_b(n,m).
\]

## Matching lower bound

The constructive witness used in `bounded_arity_extremal_bounds.py` has one physical query for each internal node of a maximizing bounded-arity adaptive tree.
For every such query `q`, a registered cross-target private pair is separated by `q` and by no other declared query.

Therefore the fixed productive frontier contains the singleton edge

\[
\{q\}
\]

for every non-padding query. All larger productive sets are inclusion-redundant, so

\[
\mathcal H_{\min}
=
\{\{q_1\},\ldots,\{q_t\}\}
\]

for the `t` fixed-mandatory resources in the sharp construction. Hence

\[
\boxed{\operatorname{rank}(\mathcal H_{\min})=1}.
\]

The same witness already attains `R_b(n,m)`. Because rank one satisfies every cap `r>=1`,

\[
R_{b,\,\operatorname{rank}\le r}(n,m)
\ge R_b(n,m).
\]

Together with the upper bound, equality follows.

## Interpretation

This distinguishes productive-frontier **rank** from productive-frontier **edge count**.

A cap on edge count can reduce `C_F`, because a hitting set needs at most one chosen query per frontier edge. That is why the exact edge-capped extremal theorem contains `E` explicitly.

By contrast, small edge size does not make the fixed problem weak. A singleton edge is the strongest possible obligation:

\[
\{q\}\in\mathcal H_{\min}
\quad\Longrightarrow\quad
q\text{ belongs to every fixed resolver}.
\]

Thus rank-one frontiers can already force arbitrarily many distinct resources and realize the full bounded-arity extremal ratio.

If one wants a structural restriction that actually limits worst-case adaptive gain, useful candidates must constrain something stronger than maximum edge size, for example

- the number of frontier edges,
- a **lower** bound on edge size,
- edge intersection / covering multiplicity,
- transversal number directly,
- degree/frequency of resource participation, or
- balancedness constraints on the underlying queries.

## Implementation and validation

- `adaptive_gain/frontier_rank_extremal_bounds.py`
- `tests/test_frontier_rank_extremal_bounds.py`

The regression suite checks that rank cap one already reproduces the sharp bounded-arity ratio across a finite grid of world counts, query counts, and arity bounds, and independently verifies that the registered sharp witnesses have frontier rank exactly one.

## Scope

This is a finite deterministic guaranteed-target-resolution theorem with unit acquisition costs. `rank` means **maximum cardinality of an inclusion-minimal productive-frontier edge**. It does not claim that frontier rank is irrelevant for computational complexity, enumeration complexity, probabilistic objectives, or richer scientific semantics.
