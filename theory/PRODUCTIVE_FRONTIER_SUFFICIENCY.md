# Productive-frontier sufficiency for fixed resolution

This note strengthens the state-resource incidence theorem.

For every reachable mixed state `s`, let

\[
P_s=\{q:\ q\text{ is productive (nonconstant) on }s\}.
\]

A query already used earlier on the history to `s` is constant on the selected
outcome cell and remains constant on every descendant subset. Therefore `P_s` is
the set of all physical queries that can still refine `s`, not merely the unused
ones.

## Theorem

For any fixed bundle `B`,

\[
\boxed{
B\text{ resolves the target}
\iff
B\cap P_s\neq\varnothing
\quad\text{for every reachable mixed state }s.
}
\]

### If a productive edge is missed, the bundle fails

Suppose a reachable mixed state `s` satisfies

\[
B\cap P_s=\varnothing.
\]

Every query in `B` is constant on `s`: previously used queries are constant on
their chosen outcome cells, and all other nonproductive queries are constant by
definition. Hence the complete bundle cannot refine `s`, so a mixed target cell
survives.

### If the bundle fails, some productive edge is missed

Suppose `B` fails. Then some pair of represented worlds with different targets has
identical outcomes under every query in `B`.

Start at the root and repeatedly apply any query from `B` that is productive on
the current state, following the outcome cell containing that unresolved pair.
The pair survives every step. Because the vocabulary is finite, the process ends
at a reachable mixed state where no query in `B` is productive:

\[
B\cap P_s=\varnothing.
\]

QED.

## Fixed resolution is a hitting-set problem

The theorem gives

\[
\boxed{
C_F
=
\min_{B}
\left\{
\sum_{q\in B}c(q):
B\cap P_s\neq\varnothing\ \forall s
\right\}.
}
\]

Thus the exact fixed comparator can be computed from the reachable productive-set
hypergraph without world-pair identities, used-query sets, or child wiring.

Implementation: `adaptive_gain/productive_frontier.py`.

## Minimal productive frontier

If

\[
P_1\subseteq P_2,
\]

then every bundle hitting `P_1` automatically hits `P_2`. Therefore only
inclusion-minimal productive sets are needed.

The retained hyperedges form an ordinary antichain in the Boolean lattice of the
`q` query resources. By Sperner's theorem,

\[
\boxed{
|\mathcal P_{\min}|
\le
\binom q{\lfloor q/2\rfloor}.
}
\]

This is tighter than the earlier ternary `(U,P)` antichain bound when only scalar
`C_F` is required.

For the complete `15^3=3,375` arbitrary-partition four-world/three-query
regression, the largest observed minimal productive frontier has exactly three
edges, saturating the Sperner bound `C(3,1)=3`.

## Joint scalar-cost representation

The cost-only continuation quotient independently determines `C_A`. Therefore

\[
\boxed{
\text{cost-only continuation structure}
+
\mathcal P_{\min}
\Longrightarrow
(C_A,C_F).
}
\]

This is the current smallest proved joint scalar-cost representation in the
repository. It is not claimed minimal in an information-theoretic or categorical
sense.

Richer structures remain necessary for richer outputs:

- named adaptive policy lifting;
- explicit child transition wiring;
- resource-transition isomorphism witnesses;
- scientific report labels;
- stochastic likelihoods or calibration state.

## Validation scope

Implementation checks include the registered fixed-cost collisions, all
`15^3=3,375` arbitrary three-query set-partition tasks on four balanced worlds,
and all `15^2 x 2^2=900` two-query arbitrary-partition tasks with costs in
`{1,2}`.

Those checks validate implementation. The theorem follows from the productive-
frontier hitting-set equivalence above.
