# Aedes Phase 1 — LVP state-perturbation gate v1

## Purpose

Validate a nutrient-independent NPYLR7 state perturbation in the LVP background before spending resources on same-background terminal-channel genetics.

This is execution planning downstream of `freeze/aedes-pre-data-admission-v1`. It does not alter frozen scientific semantics and does not by itself test empirical adaptive gain.

## Why this is Phase 1

Published next-generation NPYLR7 agonists suppress host-seeking/blood feeding at 1 micromolar after delivery in protein-free saline, with behavioral testing 2 days later. Published Ir68a oviposition-site genetics are in LVP, whereas the agonist and Ir8a studies used Orlando.

The first integration question is therefore simply:

> Does selective NPYLR7 activation produce a reproducible host-suppressed phenotype in LVP without a nutritive blood meal or gross nonspecific impairment?

If no, stop the LVP-first integration route.

## Cohort logic

Use matched previtellogenic LVP females under a preregistered age, mating, sugar-access and circadian regime.

Minimum treatment structure:

1. protein-free saline control;
2. active NPYLR7 agonist A at 1 micromolar;
3. active NPYLR7 agonist B at 1 micromolar.

Preferred active pair:

- TDI-014188;
- TDI-014184.

Both were reported to reduce blood feeding at 1 micromolar and have substantially better in-vitro potency than the original lead. TDI-014186 is a valid alternative independent active compound if reagent access favors it.

Use two active compounds rather than one so a single compound-specific phenotype is not promoted directly to a state-mechanism result.

Optional chemical negative control:

- TDI-014170 at 1 micromolar, which showed strong in-vitro activity but did not significantly reduce host seeking or biting in the published in-vivo assays.

This control is useful for separating receptor-cell potency from behavioral efficacy but is not required for the core go/no-go decision.

## Delivery

Follow the published next-generation agonist logic as closely as the LVP background permits:

- deliver compound in non-nutritive/protein-free saline;
- use a final compound concentration of 1 micromolar for the primary replication;
- record feeding success and meal-size proxy for every group;
- allow 48 h recovery before host-seeking testing.

Protein-free delivery is essential here because the purpose is to move one candidate internal-state signal without inducing egg development through a blood/protein meal.

## Primary behavioral readout

Use the published miniport logic with CO2 plus human odor where feasible.

For every replicate, retain at least:

- number introduced;
- number activated/left start compartment if separately measurable;
- number reaching attraction trap;
- treatment assignment;
- feeding-success / meal-size record;
- batch/day/cage metadata.

Do not pool individuals across treatment batches in a way that loses replicate identity.

## Secondary A-channel readout

If apparatus access permits in the same study, add the frozen acidic-host-cue dimension using the established lactic-acid + CO2 logic.

Important interpretation:

- this can show that NPYLR7 activation changes the A-related phenotype in LVP;
- it does **not** yet make that effect Ir8a-causal in LVP, because the published Ir8a genetic validation is from a different background.

Same-background Ir8a causality belongs to Stage B after a positive routing screen.

## Nonspecific-effect controls

At minimum verify that treatment does not trivially explain reduced host seeking through:

- lower meal acceptance or markedly smaller saline meals;
- gross locomotor impairment;
- excessive mortality;
- obvious failure of flight/activation.

If technically feasible, add an assay of general odor-independent movement/arousal.

## Mechanistic-specificity hierarchy

### Level P1a — pharmacological reproduction

Both independent active compounds suppress host seeking relative to matched saline without gross nonspecific impairment.

This is enough to continue feasibility testing, but not enough to set `state_routing_causality_qualified=True`.

### Level P1b — receptor-specific reproduction

In addition to P1a, the phenotype is lost or strongly reduced in an LVP-compatible NPYLR7 perturbation, or an equivalently strong receptor-specificity experiment.

This is the preferred gate before making strong claims that the LVP treatment acts through NPYLR7 rather than merely resembling the published Orlando phenotype.

## Prospective outcome classes

### F0 — failed transfer

Neither active compound reproducibly suppresses LVP host seeking.

Action: stop LVP-first integration. Do not substitute additional compounds sequentially until one works.

### F1 — compound-specific effect

Only one active compound suppresses host seeking.

Action: treat as unresolved pharmacology. Do not promote to the routing experiment without an independent specificity explanation.

### F2 — reproducible state-like host suppression

Two independent active compounds suppress host seeking without nonspecific impairment.

Action: proceed to A/B relative-dependency screening. Keep `R` composite/unresolved.

### F3 — receptor-specific host suppression

F2 plus NPYLR7-specificity in the chosen background.

Action: strongest Phase-1 basis for using pharmacological NPYLR7 activation as one controlled coordinate of R in the next experiment.

## Analysis discipline

Do not define success only as `p < 0.05` after looking at the data.

Before opening the final experiment:

- choose the primary behavioral proportion/contrast;
- define the replicate unit;
- specify exclusion criteria;
- predeclare how batch/day effects are handled;
- choose an effect-size/uncertainty criterion or power target from pilot variance.

The published study can guide assay scale, but its effect size in Orlando must not be assumed to be the LVP effect size.

## Hard stops

- no blood/protein meal in the primary pharmacological manipulation arm;
- no replacement of failed agonists with an open-ended compound search;
- no interpretation of host suppression as B-channel recruitment;
- no empirical adaptive-gain claim from Phase 1;
- no same-background Ir8a reconstruction before Phase 1 and the subsequent A/B screen justify it.

## Literature anchors

- Duvall LB et al. 2019. Cell 176:687-701.e5. DOI 10.1016/j.cell.2018.12.004.
- Zeledon EV et al. 2024. Next-generation NPYLR7 agonists; active compounds at 1 micromolar after non-nutritive saline delivery and 2-day recovery.
- Raji JI et al. 2019. Current Biology. DOI 10.1016/j.cub.2019.02.045, for the A-channel lactic-acid + CO2 assay architecture.

## Gate to Phase 2/3

Proceed only after at least F2.

Even F3 establishes only a manipulable host-suppression coordinate. The decisive frozen scientific edge remains:

`R -> relative decision use/dependency of A versus B`.
