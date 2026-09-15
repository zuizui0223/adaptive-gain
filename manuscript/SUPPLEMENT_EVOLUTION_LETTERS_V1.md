# Supplementary Information - Evolution Letters v1

## Purpose and claim ceiling

This Supplement follows `MANUSCRIPT_EVOLUTION_LETTERS_V2.md`. It is a proof-and-reproducibility map, not a second narrative manuscript and not a source of additional headline claims. The main Letter has four layers: (S1) a nonlinear no-go theorem, (S2) transport of the required between-state contrast to a finite high-gap sensing architecture, (S3) ecological recurrence as spectral filtering, and (S4) a model-conditional feedback-existence diagnostic.

The claim ceiling is unchanged throughout: the nonlinear result supplies a necessary exclusion bound, not generic sufficiency; a state-specific gap is not the same object as the between-state contrast; finite deterministic sensing architecture is not Shannon information; the constructive linear lift is not empirical validation; and a slow ecological mode does not imply a large evolutionary effect without reward-mode alignment.

## S1. Nonlinear sensing-to-selection no-go theorem

### Main-text statement

For two ecological states, define the nonnegative state-specific sensing gaps

\[
g_i=C_F(i)-C_A(i)\ge0
\]

and the ordered between-state contrast

\[
\Delta g=g_2-g_1\ge0.
\]

Let the state-specific selection contribution be `s_i=f(g_i)-kappa`, where `f` is nondecreasing and has bounded marginal effect over the relevant gap domain,

\[
0\le f(g_2)-f(g_1)\le L\Delta g.
\]

With positive feedback-per-selection scale `B`, the local restoring feedback gain obeys

\[
0\le G\le BL\Delta g.
\]

If complex local return requires `G>G_osc`, then a necessary condition is

\[
\Delta g>\frac{G_{\mathrm{osc}}}{BL}.
\]

Therefore, if an admissible architecture class imposes maximum possible between-state contrast `Delta g_max` satisfying

\[
BL\Delta g_{\max}\le G_{\mathrm{osc}},
\]

that class cannot generate the requested oscillatory regime for any lift in the declared monotone-Lipschitz class.

Crossing the bound is only necessary. A nonlinear lift may realize less selection contrast than its allowed marginal ceiling, so architecture above the bound does not generically guarantee oscillation.

### Theory, implementation, tests and receipt

- `theory/NONLINEAR_LIFT_NO_GO_V2.md`
- `adaptive_gain/nonlinear_feedback_reachability.py`
- `tests/test_nonlinear_feedback_reachability.py`
- `validation/nonlinear_lipschitz_no_go_v2.json`

### Constructive special case

The additive cue-acquisition model `s_i=lambda*g_i-kappa` is retained only as the constructive special case that can attain the marginal ceiling. It is not required by the no-go theorem.

## S2. From required contrast to finite sensing architecture

### Transport to a high-gap state

If `Delta g>=q` and all state gaps are nonnegative, then the high state satisfies `g_i>=q`. The existing sharp single-task finite bounds can therefore be applied to that state.

For binary unit-cost sensing, with

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\},
\]

the exact first componentwise gap-capable corner is

\[
(n^*,m^*,E^*)=(h_2^*(q)+q+1,\;h_2^*(q)+q,\;h_2^*(q)+q).
\]

Thus `q=2` gives `(n,m,E)=(6,5,5)`.

For maximum cue arity `b>=2`, the separate minima are

\[
m_{\min}=E_{\min}=q+h_b^*(q),
\qquad
n_{\min}=q+h_2^*(q)+1,
\]

where

\[
h_b^*(q)=\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\}.
\]

For `b>2`, these componentwise minima need not be attained by the same task, so the exact requirement is generally a Pareto frontier rather than one scalar minimum. The canonical `q=3,b=4` example has nondominated points `(7,6,6)` and `(8,5,5)`.

### Binary and bounded-arity sources

- `theory/GENERAL_BINARY_DYNAMIC_SCOPE_THRESHOLD.md`
- `theory/SHARP_BINARY_OSCILLATION_SCOPE_THRESHOLD.md`
- `theory/ARITY_GAP_PARETO.md`
- `theory/DYNAMIC_ARITY_PARETO.md`
- `adaptive_gain/binary_oscillation_scope_formula.py`
- `adaptive_gain/arity_gap_pareto.py`
- `adaptive_gain/arity_dynamic_scope.py`
- `tests/test_binary_oscillation_scope_formula.py`
- `tests/test_arity_gap_pareto.py`
- `tests/test_arity_dynamic_scope.py`
- `validation/general_binary_dynamic_scope_threshold_v1.json`
- `validation/structural_oscillation_scope_threshold_v1.json`
- `validation/arity_gap_pareto_v1.json`
- `validation/dynamic_arity_pareto_v1.json`

