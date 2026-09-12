# Aedes prospective adaptive-gain experiment v1

## Objective

Test, prospectively, whether the *Aedes aegypti* gonotrophic state switch can instantiate the finite four-world adaptive-gain task without post-hoc recoding.

The experiment has two distinct goals that must not be conflated:

1. **finite-task admission:** does a frozen ecological decision problem have `C_A<C_F`?
2. **biological routing qualification:** does an internal gonotrophic-state signal causally regulate which terminal information source is behaviorally/sensorily used?

A positive answer to goal 1 does not automatically establish goal 2.

## Frozen candidate architecture

### Coarse state information source R

Primary biological candidate: NPF/RYamide gonotrophic endocrine state.

Operational state classes for the first experiment may be defined using tightly controlled physiological cohorts, with endocrine validation in matched samples:

- `R=0`: mated previtellogenic, non-blood-fed females;
- `R=1`: mated gravid females at a preregistered post-blood-meal interval when oviposition-site search is active.

Matched endocrine assays should verify the expected NPF/RYamide state difference. The cohort label itself is not counted as organismal evidence that R is a query; causal R qualification is tested separately below.

### Host-branch terminal information A

Primary candidate: an IR8a-dependent acidic host-odor distinction.

Freeze:

- exact acidic stimulus or blend;
- fixed CO2/thermal/visual background;
- stimulus duration and concentration;
- neural/behavioral threshold defining `A=0` versus `A=1`.

An `Ir8a` loss-of-function cohort is the principal causal validation control.

### Oviposition-branch terminal information B

Primary candidate: an Ir68a-dependent water-vapor/humidity distinction used to locate water-filled containers.

Freeze:

- exact dry versus humid/water-filled target geometry;
- humidity gradient or vapor stimulus threshold;
- assay duration;
- neural/behavioral threshold defining `B=0` versus `B=1`.

`Ir68a` loss-of-function is the principal causal validation control. A direct-placement assay beside water is required to distinguish failure to locate the site from failure to lay eggs.

Geosmin/Orco may be retained as a secondary replication cue but must not replace B after the primary outcome is inspected.

## Core four-world task

Only these four worlds count toward the first frozen finite-task receipt:

| world | R | A | B | target program |
|---|---:|---:|---:|---|
| H0 | 0 | 0 | 0 | continue host search |
| H1 | 0 | 1 | 0 | approach/accept host |
| O0 | 1 | 0 | 0 | continue oviposition-site search |
| O1 | 1 | 0 | 1 | accept/approach site and progress to oviposition |

The unused terminal stimulus is physically held at its preregistered baseline in each branch. `0` therefore means an experimentally declared outcome, not retrospective “irrelevance.”

## Cross-branch controls — outside the four-world receipt

To test the biological routing interpretation, run additional conditions that do **not** alter the frozen four-world task:

- previtellogenic `R=0` with B varied low/high while A is baseline;
- gravid `R=1` with A varied low/high while B is baseline;
- optionally, both A and B varied factorially within each R state.

These controls answer whether terminal information remains sensorily available outside its focal branch and whether it changes the wrong target program.

Their role is mechanistic qualification, not retroactive editing of the finite task.

## Target operationalization

The four targets must be scored from predeclared behavioral variables.

### H0 — continue host search

Candidate definition: remains in search/flight state without crossing a preregistered host-approach/landing/feeding criterion during the trial.

### H1 — approach/accept host

Candidate definition: crosses a preregistered host-oriented approach, landing, probing or feeding threshold under the fixed host-assay background.

### O0 — continue oviposition-site search

Candidate definition: gravid search/humidity-seeking state without entering/accepting the target site or depositing eggs within the preregistered endpoint.

### O1 — accept/approach oviposition site

Candidate definition: enters/accepts the humid water-associated site and, where assay duration permits, progresses toward egg deposition.

The target labels must be distinguishable independently of the finite-task solver. If H0 and O0 cannot be supported as different programs, use the preregistered coarsened accept/reject control and retain its result.

## Acquisition-cost contract

Do not assume equal physiological costs.

Before opening the outcome matrix, choose one cost interpretation and keep it fixed. Candidate choices include:

- standardized acquisition time;
- number/duration of sampling episodes;
- integrated neural activity under a declared metric;
- energetic proxy;
- a deliberately abstract positive integer laboratory resource scale.

The four-target structural result is robust for all positive integer `(r,a,b)`:

`C_A = r + max(a,b)`

`C_F = r + a + b`

`g = min(a,b) > 0`.

If no positive biological/resource interpretation can be defended for R, the system does not qualify as a direct realization of the present positive-cost flagship task, even if a zero-cost context-conditioned model would be interesting separately.

## Measurement layers

### Layer M1 — frozen outcome matrix

For each core world, record the predeclared outcomes of R, A, B and the target program.

Admission requires deterministic/discretized outcomes under the prospectively declared confidence rule. If guaranteed resolution cannot be defended, classify the task `UNRESOLVED_MEASUREMENT` rather than forcing a binary label.

### Layer M2 — terminal-channel causality

For A:

- compare wild type versus `Ir8a` perturbation;
- confirm loss/reduction of the declared acidic-cue sensory signal;
- measure host-program output;
- assay the same perturbation in gravid controls.

For B:

- compare wild type versus `Ir68a` perturbation;
- confirm loss/reduction of the declared humidity/water-vapor signal;
- measure water-container/site-search output;
- verify that direct placement at water preserves egg laying;
- assay the same perturbation in host-search controls.

Broad or cross-branch effects are recorded as coupling, not hidden.

### Layer M3 — R causality

Manipulate the NPF/RYamide/NPYLR7 axis prospectively.

At minimum measure:

- R endocrine marker/state;
- A neural/sensory response;
- B neural/sensory response;
- host-search target behavior;
- oviposition-site-search target behavior;
- locomotion and egg-development controls.

Possible interventions include preregistered RYamide/NPF manipulations and NPYLR7 genetic/pharmacological perturbation.

A true routing result requires more than general behavioral suppression. The manipulation should alter the relative use/value of A versus B in the direction predicted by R while pleiotropic changes are separately quantified.

## Prospective admission hierarchy

### P0 — biological task semantics qualified

Worlds, cues, costs and targets are predeclared and measurable.

### P1 — finite positive gap

The frozen matrix passes exact computation with `C_A<C_F`.

A zero-gap result is retained as `ADMITTED_ZERO_GAP`.

### P2 — terminal-channel causality

A and B each have causal sensory handles consistent with their declared branch-specific target distinctions.

### P3 — state-dependent routing

Manipulating R changes terminal information use / target-program allocation in the preregistered direction, beyond nonspecific motivational or motor effects.

### P4 — heritable genotype-policy bridge

A specific heritable edit can be mapped onto a policy-state change only after full cross-context effects are measured.

### P5 — population claims

Not licensed by this experiment alone. Mutation bias, population process and absolute mutation-rate scale remain additional requirements.

## Primary success criterion

The strongest feasible first conclusion is:

> In a preregistered four-world gonotrophic decision task, Aedes uses context-contingent terminal information such that the exact adaptive resolution cost is lower than the fixed-repertoire cost, and the context dependence is supported by causal state- and sensory-channel perturbations.

Do not use this sentence unless P0–P3 all pass.

## Primary negative outcomes

The study is still informative if any of the following occur:

- `g=0` under the frozen four-target task;
- only the coarsened target ontology is defensible and gives `g=0`;
- A or B cannot be discretized with guaranteed resolution;
- terminal cues remain equally used in both states and only action/motivation changes;
- R manipulations affect general physiology but not relative terminal information use;
- Ir8a/Ir68a perturbations produce broad coupled effects incompatible with a local routing interpretation.

These outcomes must not trigger within-study world/cue/target redesign.

## Analysis freeze

Before the final outcome matrix is opened, store a versioned receipt containing:

- world definitions;
- cohort/state definitions;
- R/A/B measurement rules;
- target scoring thresholds;
- cost convention;
- perturbations;
- exclusion rules;
- exact solver version/commit;
- planned admission-state decision tree.

A subsequent redesigned experiment is allowed only as a new prospectively frozen task with the previous negative receipt retained.

## Scope

This protocol is intentionally upstream of the routing mutation/population side theory. Even a successful P0–P4 result does not identify stationary genotype occupancy or biological waiting time.