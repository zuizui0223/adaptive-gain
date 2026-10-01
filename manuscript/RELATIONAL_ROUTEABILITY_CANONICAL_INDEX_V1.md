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

## Mathematical support

### Relational orthogonality theorem
\`theory/QUANTITY_TOPOLOGY_ORTHOGONALITY.md\`

Core result:
same physical cue matrix, target prevalence/entropy and total full-vocabulary target information can coexist with sharply different adaptive/fixed resolution geometry.

### Summary sufficiency ladder
\`theory/ROUTEABILITY_SUMMARY_SUFFICIENCY_LADDER.md\`

Tracks which increasingly rich summaries still fail to identify conditional decision topology.

### Executable constructions

- \`adaptive_gain/balanced_quantity_topology_contrast.py\`
- \`adaptive_gain/balanced_pairwise_information_controls.py\`
- \`adaptive_gain/exact_balanced_routeability_stress_test.py\`

### Focused tests

- \`tests/test_balanced_quantity_topology_contrast.py\`
- \`tests/test_balanced_pairwise_information_controls.py\`
- \`tests/test_exact_balanced_routeability_stress_test.py\`

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
\`manuscript/RELATIONAL_ROUTEABILITY_PRIOR_ART_AUDIT_V1.md\`

Treats as prior art:
- adaptive feature acquisition;
- sequential value of information;
- generic adaptivity gaps;
- uniform separating systems;
- entropy not being a complete operational invariant.

The candidate contribution is the exact ecological composition, not those components.

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

- \`validation/balanced_quantity_topology_contrast_v1.json\`
- \`validation/balanced_pairwise_information_controls_v1.json\`
- \`validation/exact_balanced_routeability_stress_test_v1.json\`
- \`validation/relational_routeability_readiness_v1.json\`

Focused quantity/topology tests pass on Python 3.10 / 3.11 / 3.12.

The repository-wide test workflow still has an unrelated legacy manuscript phrase assertion failure; it is not evidence against the matched constructions.

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

Separate stochastic expected-loss project:

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
- write/polish;
- tighten prior art;
- execute the four-state experiment;
- only then consider the ten-state stress test;
- develop stochastic expected-loss theory as a separate project.
