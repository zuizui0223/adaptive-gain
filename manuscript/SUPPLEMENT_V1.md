# Supplementary Information v1

## Purpose

This supplement follows the four-theorem order of `manuscript/MANUSCRIPT_V1.md`. It is an index and proof map, not a second manuscript. Main-text claims must be traceable from theorem statement -> proof note -> executable implementation -> validation receipt.

## S1. Structural-temporal joint ceiling

### Main-text result
For finite recurrent structural rewards lifted by `s_i=lambda*g_i-kappa` and a finite ergodic reversible community chain,

\[
\sigma_{\rm eff}^2\le\frac{(\lambda g_{\max})^2}{4}\frac{1+r_{\max}}{1-r_{\max}}.
\]

### Proof source
- `theory/STRUCTURAL_SPECTRAL_JOINT_BOUND.md`

### Executable source
- `adaptive_gain/structural_spectral_joint_bounds.py`
- `tests/test_structural_spectral_joint_bounds.py`

### Validation receipt
- `validation/structural_spectral_joint_bound_v1.json`

### What remains supplementary
- reversible-chain spectral decomposition details;
- equality construction;
- random reversible-chain audit;
- asymptotic crossover corollary details.

## S2. Required dynamics imply minimum or Pareto-minimal information complexity

### Main-text result
A required integer structural gap `q` implies an exact binary first corner and, for bounded arity `b>2`, a generally multi-point Pareto frontier over world count, query count, and productive-frontier obligations.

### Binary theorem sources
- `theory/GENERAL_BINARY_DYNAMIC_SCOPE_THRESHOLD.md`
- `theory/SHARP_BINARY_OSCILLATION_SCOPE_THRESHOLD.md`
- `adaptive_gain/binary_oscillation_scope_formula.py`
- `tests/test_binary_oscillation_scope_formula.py`
- `validation/general_binary_dynamic_scope_threshold_v1.json`
- `validation/structural_oscillation_scope_threshold_v1.json`

### Bounded-arity theorem sources
- `theory/ARITY_GAP_PARETO.md`
- `theory/DYNAMIC_ARITY_PARETO.md`
- `adaptive_gain/arity_gap_pareto.py`
- `adaptive_gain/arity_dynamic_scope.py`
- `tests/test_arity_gap_pareto.py`
- `tests/test_arity_dynamic_scope.py`
- `validation/arity_gap_pareto_v1.json`
- `validation/dynamic_arity_pareto_v1.json`

### Downstream reachability source
- `adaptive_gain/structural_oscillation_reachability.py`
- `tests/test_structural_oscillation_reachability.py`

### Static support inherited from the repository
The main text uses but does not claim priority for bounded-arity rooted-tree extremal counting, fixed-versus-adaptive separation costs, and productive-frontier obligations. Their detailed proofs, private-pair constructions, continuation quotients, and certificate ladders remain outside the ecological narrative.

### What remains supplementary
- exact recurrence for `F_b(n,h)`;
- private-pair forest construction;
- solver-cap separation between small exact audits and large constructive audits;
- binary logarithmic bracket;
- Pareto dominance checks;
- integer-gap ladder edge cases.

## S3. Two origins of stasis

### Main-text result
Neutral cancellation stasis and attractive restoring stasis can both yield little retained long-term change but have different return-map structure.

### Theory source
- `theory/TWO_ORIGINS_OF_STASIS.md`

### Executable source
- `adaptive_gain/stasis_mechanisms.py`
- `tests/test_stasis_mechanisms.py`

### Validation receipt
- `validation/stasis_mechanisms_v1.json`

### What remains supplementary
- periodic-map derivation;
- neutral multiplier proof;
- real versus complex attractive fixtures;
- exact transient-period calculations.

## S4. Oscillation forces feedback existence within the generalized local model

### Main-text result
Real nonnegative stable modes can admit a zero-feedback decomposition, whereas a non-real conjugate eigenpair forces `G>0` for every admissible real `phi<1` within the declared model class.

### Theory sources
- `theory/FEEDBACK_EXISTENCE_FROM_OSCILLATION.md`
- `theory/GENERAL_RESPONSE_IDENTIFIABILITY.md`
- `theory/SCALAR_TRANSIENT_OBSERVABILITY.md` only for the interpretation limit; no observation-design program is imported.

### Executable sources
- `adaptive_gain/feedback_existence_identifiability.py`
- `adaptive_gain/general_response_identifiability.py`
- `adaptive_gain/general_response_scalar_observability.py`
- `tests/test_feedback_existence_identifiability.py`
- `tests/test_general_response_identifiability.py`
- `tests/test_general_response_scalar_observability.py`

### Validation receipts
- `validation/feedback_existence_identifiability_v1.json`
- `validation/general_response_identifiability_v1.json`
- `validation/general_response_scalar_observability_v1.json`

### What remains supplementary
- characteristic-polynomial derivation;
- admissible decomposition family;
- 200,000-model numerical audit;
- scalar nonidentifiability algebra;
- critical-slowing and AR(2) inversion details.

## S5. Claim and provenance discipline

The canonical paper-level theorem hierarchy is `theory/PAPER_THEOREM_SPINE.md`. The ecological claim boundary is recorded in:

- `manuscript/NOVELTY_PARAGRAPH_V1.md`;
- `manuscript/PRIOR_ART_AUDIT_V2.md`;
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`.

No novelty is claimed for generic information use, sequential cue acquisition, test cover, decision trees, adaptivity gaps, bounded-arity tree counting, fluctuating selection, temporal autocorrelation, eco-evolutionary feedback, Jury/Schur stability, spectral formulas, or generic nonidentifiability.

## S6. Explicit exclusions

This supplement does not extend the main paper into observation design, stochastic finite-sample identification, continuous compatible sets, unequal acquisition costs, noisy cue likelihoods, multivariate quantitative genetics, mutation/migration/drift, or global nonlinear bifurcation theory.

## S7. Reproducibility entry points

Run the repository test suite and the two existing audit scripts from the repository root. The current paper branch is designed so that theorem statements, executable implementations, tests, and validation receipts remain synchronized under CI.
