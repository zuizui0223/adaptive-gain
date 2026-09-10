# Supplementary Information v1

## Purpose

This supplement follows the hierarchical result order of `manuscript/MANUSCRIPT_V1.md`. It is an index and proof map, not a second manuscript. Main-text claims must be traceable from result statement -> proof note -> executable implementation -> validation receipt.

The hierarchy is deliberate: S1 is the principal reachability theorem, S2 the supporting structural-temporal envelope, S3 the feedback-existence diagnostic theorem, and S4 the mechanistic stasis proposition. These should not be presented as four equal novelty claims.

## S1. Principal reachability theorem: required dynamics imply minimum or Pareto-minimal finite decision/separation structure

### Main-text result
A required integer structural gap `q` implies an exact binary first corner and, for bounded arity `b>2`, a generally multi-point Pareto frontier over represented-world count, declared-query count, and productive-frontier obligations. Under the declared structural feedback lift, a required local dynamical phase therefore imposes a minimum or Pareto-minimal finite deterministic decision/separation structure. This is a discrete structural result, not a lower bound on Shannon mutual information.

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

### Canonical Pareto example
For `q=3,b=4`, `(8,5,5)` and `(7,6,6)` are both nondominated. The example is retained in the main text because it shows that reducing query/frontier burden and reducing represented-world count are not the same objective.

### Static support inherited from the repository
The main text uses but does not claim priority for bounded-arity rooted-tree extremal counting, fixed-versus-adaptive separation costs, and productive-frontier obligations. Their detailed proofs, private-pair constructions, continuation quotients, and certificate ladders remain outside the ecological narrative.

### Information-theory boundary
The reverse direction is not itself a novelty claim. Moffett & Eckford (2022) already derive minimum mutual-information requirements for target population growth and average selection coefficients using rate-distortion theory, within the broader fitness-value-of-information literature. S1 instead minimizes a finite deterministic decision/separation architecture and returns componentwise minima or a Pareto set over `(n,m,E)` for a required local feedback phase. Do not describe S1 as a generic `minimum information` theorem.

### What remains supplementary
- exact recurrence for `F_b(n,h)`;
- private-pair forest construction;
- solver-cap separation between small exact audits and large constructive audits;
- binary logarithmic bracket;
- Pareto dominance checks;
- integer-gap ladder edge cases.

## S2. Supporting structural-temporal extremal envelope

### Main-text result
For finite recurrent structural rewards lifted by `s_i=lambda*g_i-kappa` and a finite ergodic reversible community chain,

\[
\sigma_{\rm eff}^2\le\frac{(\lambda g_{\max})^2}{4}\frac{1+r_{\max}}{1-r_{\max}}.
\]

The bound is sharp because an equality witness exists, but it is an extremal envelope rather than a generic predictor of realized multi-state variance.

### Tightness decomposition
Writing

\[
f(r)=\frac{1+r}{1-r},
\qquad
B=\frac{(\lambda g_{\max})^2}{4}f(r_{\max}),
\]

and `tilde w_j=w_j/Var_pi(s)` when the stationary reward variance is positive,

\[
\frac{\sigma_{\rm eff}^2}{B}
=
\frac{4\operatorname{Var}_\pi(s)}{(\lambda g_{\max})^2}
\frac{\sum_j\widetilde w_j f(r_j)}{f(r_{\max})}.
\]

The first factor records range/variance saturation and the second reward alignment with the slowest algebraic mode. Both must equal one for equality in the headline bound.

The executable audit helper uses the equivalent observable factorization

\[
\frac{\sigma_{\rm eff}^2}{B}
=
\frac{\operatorname{Var}_\pi(s)}{V_{\max}}
\frac{\sigma_{\rm eff}^2}{\operatorname{Var}_\pi(s)A_{\max}},
\]

where `V_max=(lambda*g_max)^2/4` and `A_max=(1+r_max)/(1-r_max)`. This avoids requiring an explicit eigendecomposition merely to audit how much slack comes from reward-range saturation versus temporal mode alignment.

### Proof source
- `theory/STRUCTURAL_SPECTRAL_JOINT_BOUND.md`
- `theory/STRUCTURAL_REWARD_MODE_ALIGNMENT.md`

### Executable source
- `adaptive_gain/structural_spectral_joint_bounds.py`
- `tests/test_structural_spectral_joint_bounds.py`

### Validation receipts
- `validation/structural_spectral_joint_bound_v1.json` — original sharp-ceiling validation;
- `validation/structural_spectral_slack_v2.json` — deterministic equality and loose-factorization checks.

