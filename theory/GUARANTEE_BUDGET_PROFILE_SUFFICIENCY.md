# Deterministic guarantee budget profiles need only `(C_A,C_F)`

For the finite deterministic exact target-resolution contract, define for every
nonnegative integer budget `B`:

\[
A(B)=\mathbf 1[C_A\le B],
\qquad
F(B)=\mathbf 1[C_F\le B].
\]

The adaptive-only indicator is

\[
G_{\mathrm{exact}}(B)=A(B)(1-F(B)).
\]

Therefore the complete guarantee budget profile is a pair of step functions and
contains no information beyond the two minima:

\[
\boxed{
(C_A,C_F)
\Longrightarrow
\{A(B),F(B),G_{\mathrm{exact}}(B):B\ge0\}.
}
\]

Conversely the full profile identifies the first budget at which each class
becomes feasible, so it recovers the same minima whenever they are finite.

## Compact reconstruction

The repository already has two compact sufficient objects:

- cost-only continuation structure determines `C_A`;
- the static minimal productive frontier, generated directly from cross-target
  pair incidence, determines `C_F`.

Hence

\[
\boxed{
\text{adaptive continuation}
+
\mathcal H_{\min}
\Longrightarrow
\text{entire deterministic guarantee budget profile}.
}
\]

`adaptive_gain/frontier_budget_profile.py` reconstructs the profile this way and
checks it against `core.resolution_budget_profile`.

## All optimal fixed bundles

The same minimal productive frontier retains more than scalar `C_F`.  A fixed
bundle resolves iff it hits every frontier edge, so

\[
\boxed{
\operatorname{OptFixed}
=
\arg\min_{B:\,B\cap E\ne\varnothing\;\forall E\in\mathcal H_{\min}} c(B).
}
\]

Thus named child wiring is unnecessary even to recover **all** minimum-cost fixed
bundles.  `minimal_frontier_fixed_minimum_resolution()` returns the same complete
`optimal_bundles` tuple as the direct world-table solver.

## Validation

Regression checks include:

- MROD-style and PAYOFF-style routing witnesses through budgets `0..4`;
- all `16^3=4096` balanced four-world / three-binary-unit-cost tasks through
  budgets `0..3`;
- exact equality of every profile row and of the complete set of optimal fixed
  bundles between compact and direct solvers.

## Claim boundary

This result is specific to **binary feasibility of exact guaranteed resolution**.
It does not collapse richer budget-indexed objectives such as mutual information,
expected loss, posterior entropy, calibration value, or stochastic success
probability.  Those can vary nontrivially below the exact-resolution threshold and
remain separate open problems.
