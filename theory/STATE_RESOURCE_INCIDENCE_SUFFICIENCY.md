# State-resource incidence sufficiency for fixed resolution

This note proves an exact deterministic fixed-resolution criterion that is weaker
than the full resource-labelled transition system.

For every reachable mixed state `s`, define

- `U_s`: queries already consumed on the history leading to `s`;
- `P_s`: still-available queries that are productive (nonconstant) on the worlds
  represented at `s`.

Only productive queries generate child states in the reachable-state construction.
A constant query may be omitted because once it is constant on a world subset, it
remains constant on every descendant subset.

## Theorem

For a fixed bundle `B`,

\[
\boxed{
B\text{ fails to resolve the target}
\iff
\exists s:\ U_s\subseteq B,\quad P_s\cap B=\varnothing.
}
\]

### Forward direction

Assume `B` fails. Then some pair of represented worlds with different targets has
the same outcome under every query in `B`.

Start at the root mixed state and repeatedly choose any query in `B` that is
productive on the current state. Follow the outcome cell containing that unresolved
cross-target pair. The pair survives every chosen query because all its `B`
outcomes agree.

The process is finite. It terminates at a reachable mixed state `s` after using a
subset `U_s` of `B`. At termination no remaining query from `B` is productive, so

\[
U_s\subseteq B,\qquad P_s\cap B=\varnothing.
\]

### Reverse direction

Suppose a reachable mixed state `s` satisfies

\[
U_s\subseteq B,\qquad P_s\cap B=\varnothing.
\]

The queries in `U_s` have already been applied on the history to `s`. Every query
in `B\\U_s` is nonproductive on `s`; applying them cannot refine that mixed state.
Therefore the complete bundle `B` leaves at least one mixed target cell and fails.

QED.

## Exact fixed optimum

The theorem gives a bundle test that does not need world-pair identities or child
wiring. A bundle resolves iff no stored row witnesses failure:

```text
for every row (U,P):
    not (U subseteq B and P intersect B = empty)
```

Thus query costs together with the unique reachable `(U,P)` rows determine `C_F`.

The implementation is `adaptive_gain/state_resource_incidence.py`.

## Row dominance

A row `(U1,P1)` makes `(U2,P2)` redundant when

\[
U_1\subseteq U_2,\qquad P_1\subseteq P_2.
\]

Any bundle failing the second row also fails the first, so the second row can be
removed without changing the exact fixed optimum. `reduced_rows` applies this
componentwise-subset kernel.

## Joint representation

The existing cost-only continuation quotient already determines deterministic
adaptive worst-path cost `C_A`. Therefore

\[
\boxed{
\text{cost-only continuation structure}
+
\{(U_s,P_s)\}_{s\text{ mixed}}
\Longrightarrow
(C_A,C_F).
}
\]

This is strictly weaker than retaining the full resource-labelled child transition
system for the purpose of computing the two scalar costs. It does not preserve
named optimal policies, child wiring, report labels, stochastic probabilities, or
calibration semantics.

## Validation

Regression checks include:

- the registered `C_F=3` versus `C_F=2` continuation collision;
- the registered four-query per-resource-role collision;
- all `15^3 = 3,375` triples of arbitrary set partitions on four balanced worlds;
- all `15^2 x 2^2 = 900` two-query arbitrary-partition tasks with costs in `{1,2}`;
- tampered-certificate rejection.

These finite checks test the implementation. The theorem itself follows from the
bundle-failure equivalence above and is not inferred from enumeration.

## Claim boundary

The result is limited to the repository's finite deterministic guaranteed-target-
resolution contract with positive acquisition costs. It does not by itself extend
to noisy observations, expected-loss objectives, repeated stochastic sampling,
calibration-changing actions, continuous compatible sets, or scientific report
licensing.
