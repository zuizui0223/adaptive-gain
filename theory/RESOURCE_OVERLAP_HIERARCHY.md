# Resource-overlap hierarchy for joint adaptive/fixed resolution

This note separates which resource information is sufficient for deterministic
worst-path adaptive cost `C_A` and fixed-bundle cost `C_F`.

The finite contract remains:

- finitely many represented hidden worlds;
- a declared target label in every world;
- positive query acquisition costs;
- deterministic query outcomes;
- exact guaranteed target resolution.

No statement here is a natural-data prevalence claim or report-license claim.

## 1. Orbit capacity is not enough

The cost-only continuation quotient preserves `C_A` but forgets physical query
identity. Adding only exact query-orbit sizes/costs still does not recover `C_F`.

The registered five-world pair `orbit_capacity_collision()` has the same
cost-only continuation root type and the same query-orbit capacity profile, but

\[
(C_A,C_F)=(2,3)
\]

versus

\[
(C_A,C_F)=(2,2).
\]

Therefore

\[
\boxed{
\text{continuation type + resource-orbit capacities}
\not\Rightarrow C_F.
}
\]

## 2. First-order per-resource role profiles are still not enough

For each physical query `q`, record the set of abstract local roles

\[
(\text{parent continuation type},\text{ local action type})
\]

that it realizes anywhere in the reachable mixed-state graph.

This is stronger than orbit capacity, but the four-world/four-query pair
`resource_role_profile_collision()` has the same continuation root type and the
same multiset of complete per-resource role profiles while its exact fixed costs
are `2` and `3`.

Hence

\[
\boxed{
\text{continuation type + per-resource role-profile multiset}
\not\Rightarrow C_F.
}
\]

The exact balanced four-world binary scan locates the first registered ambiguity:

- with three queries, all `16^3=4,096` labeled tasks have zero ambiguous role-profile signatures;
- with four queries, one ambiguous signature contains `2,304` tasks:
  `1,536` with `(C_A,C_F)=(2,2)` and `768` with `(2,3)`.

## 3. Reachable state-resource incidence is sufficient for `C_F`

The previous version of this note treated co-location only as an empirical repair.
The stronger result is now proved.

For every reachable mixed state `s`, define

- `U_s`: queries already used on the history to `s`;
- `P_s`: still-available queries productive (nonconstant) on `s`.

For a fixed bundle `B`,

\[
\boxed{
B\text{ fails}
\iff
\exists s:\ U_s\subseteq B,\quad P_s\cap B=\varnothing.
}
\]

If `B` fails, follow a surviving cross-target pair while repeatedly applying any
productive query from `B`; the process terminates at a mixed state where all
remaining `B` queries are constant. Conversely, such a state is an explicit
witness that applying the rest of `B` cannot resolve the target.

Therefore query costs plus the set of reachable `(U_s,P_s)` rows determine the
exact fixed optimum:

\[
\boxed{
\{(U_s,P_s)\}_{s\text{ mixed}} + \text{query costs}
\Longrightarrow C_F.
}
\]

Concrete child wiring and world-pair identities are unnecessary for this scalar
fixed optimum.

Implementation: `adaptive_gain/state_resource_incidence.py`.

See `theory/STATE_RESOURCE_INCIDENCE_SUFFICIENCY.md`.

## 4. A smaller fixed-side row kernel

A row `(U_1,P_1)` dominates `(U_2,P_2)` when

\[
U_1\subseteq U_2,\qquad P_1\subseteq P_2.
\]

Every bundle failing row 2 also fails row 1, so row 2 is redundant. The
`reduced_rows` certificate removes these componentwise-dominated failure rows
without changing `C_F`.

This is a different compression from cross-target pair-cover dominance: it works
on reachable history/resource incidence rather than world-pair obligations.

## 5. Joint sufficiency without child wiring

The cost-only continuation quotient already determines `C_A`. Combining it with
the state-resource incidence theorem gives

\[
\boxed{
\text{cost-only continuation structure}
+
\{(U_s,P_s)\}_{s\text{ mixed}}
\Longrightarrow
(C_A,C_F).
}
\]

This is strictly weaker than retaining the full resource-labelled transition
system when only the two scalar optimum costs are required.

The richer `resource_continuation.py` remains useful when one needs named resource
transitions, policy lifting, explicit child structure, or resource-transition
isomorphism certificates. Its sufficiency is unchanged; it is simply no longer
minimal for the scalar pair `(C_A,C_F)`.

## 6. Revised hierarchy

The current information hierarchy is therefore

\[
\boxed{
\begin{array}{c}
\text{orbit capacity}\quad\text{(insufficient for }C_F\text{)}\\
\downarrow\\
\text{per-resource role profile}\quad\text{(insufficient for }C_F\text{)}\\
\downarrow\\
\text{reachable state-resource }(U,P)\text{ incidence}\quad\Rightarrow C_F\\
\downarrow\\
\text{resource-labelled transition structure}\quad\Rightarrow(C_A,C_F)\text{ plus wiring}
\end{array}
}
\]

For the joint scalar costs, attach the cost-only continuation quotient to the
`(U,P)` incidence layer.

## 7. Validation and scope

Implementation checks include the two registered fixed-cost collisions,
all `15^3=3,375` arbitrary three-query set-partition tasks on four balanced worlds,
and all `15^2 x 2^2=900` two-query arbitrary-partition tasks with costs in `{1,2}`.
Those tests validate code; the sufficiency claim follows from the bundle-failure
equivalence above.

The theorem does not automatically extend to stochastic repeated sampling,
expected loss, calibration-changing actions, continuous compatible sets, or
scientific report licensing.