### Detailed finite material retained outside the main Letter

Exact finite recurrences, private-pair constructions, continuation quotients, exhaustive enumeration, solver/certificate machinery, proof DAGs and equality witnesses remain repository-level proof support. They are not independent biological claims.

## S3. Ecological recurrence as spectral filtering

Let ecological states evolve as a finite ergodic reversible Markov chain with stationary distribution `pi`. If the centered state-specific selection reward is expanded over nonstationary ecological modes, the asymptotic variance rate is

\[
\sigma_{\mathrm{eff}}^2=\sum_r w_r\frac{1+r_r}{1-r_r},
\]

where `r_r` is a nontrivial ecological eigenvalue and `w_r` is the squared projection of the centered reward onto that mode.

In the linear acquisition-cost special case, if `0<=g_i<=g_max`, then

\[
\sigma_{\mathrm{eff}}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
\]

This bound is extremally sharp but not a generic realized-variance predictor. Its slack separates use of the available reward range from alignment of reward variation with the slow ecological mode. Ecological persistence alone is therefore insufficient for a large long-run evolutionary effect.

### Sources

- `theory/STRUCTURAL_SPECTRAL_JOINT_BOUND.md`
- `theory/STRUCTURAL_REWARD_MODE_ALIGNMENT.md`
- `adaptive_gain/structural_spectral_joint_bounds.py`
- `tests/test_structural_spectral_joint_bounds.py`
- `validation/structural_spectral_joint_bound_v1.json`
- `validation/structural_spectral_slack_v2.json`

## S4. Diagnostic boundary: compatible oscillation forces nonzero feedback

Stable monotone return can admit a decomposition with `G=0`. By contrast, for a non-real conjugate local eigenpair that is compatible with the declared persistence domain `0<=alpha<=1`, `0<=phi<1`, every model-compatible decomposition has `G>0`.

Compatibility must be checked first. With trace `T=alpha+phi`, at least one allowed persistence split exists only for `0<=T<2`. Outside that range, the correct conclusion is model incompatibility, not feedback existence.

This diagnostic identifies feedback existence only. It does not identify feedback magnitude, the separate persistence parameters, or the causal contribution of sensing architecture.

### Sources

- `theory/FEEDBACK_EXISTENCE_FROM_OSCILLATION.md`
- `theory/GENERAL_RESPONSE_IDENTIFIABILITY.md`
- `adaptive_gain/feedback_existence_identifiability.py`
- `adaptive_gain/general_response_identifiability.py`
- `tests/test_feedback_existence_identifiability.py`
- `tests/test_general_response_identifiability.py`
- `validation/feedback_existence_identifiability_v1.json`
- `validation/feedback_existence_boundary_regression_v2.json`
- `validation/general_response_identifiability_v1.json`

## S5. Information-theory and novelty boundary

The Letter does not claim a new generic minimum-information principle. Fitness-value-of-information and rate-distortion work already address how information can change growth or selection and can derive minimum mutual-information requirements for target outcomes. The object here is different: a finite deterministic decision/separation architecture and the adaptive-versus-fixed structural gap it permits within ecological states.

The paper-level novelty claim is therefore restricted to the composition

```text
requested local feedback regime
-> required between-state structural contrast
-> at least one required high-gap ecological state
-> exact or Pareto-minimal finite sensing architecture
```

within the declared model class, with ecological recurrence retained as a supporting temporal filter.

Canonical claim-boundary records are:

- `manuscript/PRIOR_ART_AUDIT_V2.md`
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`
- `manuscript/LITERATURE_POSITIONING.md`
- `manuscript/HIGHER_TIER_INTEGRATION_MAP_V2.md`

## S6. Explicit exclusions

Neither the main Letter nor this Supplement extends the result to noisy Bayesian cue channels, unequal acquisition costs, stochastic finite-population genetics, mutation, migration, drift, demographic stochasticity, multivariate genetics, continuous compatible-set inference, or global nonlinear bifurcation theory.

## S7. Reproducibility

The repository test suite, witness audit and certificate audit are the executable entry points. The Evolution Letters scientific-and-visual freeze validated on 2026-09-15 is recorded in `manuscript/EVOLUTION_LETTERS_READINESS_V1.json`. The canonical Letter manuscript is `manuscript/MANUSCRIPT_EVOLUTION_LETTERS_V2.md`; the canonical Letter figure legends and alt text are `manuscript/FIGURE_LEGENDS_EVOLUTION_LETTERS_V2.md`.
