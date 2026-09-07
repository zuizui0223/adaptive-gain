# Sharp unit-cost ratio under a productive-frontier edge cap

The productive frontier

\[
\mathcal H_{\min}
=
\min_{\subseteq}\{P_s:s\text{ reachable mixed}\}
\]

is the exact fixed-side sufficient statistic.  Under unit costs,

\[
C_F=\tau(\mathcal H_{\min}),
\]

where `tau` is transversal number.

This note adds a structural cap

\[
|\mathcal H_{\min}|\le E
\]

to the fixed-world / fixed-query / bounded-arity extremal problem.

## Upper bound

For a hypergraph with at most `E` nonempty edges,

\[
\tau(\mathcal H)\le E,
\]

because choosing one resource from each edge gives a hitting set of size at most
`E`.

The bounded-arity tree theorem already gives, for `C_A=h`,

\[
C_F\le \min\{m,F_b(n,h)\}.
\]

Combining the independent vocabulary, frontier-edge, and adaptive-tree bounds,

\[
\boxed{
C_F
\le
\min\{m,E,F_b(n,C_A)\}.
}
\]

Hence

\[
\boxed{
\frac{C_F}{C_A}
\le
R_{b,E}(n,m)
:=
\max_{1\le h\le n-1}
\frac{\min\{m,E,F_b(n,h)\}}{h}.
}
\]

## Sharpness

Use the private-pair forest construction from
`SHARP_BOUNDED_ARITY_UNIT_COST_RATIO.md`, but retain only

\[
I=\min\{m,E,F_b(n,h)\}
\]

internal-node queries at a maximizing depth.

Every retained query has a cross-target pair for which it is the unique separator.
By productive-frontier / minimal-pair-separator equivalence, the minimal frontier
contains the singleton edge for every retained query.

Because every nonempty frontier edge contains some retained resource, those
singleton edges make all larger edges inclusion-nonminimal.  Thus

\[
\boxed{
\mathcal H_{\min}
=
\{\{q_1\},\ldots,\{q_I\}\}
}
\]

and

\[
|\mathcal H_{\min}|=I\le E,
\qquad
C_F=I.
\]

The same bounded-arity tree is an adaptive resolving policy of depth at most
`h`.  Therefore the constructed ratio is at least `I/h`; the universal upper
bound forbids anything larger.  Hence the bound is exact:

\[
\boxed{
\max_{\substack{|W|=n,\ |Q|=m,\operatorname{arity}\le b\\
|\mathcal H_{\min}|\le E}}
\frac{C_F}{C_A}
=
R_{b,E}(n,m).
}
\]

## Consequences

- `E=1` forces ratio 1.
- `E>=m` recovers the uncapped bounded-arity theorem.
- At fixed `n,m,b`, increasing the number of frontier obligations can only
  increase the extremal ratio.
- The role of frontier **edge count** is therefore completely separate from
  frontier rank or more detailed incidence geometry.

## Implementation

- `adaptive_gain/frontier_edge_extremal_bounds.py`
- `tests/test_frontier_edge_extremal_bounds.py`

The executable audit checks endpoint recovery, monotonicity in `E`, and exact
solver agreement on a small grid for arities 2, 3, and 4.

## Scope

This theorem assumes finite deterministic guaranteed target resolution and unit
query costs.  It does not address unequal costs, stochastic likelihoods,
calibration-changing actions, or continuous compatible sets.
