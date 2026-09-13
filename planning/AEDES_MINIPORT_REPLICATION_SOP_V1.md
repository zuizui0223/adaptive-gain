# Aedes Miniport replication SOP v1

## Scope

Execution-readiness SOP only. This document does not change the frozen scientific task or Phase 1 decision rules. It translates the published 2024 Miniport host-seeking assay into a reproducible local implementation contract.

## Published assay anchor

The 2024 NPYLR7 study specifies:

- starting canister: approximately 6 in x 3 in x 3 in acrylic with mesh for airflow;
- group size: 10-20 females per canister;
- mosquitoes loaded into canisters 24 h after the treatment meal;
- two water-soaked cotton balls supplied during overnight acclimation to prevent desiccation;
- behavioral test at 48 h after meal;
- four attraction positions used in parallel, with canisters randomly assigned to positions 1-4;
- 5 min pre-trial acclimation after connection to the apparatus;
- 5% CO2 delivered at 30 mL/min;
- 30 s CO2 pre-activation before the sliding door opens;
- human odor source: nylon stocking worn by the same experimenter for 8-10 h and stored sealed at -20 C until use;
- sliding door open for **5 min** in the 2024 screening assay;
- attraction scored as mosquitoes in the attraction trap / total eligible mosquitoes.

The 5 min endpoint, rather than the earlier 2019 10 min implementation, is the canonical Phase 1 v1 duration unless a preregistered apparatus-qualification amendment is made before any compound outcome is opened.

## Published treatment-meal contract

The source study used Glytube membrane feeding with the following anchors:

- females fasted with access to water for 24 h before feeding;
- saline vehicle: 400 mM NaHCO3 in deionized water;
- high-concentration compound stocks: 30 mM in 100% DMSO, stored at -20 C;
- final test-compound concentration: 1 micromolar;
- ATP: 1 mM final concentration;
- meals / heating elements warmed in a 42 C water bath for 15 min before feeding;
- females allowed 15-20 min to feed to repletion;
- abdominal engorgement scored and supported by weighing;
- incompletely fed females discarded before behavioral testing;
- water wick supplied during the 48 h recovery;
- mortality counted at 24 h after meal.

The exact source-lab purity / lot / handling data for TDI-014188 and TDI-014186 remain an execution-readiness gate in issue #49. Local implementation may not silently change solvent or formulation after LVP outcome data are opened.

## Locked Phase 1 groups

1. saline vehicle;
2. TDI-014188;
3. TDI-014186.

Environmental controls should include non-fed and blood-fed females under the published Miniport qualification logic where institutionally and experimentally feasible.

No replacement agonist is permitted after LVP outcome data are opened.

## Randomization and blocking

For every behavioral block:

- randomize treatment canisters across Miniport positions 1-4;
- balance position exposure across treatment groups across blocks;
- keep human-odor preparation constant within a confirmatory batch;
- blind scoring to treatment where technically feasible;
- treat replicate canister, not individual mosquito, as the primary independent behavioral unit unless the final preregistered analysis explicitly uses a hierarchical model.

## Published daily environmental-QC gate

The 2024 study used explicit day-level controls:

- if non-fed females were <50% attracted, halt and discard that experimental day's behavioral data;
- if saline-fed females were <50% attracted, halt and discard that experimental day's behavioral data;
- if blood-fed females were >20% attracted, halt and discard that experimental day's behavioral data.

These environmental-QC thresholds are adopted as the default Phase 1 v1 qualification contract because they were prespecified by the source method and directly protect interpretation of the assay.

If a local institution cannot run the blood-fed control during an apparatus-only build stage, that stage remains `BUILT_NOT_QUALIFIED`; full confirmatory qualification requires the complete frozen environmental-control logic or a prospectively justified v2 amendment before compound outcomes are opened.

## Required controls

### Meal / intake control

Record:

- proportion feeding to repletion;
- post-feeding mass or equivalent intake proxy;
- treatment-meal identity;
- exclusion of incompletely fed females using the frozen rule.

The published study explicitly measured feeding to repletion and female weight to exclude palatability / intake artifacts.

### Mortality control

Record mortality at 24 h post-meal and immediately before behavioral testing.

The source compound-screening framework treated >50% mortality as high lethality and excluded such compounds from behavioral interpretation. Under the locked two-compound Phase 1 design, a comparable high-lethality result is a toxicity failure, not an invitation to select a third agonist.

### General-performance control

Use `planning/AEDES_GENERAL_PERFORMANCE_CONTROL_SOP_V1.md` as the host-cue-independent locomotor / activity control.

A compound that suppresses Miniport attraction while causing gross general locomotor impairment cannot satisfy the Phase 1 selective state-perturbation gate.

## Primary endpoint

For each replicate canister:

`host_seeking_fraction = n_entered_attraction_trap / n_eligible_at_trial_start`

Any dead mosquitoes may only be excluded under the prospectively frozen denominator rule. Denominator handling may not be changed after treatment effects are visible.

The source paper normalized behavioral values to matched saline attraction for presentation / analysis. The local confirmatory analysis must freeze whether raw fractions, block-normalized contrasts, or a hierarchical model is primary before treatment labels are opened.

## Confirmatory classification

Use `planning/AEDES_PHASE1_2_CONFIRMATORY_DECISION_RULES_V1.md` and the machine-readable phase receipt.

- `GO`: both TDI-014188 and TDI-014186 reproduce the preregistered host-suppression direction versus saline, the environmental-QC day passes, and intake / mortality / general-performance controls pass;
- `UNRESOLVED`: one compound only, inconsistent independent blocks, borderline general impairment, or assay-QC ambiguity;
- `STOP`: both preselected compounds fail under an otherwise qualified assay, high lethality / broad impairment prevents selective interpretation, or the apparatus cannot reproduce the source qualification baseline.

Do not add compounds, alter host cues, change trial duration, or relax day-level QC after outcome data are opened.

## Build / validation gate before compounds

Before any confirmatory compound experiment, the local Miniport must pass qualification showing:

1. stable non-fed and saline-fed attraction at or above the frozen source threshold;
2. blood-fed attraction at or below the frozen source threshold;
3. no persistent Miniport position bias beyond the preregistered tolerance;
4. acceptable between-block repeatability;
5. no excessive desiccation / mortality;
6. reproducible scorer / recording workflow;
7. verified CO2 flow at the target concentration and rate.

Pilot qualification may tune mechanical factors such as seals, airflow balance and lighting using control mosquitoes only. Once the confirmatory apparatus specification is frozen, no treatment-informed mechanical tuning is permitted.

## Source anchors

- Zeledon et al. 2024, Parasites & Vectors, DOI 10.1186/s13071-024-06347-w — canonical Phase 1 feeding, Miniport, 5 min trial and day-level environmental QC.
- Duvall et al. 2019, Cell, DOI 10.1016/j.cell.2018.12.004 — original Miniport and NPYLR7 receptor-specificity framework.
- VosshallLab/Miniport-Construction — public design repository referenced by the source studies.
