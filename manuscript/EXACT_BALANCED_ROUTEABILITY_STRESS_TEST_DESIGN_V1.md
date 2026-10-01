# Exact-balanced routeability stress test design v1

Status: prospective follow-up / stress-test design. This does **not** replace the simpler four-state experiment and does not modify the frozen V5 submission surface.

## Goal

Test the stronger relational routeability claim under a physical cue environment in which:

- all six binary cues are exactly 5/5 balanced;
- routeable and control architectures use the **same ten physical cue vectors**;
- target prevalence is matched 6:4;
- only the cue-to-action / reward mapping differs.

This design is the finite experimental realization of the quantity–topology orthogonality theorem at routing depth \(d=2\).

---

## 1. Exact task

There are ten represented states:

- four branch pairs \(a_0,b_0,\ldots,a_3,b_3\);
- two dummy states.

There are six binary cue channels:

- route bit 0: \(r_0\);
- route bit 1: \(r_1\);
- branch terminals: \(t_0,t_1,t_2,t_3\).

Every cue has exactly five 0 outcomes and five 1 outcomes.

### Physical cue matrix

| state | \(r_0\) | \(r_1\) | \(t_0\) | \(t_1\) | \(t_2\) | \(t_3\) | routeable target | control target |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| a0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 |
| b0 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 |
| a1 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 |
| b1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 1 |
| a2 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |
| b2 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 |
| a3 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| b3 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 0 |
| dummy 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dummy 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

The control target is:

\[
T_K=0\iff r_0=r_1,
\qquad
T_K=1\iff r_0\ne r_1.
\]

Thus both target maps have six target-0 and four target-1 states.

---

## 2. Exact structural costs

### Routeable architecture

The two routing bits identify the branch, after which only that branch's terminal is needed.

Therefore:

\[
C_A=3.
\]

Each of the four branch terminal cues is uniquely required for one mixed target pair, so every fixed resolver must include all four terminals. The four terminals jointly resolve.

Therefore:

\[
\boxed{(C_A,C_F)=(3,4).}
\]

### Matched control

The two route bits jointly resolve equality versus inequality.

No single cue can resolve the 6:4 target split because every cue outcome partition is 5:5.

Therefore:

\[
\boxed{(C_A,C_F)=(2,2).}
\]

---

## 3. Primary common-budget contrast

Use one common acquisition budget:

\[
\boxed{B=3.}
\]

### Contingent access schedule

All individuals receive exactly three cue observations:

1. \(r_0\);
2. \(r_1\);
3. terminal \(t_j\), where \(j=r_0+2r_1\).

The third cue is therefore selected by the observed routing state.

Under the deterministic table:

- routeable accuracy ceiling = 1.00;
- control accuracy ceiling = 1.00.

### Fixed access schedule

Use the same precommitted three-cue bundle in both architectures:

\[
\boxed{t_0,\ t_1,\ t_2.}
\]

Present the three cues sequentially with timing and persistence matched to the contingent arm; cue identity does not depend on earlier outcomes.

Under a uniform distribution over the ten states:

- routeable Bayes-optimal target accuracy ceiling = 0.80;
- control Bayes-optimal target accuracy ceiling = 1.00.

Thus:

\[
\boxed{
(1.00-0.80)-(1.00-1.00)=0.20.
}
\]

The 0.20 value is an **exact information/decision ceiling contrast**, not a behavioral SESOI.

---

## 4. Why this is a stronger control than the four-state experiment

The four-state experiment is deliberately minimal.

This ten-state stress test adds stronger constraints:

1. every individual cue has identical maximal marginal entropy under the uniform state distribution;
2. the full physical cue matrix is identical between architectures;
3. target prevalence and target entropy are identical;
4. total full-vocabulary target information is identical;
5. the same contingent cue schedule is used in both architectures;
6. the same fixed three-cue schedule is used in both architectures.

The only treatment difference is the target/reward mapping.

Therefore a positive architecture × access interaction cannot be attributed to:
- richness;
- cue number;
- cue prevalence;
- cue entropy;
- physical cue combinations;
- number of observations;
- target prevalence.

It is specifically predicted from action-conditioned decision topology.

---

## 5. Biological implementation

This design is more demanding than the four-state task and should be attempted only after the minimal experiment establishes feasibility.

A candidate artificial-flower implementation would need six independently controllable cue channels.

A possible layout:

- two coarse context/routing features;
- four terminal windows/features.

The physical identities assigned to \(r_0,r_1,t_0,\ldots,t_3\) must be counterbalanced across individuals so that the mathematical role is not confounded with one color, odor, side, shape, or spatial position.

### Presentation

For contingent access:
- reveal both route cues in two matched stages;
- reveal only the branch-selected terminal in stage 3.

For fixed access:
- reveal \(t_0,t_1,t_2\) in three matched stages.

The total number of observations is three in both arms.

Cue persistence should be frozen before confirmatory collection.

---

## 6. Training

Because the architecture contains ten states, full-information training should precede budgeted testing.

Recommended structure:

1. architecture-neutral familiarization with the six physical cue channels;
2. architecture-specific full-information training in which all six cue channels are observable;
3. fixed training dose, not an accuracy-based inclusion threshold;
4. randomized budgeted test after training.

Do not require routeable and control learning curves to be identical before testing; architecture-specific learning is itself treatment-dependent.

---

## 7. Primary endpoint

Same as the minimal experiment:

- 1 = correct target/action within the frozen response window;
- 0 = incorrect action or timeout.

The theoretical ceiling interaction is 0.20.

The behavioral confirmatory hypothesis should remain qualitative/directional unless a separate external SESOI is justified:

\[
H_1:
[p_{R,C}-p_{R,F}]
-
[p_{K,C}-p_{K,F}]
>0.
\]

Do not power the study on 0.20 solely because the deterministic task ceiling is 0.20.

---

## 8. Secondary mechanistic checks

Useful diagnostics:

- accuracy conditional on each routing branch;
- third-cue choice in an autonomous-routing follow-up;
- latency after \(r_0,r_1\);
- whether animals exploit the branch-specific terminal rather than a learned state-specific motor rule;
- transfer to remapped physical cue symbols.

A transfer test is particularly valuable because it distinguishes abstract routing structure from memorization of fixed flower identities.

---

## 9. Experimental hierarchy

### First experiment

Four-state / three-cue minimal routeability test.

Purpose:
- feasibility;
- causal architecture × access × budget result.

### Second experiment

Ten-state / six-cue exact-balanced stress test.

Purpose:
- eliminate marginal cue entropy and physical cue-distribution explanations;
- test the stronger relational theorem.

The second experiment should not be a prerequisite for the first paper.

---

## 10. Executable provenance

Exact task and ceiling calculations:

- adaptive_gain/exact_balanced_routeability_stress_test.py
- tests/test_exact_balanced_routeability_stress_test.py

Underlying theorem:

- adaptive_gain/balanced_quantity_topology_contrast.py
- theory/QUANTITY_TOPOLOGY_ORTHOGONALITY.md

## Claim ceiling

A positive behavioral result would show that action-conditioned routeability matters under a highly constrained matched cue environment.

It would not establish:
- natural prevalence of such exact-balanced architectures;
- evolved niche breadth;
- natural community stability;
- quantitative validity of the deterministic model under noisy cues.
