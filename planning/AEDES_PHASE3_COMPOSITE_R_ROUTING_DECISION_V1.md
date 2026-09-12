# Aedes Phase 3 — composite-R routing decision v1

## Purpose

Define the decisive causal interpretation after Phase 1 state manipulation and Phase 2 B-channel validation.

This document is execution planning only. It cannot rescue or modify the frozen v1 task. In particular, if the biology requires multiple separately acquired internal-state information sources, the correct outcome is **v1 rejection and a prospectively defined v2**, not retroactive expansion of R.

## Why this decision is needed

The current literature already suggests at least two mechanistically distinct state components:

1. NPF/RYamide/NPYLR7 signaling causally regulates host attraction and host-seeking suppression;
2. egg maturation plus the circadian clock gene `cycle` controls the timing of mature-gravid hyperactivity and nocturnal humidity/oviposition-site seeking.

The 2025 post-biting reprogramming work shows that humidity seeking emerges around day 3 post-blood meal, is concentrated in an approximately 5-h post-dusk window, and loses its normal temporal organization in `cycle` mutants. Direct freshwater placement preserves egg-laying competence, separating search behavior from the ability to lay eggs.

Therefore a simple observation that one pathway controls A and another controls B does not establish the frozen single-query role R.

## Frozen v1 requirement

For v1 empirical admission, `R` must be defensible as **one organism-level state information source inside one shared decision architecture**.

Its molecular determinants may be multiple, but the decision system must have a biologically meaningful integrated state representation rather than two separately queried branch controllers that the model has collapsed for convenience.

If the evidence instead supports multiple independently used state signals, v1 fails comparator/task semantics and a new finite task must be declared before new data are used to estimate gain.

## Phase-3 perturbation axes

### H-side state perturbation

Use the Phase-1 validated NPYLR7 pharmacological manipulation as a controlled host-suppression perturbation.

This provides a causal test of one candidate component of R without blood-derived nutrients.

### O-side state/timing perturbation

Use natural mature-gravid timing as the primary frozen endpoint.

Where access permits, use `cycle` perturbation only as a mechanistic diagnostic for B timing/search state. It is **not** automatically another R query and must not be inserted into v1 cost accounting after the fact.

## Core measurements

Across the relevant endpoint/state conditions, measure:

- A sensory response under the frozen acidic-host-cue condition;
- A target-level behavioral dependency;
- B Moist-Cell/humidity response where feasible;
- B site-search/target-level dependency;
- locomotion/arousal;
- egg maturity and egg retention;
- circadian phase;
- direct-placement egg-laying competence for O-side search deficits.

Dependency, not response amplitude, remains the central quantity.

## Prospective causal outcome classes

### R0 — host suppression only

NPYLR7 activation reduces host seeking/A dependence, but B response/dependency is unchanged.

Interpretation:

- NPYLR7 is one host-suppression component;
- it is insufficient for the full H-to-O routing transition;
- `state_routing_causality_qualified=False` for v1.

This is the key early negative outcome already frozen conceptually.

### R1 — independent branch controllers

H-side A dependency is controlled by NPYLR7-related signaling, while O-side B dependency/timing is controlled by egg-maturity/circadian mechanisms such as `cycle`, with no evidence of a common integrated decision-state representation.

Interpretation:

- real biological state dependence exists;
- real branch-specific sensory control exists;
- the frozen single-R v1 representation is not biologically qualified.

Action:

**reject v1 empirical admission.** If scientifically worthwhile, define a new v2 prospectively with multiple state information sources and recompute `C_A`, `C_F`, and comparator semantics before collecting decisive v2 data.

Do not call R1 a positive adaptive-gain result for v1.

### R2 — convergent modulation without integrated readout

Multiple state perturbations alter A/B relative dependency in a coordinated way, but there is no evidence that the organism uses one integrated state representation before choosing terminal information.

Interpretation:

- strong state-dependent sensory reconfiguration;
- comparator semantics remain unresolved.

Action:

v1 remains unadmitted until a shared-architecture state representation is justified.

### R3 — candidate integrated state routing

A prospectively identified organism-level state readout or shared circuit representation predicts/mediates the A/B dependency switch, and causal manipulation of upstream state components moves that representation and the downstream dependency pattern together.

Required features:

- the state readout is not merely an experimenter label;
- it is available to the shared decision architecture;
- changes in it precede or mediate the terminal dependency shift;
- A/B causal channel controls remain intact;
- target behavior is not explained solely by locomotor, egg-maturity or motor-output changes.

Interpretation:

candidate support for `comparator_semantics_qualified=True` and `state_routing_causality_qualified=True`, subject to the other frozen empirical admission gates.

### R4 — fully admitted v1 routing

R3 plus:

- frozen task measurement succeeds;
- target ontology and cost semantics pass;
- same-system terminal-channel causality passes;
- exact observed finite task yields positive gap under the preregistered semantics.

Only R4 licenses the v1 claim of positive adaptive gap with causal context routing.

## Role of `cycle`

`cycle` is especially useful as a **falsification/diagnostic perturbation**, not as a convenient replacement for R.

Published data show:

- non-blood-fed females have low humidity seeking;
- mature-gravid females show strong rhythmic humidity seeking after dusk;
- `cycle` mutants lose normal temporal organization of this behavior;
- long-range site search and reproductive efficiency are impaired when search is required;
- direct placement on freshwater retains egg-laying competence.

If `cycle` selectively changes O-side timing/search while NPYLR7 selectively changes H-side host suppression, that pattern favors R1 rather than R3 unless a common downstream integrated state representation is demonstrated.

## v2 trigger

Start a new version only if v1 is rejected because biology requires multiple state sources.

A v2 declaration must occur **before** opening decisive v2 outcome data and must specify:

- the new state-query vocabulary;
- costs/availability of each state source;
- whether state sources are acquired sequentially, constitutively available, or jointly encoded;
- new fixed-comparator semantics;
- new targets/worlds if needed;
- exact recomputed `C_A`, `C_F`, and gap;
- new falsification controls.

v2 must not inherit `g=1` by assumption.

## Stop rules

- do not label NPYLR7 and `cycle` as two parts of one free R without evidence of integration;
- do not count upstream molecular determinants as separate queries unless the organism separately acquires/uses them in the decision problem;
- do not add new state signals to v1 after observing R0/R1/R2;
- do not infer shared routing from correlated endpoint timing alone;
- do not claim v1 positive adaptive gain unless R4 is reached.

## Literature anchor

Post-biting behavioral reprogramming study (PMID 41379618): mature eggs coincide with nocturnal hyperactivity/humidity seeking; `cycle` is required for normal temporal organization and efficient active site search, with direct egg-laying competence controls separating search from oviposition ability.

## Decision value

This protocol makes an otherwise ambiguous result scientifically useful:

- if one integrated R exists, v1 can advance;
- if H and O are controlled by distinct internal-state channels, that is a clean falsification of v1 and directly determines the architecture of a future v2.

Either result increases information; neither licenses post-hoc rescue of the frozen task.
