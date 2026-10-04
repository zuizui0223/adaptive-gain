# Relational routeability — canonical index v1

Status: canonical entry point for the post-freeze math–ecology integration.  
This branch does **not** modify the frozen Evolution Letters V5 initial-submission surface.

## Read this first

1. **Theorem spine**  
   \`theory/RELATIONAL_ROUTEABILITY_THEOREM_SPINE_V1.md\`

   Canonical statement of:
   - relational routeability;
   - exact common-budget corollary;
   - finite pairwise-information controls;
   - summary-sufficiency hierarchy;
   - experiment and measurement consequences.

2. **Readiness / stop rule**  
   \`validation/relational_routeability_readiness_v1.json\`

   Machine-readable current claim ceiling and allowed next work.

---

## Current synthesis manuscript

`manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md`

Current decision-ecology synthesis draft. It contains the exact characterization of fixed cost by static subset information, the 12-state twins with identical complete Shannon entropy vectors but different adaptive costs, unbounded additive direct-product amplification, exact target-relevant decision redundancy, a finite-budget ecological consequence, a temporal predictive-routing extension, and cross-system biological grounding for staged ecological decision making. Retain `MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_3_AMNAT.md` as the pre-strengthening baseline.

Baseline prior-art-positioned draft retained as `manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_2.md`.

---

## Ecology Letters submission surface

Canonical target: **Ecology Letters — Letter**.

- manuscript:
  `manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md`
- submission metadata:
  `manuscript/SUBMISSION_METADATA_ECOLOGY_LETTERS_ROUTEABILITY_V1.md`
- figure legends:
  `manuscript/FIGURE_LEGENDS_RELATIONAL_ROUTEABILITY_V1.md`
- novelty statement:
  `manuscript/NOVELTY_STATEMENT_ECOLOGY_LETTERS_ROUTEABILITY_V1.md`
- cover letter:
  `manuscript/COVER_LETTER_ECOLOGY_LETTERS_ROUTEABILITY_V1.md`
- data accessibility:
  `manuscript/DATA_ACCESSIBILITY_ECOLOGY_LETTERS_ROUTEABILITY_V1.md`
- submission readiness:
  `validation/ecology_letters_routeability_submission_readiness_v1.json`

Current controlled counts:
- abstract: 150 words;
- main text: approximately 4,485 words under the journal definition;
- references: 30;
- main figures: 2.

Do not use the older generic/Theoretical Ecology `SUBMISSION_METADATA_V1.md` for
this submission.

---

## Proof supplement

`manuscript/SUPPLEMENT_RELATIONAL_ROUTEABILITY_PROOFS_V1.md`

Formal analytic proof of the relational theorem/common-budget corollary plus the exact finite verification scope for pairwise controls and the ten-state stress test.

## Mathematical recovery audit

manuscript/MATHEMATICAL_RECOVERY_AUDIT_V1.md

Repository-wide audit from the initial finite-resolution theory through the
exact-balanced companion, temporal/noisy routing, routing-population side line,
eco-evolutionary identifiability, and OU congruence program. The audit records
which results belong in the current paper, Supplement, mathematical companion,
separate papers, or archive. It records temporal/noisy routing as recovered into the current paper's secondary decision-ecology result and assigns every other independent theorem family to Supplement, companion, separate paper, or archive.

---

## Mathematical support

### Relational orthogonality theorem
\`theory/QUANTITY_TOPOLOGY_ORTHOGONALITY.md\`

Core result:
same physical cue matrix, target prevalence/entropy and total full-vocabulary target information can coexist with sharply different adaptive/fixed resolution geometry.

### Static-information / adaptive-access theorem
`theory/STATIC_INFORMATION_ADAPTIVE_ACCESS_THEOREM.md`

Core strengthening: the full named static subset-information function exactly determines `C_F`, yet even the complete Shannon entropy vector does not determine `C_A`. Direct products preserve complete entropic equivalence while amplifying the adaptive-cost difference without bound additively.

### Summary sufficiency ladder
`theory/ROUTEABILITY_SUMMARY_SUFFICIENCY_LADDER.md`

Now includes the missing all-subset-information level and the outcome-resolved Bellman level.

### Executable constructions

- \`adaptive_gain/balanced_quantity_topology_contrast.py\`
- \`adaptive_gain/balanced_pairwise_information_controls.py\`
- `adaptive_gain/exact_balanced_routeability_stress_test.py`
- `adaptive_gain/static_information_adaptive_separation.py`

### Focused tests

- \`tests/test_balanced_quantity_topology_contrast.py\`
- \`tests/test_balanced_pairwise_information_controls.py\`
- `tests/test_exact_balanced_routeability_stress_test.py`
- `tests/test_static_information_adaptive_separation.py`

Focused CI:
\`.github/workflows/quantity-topology-smoke.yml\`

---

## Ecological interpretation

### Canonical synthesis
\`manuscript/BALANCED_ROUTEABILITY_MATH_ECOLOGY_SYNTHESIS_V2.md\`

### Ecological principle audit
\`manuscript/ECOLOGICAL_PRINCIPLE_BLINDNESS_AUDIT_V1.md\`

Separates:
- DIRECT structural consequences;
- MODIFIER-only evolutionary claims;
- NOT-YET-REACHED downstream claims such as diversity–stability.

### Prior-art boundary
`manuscript/RELATIONAL_ROUTEABILITY_PRIOR_ART_AUDIT_V1.md`

### Cross-system biological grounding
`manuscript/BUMBLEBEE_PUBLIC_DATA_ROUTEABILITY_BRIDGE_V1.md`

Canonical quantitative receipt:
`validation/bombus_empirical_convergence_panel_v1.json`

Access-mode interaction:
`validation/yuan_free_cue_acquisition_interaction_v1.json`

Current result: no **single** public dataset identifies the full same-environment branch-specific \(C_A<C_F\) theorem. Public *Bombus* data provide one quantified example of several operations relevant to conditional information use:

- Yuan et al. 2026: 19,200 raw trials; costly need-dependent information acquisition, with a strong difficulty × free-information access-mode interaction;
- Spaethe et al. 2026: secondary-cue recruitment rises from about 0.026 to 0.374 when the primary cue becomes difficult;
- MaBouDi et al. 2025: selective sequential visual sampling;
- Chow et al. 2022: early context switches the later correct action;
- Essenberg et al. 2015: closest branch-specific cue-relevance precedent.

Use the *Bombus* datasets as one quantified example within a broader cross-system biological grounding, not as direct validation of the exact deterministic (C_A,C_F) theorem.

### Bibliography verification
`manuscript/RELATIONAL_ROUTEABILITY_BIBLIOGRAPHY_AUDIT_V1.md`

Core ecology, information-fitness, adaptive-acquisition and extra-entropic references verified against primary/authoritative sources.

### Journal fit
`manuscript/RELATIONAL_ROUTEABILITY_JOURNAL_FIT_AUDIT_V1.md`

Preferred first target: **Ecology Letters (Letter)**, now that the deterministic theorem is paired with a compact public *Bombus* empirical-convergence analysis. **The American Naturalist** remains the natural fallback; Theoretical Ecology remains a lower fallback.


\`manuscript/RELATIONAL_ROUTEABILITY_PRIOR_ART_AUDIT_V1.md\`

Treats as prior art:
- adaptive feature acquisition;
- sequential value of information;
- generic adaptivity gaps;
- uniform separating systems;
- entropy not being a complete operational invariant.

The candidate contribution is the exact ecological composition, not those components.

---

## Figure architecture

`manuscript/RELATIONAL_ROUTEABILITY_FIGURE_PLAN_V1.md`

Implemented main figures:
1. `manuscript/figures/figure_routeability_entropy_access_v1.svg` — complete Shannon entropic equivalence -> different adaptive accessibility;
2. `manuscript/figures/figure_routeability_bombus_bridge_v1.svg` — finite ecological budget + one quantified *Bombus* example -> prospective matched routeability experiment.

Figure integrity/value receipt:
`validation/routeability_main_figures_v1.json`.

---

## Measurement

### Routeability measurement protocol
\`manuscript/ROUTEABILITY_MEASUREMENT_PROTOCOL_V1.md\`

Minimum empirical structural object:

\[
(W,T,Q,c)
\]

with a declared focal action, cue-state table and cue costs/timing.

Rule:

\[
\boxed{\text{Measure the action-conditioned cue table first; summarize it second.}}
\]

---

## Experimental program

### Experiment 1 — minimal causal test
\`manuscript/ROUTEABILITY_EXPERIMENT_DESIGN_V1.md\`

Four states, three cues.

Purpose:
- behavioral feasibility;
- direct architecture × access × budget test;
- exact localization to the routeability-sensitive budget window.

### Experiment 2 — exact-balanced stress test
\`manuscript/EXACT_BALANCED_ROUTEABILITY_STRESS_TEST_DESIGN_V1.md\`

Ten states, six cues, every cue exactly 5/5 balanced.

Exact deterministic costs:

\[
(C_A,C_F)_R=(3,4),\qquad
(C_A,C_F)_K=(2,2).
\]

At common budget \(B=3\):

\[
\boxed{\text{architecture}\times\text{access ceiling interaction}=1/5.}
\]

This is a stronger follow-up, not a prerequisite for Experiment 1.

---

## Validation receipts

- `validation/independent_section5_audit_v1.json`
- `validation/independent_temporal_routing_audit_v1.json`
- `validation/temporal_routing_threshold_v1.json`
- `validation/noisy_temporal_routing_factorization_v1.json`
- \`validation/balanced_quantity_topology_contrast_v1.json\`
- \`validation/balanced_pairwise_information_controls_v1.json\`
- \`validation/exact_balanced_routeability_stress_test_v1.json\`
- `validation/relational_routeability_readiness_v1.json`
- `validation/static_information_adaptive_separation_v1.json`
- `validation/bombus_public_data_component_receipt_v1.json`
- `validation/bombus_empirical_convergence_panel_v1.json`
- `validation/yuan_free_cue_acquisition_interaction_v1.json`

Repository-wide CI is green on Python 3.10 / 3.11 / 3.12 for the integrated decision-ecology branch, including the static-information twins, direct-product checks, temporal/noisy routing tests, witness audit and certificate-ladder audit.

---

## Claim hierarchy

### Established in the deterministic model

\[
\text{same cue environment}
+
\text{different action-conditioned topology}
\Rightarrow
\text{different }(C_A,C_F).
\]

With a common hard budget:

\[
\text{same cue environment}
+
\text{same budget}
+
\text{different topology}
\Rightarrow
\text{different feasible access regime}.
\]

### Ecologically direct

- information amount versus acquisition architecture;
- processing burden at fixed nominal niche breadth;
- behavioral accessibility under finite observation budgets.

### Modifier only

- heterogeneity → evolved niche breadth;
- specialist/generalist evolutionary outcomes.

### Not yet reached

- diversity–stability;
- community resilience;
- ecosystem-function stability.

---

## V5 boundary

Do **not** reopen frozen V5 for these post-freeze developments.

The safe V5-level interpretation is:

> conditional decision topology is a relational ecological axis not determined by strong distributional summaries of heterogeneity or information, and finite ecological budgets expose its consequences.

---

## Next-paper boundary

General stochastic expected-loss project beyond the recovered minimal noisy temporal model:

\[
J(\pi)
=
\mathbb E[C_\pi]
+
\lambda\mathbb E[L(A,T)].
\]

Main question:

> does the quantity/topology separation survive noisy cues, allowed error and expected-loss optimization?

This is not required for the deterministic paper.

## Stop rule

No new deterministic theorem family.

Allowed work now:
- editorial compression and Ecology Letters packaging;
- render the two canonical figures, including the frozen Bombus public-data panel;
- execute the prospective four-state routeability experiment in an experimentally tractable decision system; *Bombus* is one candidate, not a required taxon;
- only then consider the ten-state stress test;
- develop stochastic expected-loss theory as a separate project.