### What remains supplementary
- reversible-chain spectral decomposition details;
- equality construction;
- random reversible-chain audit;
- asymptotic crossover corollary details.

## S3. Diagnostic theorem: model-compatible oscillation forces feedback existence

### Main-text result
Stable real nonnegative modes can admit a zero-feedback decomposition. A non-real conjugate eigenpair forces `G>0` for every admissible real `phi<1` only after the observed invariants are shown to lie inside the declared generalized persistence domain.

The parent generalized model permits `0<=alpha<=1` and requires `0<=phi<1`. Since `T=alpha+phi`, at least one persistence split exists exactly when

\[
0\le T<2.
\]

For a complex eigenpair satisfying this compatibility condition, every model-feasible decomposition has `G>0`; feedback magnitude remains unidentified. If `T<0` or `T>=2`, the correct conclusion is model incompatibility rather than feedback existence.

The neutral real boundary `alpha=1` remains permitted. Thus a real mode exactly at one can be model-feasible in a zero-feedback decomposition when the other eigenvalue serves as `phi`, even though that case is outside the asymptotically stable monotone-return corollary. A double unit root is infeasible because it would require `phi=1`.

### Exact gain-infimum helper
For

\[
G(\phi)=\frac{\phi^2-T\phi+D}{1-\phi},
\qquad
R=1-T+D,
\]

setting `x=1-phi` gives `G=R/x+(T-2)+x` on `0<x<=1`. This public helper optimizes over the unit community-memory interval and does not additionally restrict the implied `alpha=T-phi`. Therefore

\[
\inf_{0\le\phi<1}G(\phi)=
\begin{cases}
-\infty,&R<0,\\
T-2,&R=0,\\
T-2+2\sqrt R,&0<R\le1,\\
D,&R>1.
\end{cases}
\]

This piecewise expression is implemented directly and regression-tested, including the `R<0` and excluded-boundary `R=0` cases.

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
- `validation/feedback_existence_identifiability_v1.json` — original 200,000-model random audit;
- `validation/feedback_existence_boundary_regression_v2.json` — deterministic `R<0`, `R=0`, interior, `R>1`, `alpha=1`, double-unit-root, and complex-outside-model checks;
- `validation/general_response_identifiability_v1.json`;
- `validation/general_response_scalar_observability_v1.json`.

### What remains supplementary
- characteristic-polynomial derivation;
- admissible decomposition family;
- 200,000-model numerical audit;
- scalar nonidentifiability algebra;
- critical-slowing and AR(2) inversion details.

## S4. Mechanistic proposition: two origins of stasis

### Main-text result
Neutral cancellation stasis and attractive restoring stasis can both yield little retained long-term change but have different return-map structure.

This distinction is retained for biological interpretation. The identity-map versus contraction algebra is standard and is not presented as a separate mathematical novelty claim.

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

## S5. Claim and provenance discipline

The canonical paper-level result hierarchy is `theory/PAPER_THEOREM_SPINE.md`. The ecological claim boundary is recorded in:

- `manuscript/NOVELTY_PARAGRAPH_V1.md`;
- `manuscript/PRIOR_ART_AUDIT_V2.md`;
- `manuscript/FINAL_PRIORITY_SEARCH_LOG.md`;
- `manuscript/LITERATURE_POSITIONING.md`.

No novelty is claimed for generic information use, sequential cue acquisition, the fitness value of information, minimum Shannon/mutual-information requirements for target fitness or selection, generic evolutionary information thresholds, evolved sensing architecture, test cover, decision trees, adaptivity gaps, bounded-arity tree counting, fluctuating selection, temporal autocorrelation, eco-evolutionary feedback, Jury/Schur stability, spectral formulas, identity maps versus contractions, or generic nonidentifiability.

The novelty boundary is the exact **discrete** ecological composition from a required local dynamical regime through a structural adaptive/fixed gap to a minimum/Pareto-minimal finite decision/separation architecture, with the recurrence envelope as a supporting result.

## S6. Explicit exclusions

This supplement does not extend the main paper into observation design, stochastic finite-sample identification, continuous compatible sets, unequal acquisition costs, noisy cue likelihoods, multivariate quantitative genetics, mutation/migration/drift, or global nonlinear bifurcation theory.

## S7. Reproducibility entry points

Run the repository test suite and the two existing audit scripts from the repository root. The frozen mathematical baseline is main commit `569abe805cedc3cee9eeebc4a8aa9410efc12c87`; the submission-polish branch changes claim wording and bibliography, not the executable theorem implementation.
