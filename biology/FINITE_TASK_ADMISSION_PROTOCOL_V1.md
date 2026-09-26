# Finite-task empirical admission protocol v1

## Purpose

This protocol is the hard gate between the abstract adaptive-gain theory and any biological claim that a real system realizes a finite sensing gap.

It is designed to prevent retrospective task construction: worlds, targets, cues, cue costs and exclusion rules must be frozen before the outcome matrix is opened.

The protocol is system-agnostic. The C. elegans prospectus is the first candidate use case.

## Admission states

Every candidate task ends in exactly one of these states:

- `ADMITTED_POSITIVE_GAP`: the frozen task is empirically supported and exact computation gives `g=C_F-C_A>0`.
- `ADMITTED_ZERO_GAP`: the frozen task is empirically supported and gives `g=0`.
- `ADMITTED_NEGATIVE_GAP_IMPOSSIBLE`: invalid because adaptive cost cannot exceed fixed cost under the declared definitions; treat as a data/model audit failure.
- `UNRESOLVED_MEASUREMENT`: one or more frozen cue outcomes cannot be assigned with the required confidence.
- `REJECTED_TASK_SEMANTICS`: a declared cue or cost does not correspond to a defensible biological measurement.
- `REJECTED_REDUNDANCY`: an allegedly branch-specific cue is not branch-specific under perturbation.
- `REJECTED_TARGET_INSTABILITY`: target/action labels change across repeats or depend on post-hoc recoding.
- `REJECTED_POSTHOC_REDESIGN`: worlds, cues, costs or targets were changed after inspecting the gap.

A failed task is a scientific result. It may motivate a new, independently preregistered task, but the failed receipt remains frozen.

## Stage 0 — preregistration freeze

Before opening the full empirical outcome matrix, record:

1. system, sex/stage/physiological state restrictions;
2. represented alternatives `W={w_1,...,w_n}`;
3. target/action map `y(w)`;
4. declared cues `Q={q_1,...,q_m}`;
5. outcome alphabet and arity of every cue;
6. cue-acquisition cost convention;
7. missing/unresolved outcome rule;
8. replication and measurement thresholds;
9. genotype/regulatory perturbations, if any;
10. criterion for branch specificity / pleiotropic failure.

Hash or otherwise version this declaration before the final matrix is inspected.

## Stage 1 — biological cue qualification

A declared query is admitted only if all are true:

- it is an organism-level information source or explicitly justified internal state signal;
- its outcome is experimentally observable;
- the acquisition cost used by the finite-task solver has a biological interpretation fixed in advance;
- the cue is not merely a researcher-side measurement with no organismal counterpart;
- if a cue is unavailable in a state, the meaning of unavailability is declared before analysis.

Expression of a receptor alone is not a query-cost measurement.

## Stage 2 — empirical outcome matrix

Measure every declared cue in every represented world.

No cell may be assigned `irrelevant`, `constant`, `missing`, or a collapsed outcome merely because doing so produces a larger adaptive gap.

For stochastic measurements, the deterministic finite-task model can only be used after a prospectively declared discretization/guaranteed-resolution rule is met. Otherwise the candidate belongs to a noisy/probabilistic extension and is not admitted to the current theorem.

## Stage 3 — target validation

The target/action partition must be independently meaningful.

Examples of admissible support include:

- experimentally distinct actions with a predeclared functional interpretation;
- demonstrated receptor/circuit-dependent behavioral categories;
- independently specified management/decision classes in a non-neural system.

Do not define targets by clustering the observed cue matrix after the fact.

## Stage 4 — exact finite-task computation

Once the task is frozen and admitted, compute:

- exact adaptive minimum `C_A`;
- exact fixed minimum `C_F`;
- gap `g=C_F-C_A`;
- one optimal adaptive certificate;
- one optimal fixed certificate;
- the set of mandatory/irreducible fixed obligations where applicable.

The biological claim is the exact result for this frozen task, not a universal property of the organism.

## Stage 5 — independent witness audit

For a positive gap, verify independently that:

1. the adaptive certificate distinguishes every required target pair;
2. every proposed cheaper adaptive strategy fails;
3. the fixed certificate distinguishes every required target pair;
4. every fixed subset below `C_F` fails;
5. the claimed gap does not depend on an unmeasured or recoded outcome.

Small tasks should be exhaustively enumerated when feasible.

## Stage 6 — genotype-policy bridge

Only after a positive or zero finite task is established may a heritable perturbation be mapped onto policy states.

For every proposed mutation edge:

- identify the exact genomic/regulatory edit;
- repeat the full frozen cue matrix;
- measure all target behaviors;
- audit all declared contexts, not only the intended branch;
- encode coupled changes as one coupled move rather than splitting them into artificial branch-local steps.

A laboratory CRISPR edit proves experimental manipulability, not its natural proposal probability.

## Stage 7 — accessibility claim gate

Mutation accessibility requires, beyond the finite task:

- a declared genotype-policy map;
- a mutation support graph;
- a declared start genotype/state.

Only graph reachability and path quantities licensed by those declarations may be reported.

Do not infer a universal edit distance from `q` or `g` alone.

## Stage 8 — stationary population claim gate

Stationary phase occupancy additionally requires:

- relative mutation/proposal bias or an equivalent neutral stationary measure;
- an explicit population process connecting mutation and selection.

Without these, PR #33 shows occupancy is nonidentified even on fixed local support.

## Stage 9 — biological time gate

Waiting time in generations additionally requires an absolute mutation/proposal-rate scale and a mapping from model attempts/substitutions to biological time.

A Markov-chain hitting time in proposal attempts must not be relabeled as generations.

## Minimal receipt

Every empirical candidate should freeze a receipt containing at least:

```text
candidate_id
protocol_version
preregistered_declaration_ref
worlds
targets
cues
cue_arities
cue_costs
measurement_rule
outcome_matrix_ref
C_A
C_F
gap
adaptive_certificate_ref
fixed_certificate_ref
admission_state
genotype_policy_bridge_state
mutation_support_state
mutation_bias_state
absolute_rate_state
population_process_state
licensed_claims
prohibited_claims
```

## Interpretation ladder

The allowed inference ladder is intentionally one-way:

`finite task admitted`

`-> exact C_A, C_F, g`

`-> [only with genotype-policy map + support] accessibility`

`-> [only with mutation bias + population process] stationary occupancy`

`-> [only with absolute rate scale] biological waiting time`.

Failure at any layer blocks only downstream claims. It does not invalidate the upstream finite-task result.

## Relation to the flagship

This protocol does not alter the frozen Theoretical Ecology submission. It operationalizes the existing claim boundary: natural history defines a candidate decision problem; the finite theory evaluates the frozen structure; downstream evolutionary accessibility requires additional biological declarations that the flagship does not identify.