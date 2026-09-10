# General-response identifiability branch

This branch sits downstream of the generalized evolutionary-response theory and sharpens the interpretation limits of local evolutionary transients.

The main paper-level focus is **not** observation design. It is the relation among structurally generated selection amplitude, community temporal structure, long-term retention, and feedback geometry.

Start with:

- `MAIN_ECO_EVOLUTIONARY_CLAIM.md` — four-pillar synthesis for the main theoretical paper;
- `ECO_EVOLUTIONARY_TIMESCALE_THEORY_MAP.md` — hierarchy of the structural, temporal, feedback, and identifiability layers;
- `FEEDBACK_EXISTENCE_FROM_OSCILLATION.md` — qualitative feedback-existence corollary.

## Generalized local invariants

The generalized local response has

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G.
\]

A free scalar transient can identify the characteristic invariants `(T,D)` when both local modes are visible, but does not generally identify `(alpha,phi,G)` separately.

For every feasible candidate community memory `phi`,

\[
\alpha(\phi)=T-\phi,
\]

\[
G(\phi)=\frac{D-T\phi+\phi^2}{1-\phi}
\]

produce the same local characteristic polynomial.

Thus the broad boundary remains

\[
\boxed{(T,D)\text{ do not jointly identify }(\alpha,\phi,G).}
\]

## Feedback existence has a sharper asymmetry

The numerator of `G(phi)` is exactly the characteristic polynomial evaluated at `phi`.

If both observed local eigenvalues are real and lie in `[0,1)`, assigning one to `phi` and the other to `alpha` yields

\[
G=0.
\]

Therefore a stable monotone transient cannot by itself establish feedback existence.

If instead the local eigenvalues are a non-real conjugate pair, the characteristic polynomial is strictly positive for every real `phi`. Since `1-phi>0` for every admissible `phi<1`,

\[
\boxed{G(\phi)>0\text{ for every compatible decomposition}.}
\]

Hence oscillatory local dynamics force feedback existence within the generalized model, even though the feedback magnitude remains unidentified.

This is the cleanest qualitative consequence of the nonidentifiability analysis.

## Main theoretical framing

The repository should not lead with the already-standard statement that strong short-term evolution can cancel over long times.

The narrower candidate contribution is

```text
finite individual information structure
    -> state-specific structural selection amplitude

same community-state space + transition geometry
    -> recurrence / temporal filtering of those same rewards

sharp finite sensing bounds
    -> ceilings on attainable selection contrast and feedback gain
    -> restrictions on reachable dynamical phases
```

The theory also keeps two origins of stasis distinct:

1. exogenous cancellation stasis;
2. endogenous restoring stasis.

Oscillatory restoring dynamics are special because they can force feedback existence in the generalized local model.

## Executable layer

- `adaptive_gain/general_response_identifiability.py`
- `adaptive_gain/general_response_scalar_observability.py`
- `adaptive_gain/feedback_existence_identifiability.py`
- `tests/test_general_response_identifiability.py`
- `tests/test_general_response_scalar_observability.py`
- `tests/test_feedback_existence_identifiability.py`
- `validation/general_response_identifiability_v1.json`
- `validation/general_response_scalar_observability_v1.json`
- `validation/feedback_existence_identifiability_v1.json`

## Claim boundary

No novelty is claimed for generic AR(2) inversion, characteristic-polynomial algebra, observability theory, complex-eigenvalue oscillation, or generic fluctuating-selection stasis.

The repository-specific claim is the way these standard pieces constrain interpretation of the exact finite sensing-gap mechanism and its downstream eco-evolutionary dynamics.
